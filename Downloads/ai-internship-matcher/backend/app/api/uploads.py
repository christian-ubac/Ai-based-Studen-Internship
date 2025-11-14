from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from ..nlp.parser import parse_resume
from ..nlp.embedding import embed_text, save_embedding
from ..db import get_db
from .. import crud, models
import shutil, os

router = APIRouter(prefix="/upload", tags=["upload"])
UPLOAD_DIR = os.path.join(os.getcwd(), "backend", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/resume/{student_id}")
async def upload_resume(student_id:int, file: UploadFile = File(...), db=Depends(get_db)):
    filename = f"{student_id}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    parsed = parse_resume(path)
    emb = embed_text(parsed["text"])
    emb_path = save_embedding(student_id, emb, prefix="resume")
    resume = crud.create_resume(db, student_id=student_id, filename=filename,
                                parsed_text=parsed["text"],
                                skills=",".join(parsed["skills"]),
                                outcomes=",".join(parsed["outcomes"]),
                                embedding_path=emb_path)
    return {"status":"ok", "resume_id": resume.id}
