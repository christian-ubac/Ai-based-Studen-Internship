import torch
import torch.nn as nn
import numpy as np

class Ranker(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

def build_feature_vector(resume_emb, dept_emb, gpa_norm, skill_overlap):
    return np.concatenate([resume_emb, dept_emb, np.array([gpa_norm, skill_overlap])], axis=0)
