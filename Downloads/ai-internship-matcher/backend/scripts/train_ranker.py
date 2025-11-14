import numpy as np
import torch
import torch.nn as nn
from app.nlp.ranker import Ranker, build_feature_vector
from app.nlp.embedding import load_embedding
import os
import random

# This script expects a simple CSV pilot_labels.csv with columns: resume_path, dept_path, label
# For convenience, if not found, this script will generate synthetic pairs from available embeddings.

EMBED_DIR = os.path.join(os.getcwd(), "backend", "embeddings")
MODEL_DIR = os.path.join(os.getcwd(), "backend", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def load_all_embeddings():
    files = [f for f in os.listdir(EMBED_DIR) if f.endswith(".npy")]
    embs = {}
    for f in files:
        embs[f] = np.load(os.path.join(EMBED_DIR, f))
    return embs

def synth_pairs(embs, n=200):
    resumes = [k for k in embs.keys() if k.startswith("resume_")]
    depts = [k for k in embs.keys() if k.startswith("dept_")]
    pairs = []
    for _ in range(n):
        r = random.choice(resumes)
        d = random.choice(depts)
        re = embs[r]; de = embs[d]
        # simple heuristic label: cosine > 0.6 and random
        cos = float(np.dot(re,de)/(np.linalg.norm(re)*np.linalg.norm(de)+1e-8))
        label = 1 if cos>0.55 else 0
        # add noise
        pairs.append((r,d,label))
    return pairs

def prepare_features(pairs, embs):
    X=[]; y=[]
    for r,d,label in pairs:
        re = embs[r]; de = embs[d]
        gpa = 0.75 if "alice" in r.lower() else 0.5
        overlap = 1.0
        feat = build_feature_vector(re,de,gpa,overlap)
        X.append(feat); y.append(label)
    X = np.stack(X); y = np.array(y)
    return X,y

def train():
    embs = load_all_embeddings()
    if not embs:
        print("No embeddings found in", EMBED_DIR)
        return
    pairs = synth_pairs(embs, n=300)
    X,y = prepare_features(pairs, embs)
    input_dim = X.shape[1]
    model = Ranker(input_dim)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.BCELoss()
    X_t = torch.tensor(X, dtype=torch.float)
    y_t = torch.tensor(y.reshape(-1,1), dtype=torch.float)
    for epoch in range(20):
        model.train()
        opt.zero_grad()
        out = model(X_t)
        loss = loss_fn(out, y_t)
        loss.backward()
        opt.step()
        if epoch%5==0:
            print(f"Epoch {epoch} loss {loss.item():.4f}")
    ckpt = {"input_dim": input_dim, "state_dict": model.state_dict()}
    torch.save(ckpt, os.path.join(MODEL_DIR, "ranker.pt"))
    print("Saved ranker to", os.path.join(MODEL_DIR, "ranker.pt"))

if __name__=='__main__':
    train()
