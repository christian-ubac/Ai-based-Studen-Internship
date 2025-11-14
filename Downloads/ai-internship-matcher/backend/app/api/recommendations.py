from fastapi import APIRouter, Depends
from ..db import get_db
from .. import crud
from ..nlp.embedding import load_embedding
from ..nlp.ranker import build_feature_vector, Ranker
import numpy as np
import torch
import os
from ..llm.llm_client import explain_match

router = APIRouter(prefix="/recommend", tags=["recommend"])
RANKER_PATH = os.path.join(os.getcwd(), "backend", "models", "ranker.pt")
ranker = None
if os.path.exists(RANKER_PATH):
    ckpt = torch.load(RANKER_PATH, map_location="cpu")
    input_dim = ckpt.get('input_dim')
    ranker = Ranker(input_dim)
    ranker.load_state_dict(ckpt['state_dict'])
    ranker.eval()

def cos(a,b):
    return float(np.dot(a,b)/(np.linalg.norm(a)+1e-8)/(np.linalg.norm(b)+1e-8))

@router.get("/student/{student_id}")
def recommend_for_student(student_id:int, db=Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        return {"error":"student not found"}
    if not student.resumes:
        return {"error":"student has no resumes"}
    resume = student.resumes[-1]
    resume_emb = load_embedding(resume.embedding)
    departments = crud.get_all_departments(db)
    results = []
    for d in departments:
        dept_emb = load_embedding(d.embedding)
        student_skills = set(resume.skills.split(",")) if resume.skills else set()
        dept_skills = set(d.required_skills.split(",")) if d.required_skills else set()
        overlap = len(student_skills.intersection(dept_skills))
        gpa_norm = (student.gpa or 0) / 4.0
        feat = build_feature_vector(resume_emb, dept_emb, gpa_norm, overlap)
        if ranker:
            with torch.no_grad():
                x = torch.tensor(feat, dtype=torch.float).unsqueeze(0)
                score = float(ranker(x).squeeze().item())
        else:
            base = cos(resume_emb, dept_emb)
            score = base * 0.9 + 0.05 * gpa_norm + 0.05 * (overlap/ max(1, len(dept_skills)))
        reason = explain_match(student, resume, d, score)
        rec = crud.create_recommendation(db, student.id, d.id, score, reason)
        results.append({"department": d.name, "score": score, "reason": reason})
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return {"student": student.name, "recommendations": results}
