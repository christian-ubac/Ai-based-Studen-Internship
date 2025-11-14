from sentence_transformers import SentenceTransformer
import numpy as np
import os
from ..config import settings

MODEL = SentenceTransformer(settings.EMBEDDING_MODEL)
EMBED_DIR = os.path.join(os.getcwd(), "backend", "embeddings")
os.makedirs(EMBED_DIR, exist_ok=True)

def embed_text(text):
    vec = MODEL.encode([text], show_progress_bar=False)[0]
    return vec

def save_embedding(obj_id:int, vec:np.ndarray, prefix="resume"):
    path = os.path.join(EMBED_DIR, f"{prefix}_{obj_id}.npy")
    np.save(path, vec)
    return path

def load_embedding(path):
    return np.load(path)
