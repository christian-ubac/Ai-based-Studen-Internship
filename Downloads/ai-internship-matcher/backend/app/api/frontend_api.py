"""
Frontend-facing API endpoints for resume upload and recommendation retrieval.
These endpoints are designed for the Vue frontend and don't require student IDs.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from ..nlp.parser import parse_resume
from ..nlp.embedding import embed_text, save_embedding
from ..db import get_db
from .. import models
from .scraper import scrape_internships
import shutil
import os
import uuid
from sqlalchemy.orm import Session
from typing import List, Dict, Any

router = APIRouter(prefix="/api", tags=["frontend"])
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def compute_recommendations(db: Session, resume: models.Resume) -> List[Dict[str, Any]]:
    """Compute match scores between a resume and active internships.
    Returns a list of recommendation dicts (same shape as the GET endpoint).
    """
    # Get all active internships
    internships = db.query(models.Internship).filter(models.Internship.is_active == 1).all()
    if not internships:
        return []

    resume_skills = set(s.strip().lower() for s in (resume.skills or "").split(",") if s.strip())
    resume_outcomes = set(o.strip().lower() for o in (resume.outcomes or "").split(",") if o.strip())

    results: List[Dict[str, Any]] = []
    for internship in internships:
        internship_skills = set(s.strip().lower() for s in (internship.required_skills or "").split(",") if s.strip())

        if internship_skills:
            matched = len(resume_skills.intersection(internship_skills))
            skill_score = int((matched / len(internship_skills)) * 100)
        else:
            skill_score = 40

        out_text = ((internship.title or "") + " " + (internship.description or "")).lower()
        outcome_matches = 0
        for o in resume_outcomes:
            if o and o in out_text:
                outcome_matches += 1

        outcome_boost = min(outcome_matches, 3) * 10
        match_score = min(100, int(0.8 * skill_score + outcome_boost))

        matched_skills_list = [s.strip() for s in (internship.required_skills or "").split(",") if s.strip().lower() in resume_skills][:5]

        if match_score > 0 or len(results) < 5:
            results.append({
                "id": internship.id,
                "title": internship.title,
                "company_name": internship.company_name,
                "location": internship.location,
                "description": internship.description,
                "posting_url": internship.posting_url,
                "matched_skills": matched_skills_list,
                "match_score": match_score,
                "posted_date": internship.posted_date.isoformat() if internship.posted_date else None
            })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:20]


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload resume from frontend.
    Returns resume_id and extracted skills for matching.
    """
    try:
        # Generate unique ID for this resume
        resume_id = str(uuid.uuid4())
        filename = f"{resume_id}_{file.filename}"
        path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Parse resume (extract text and skills)
        parsed = parse_resume(path)
        
        # Create embedding
        try:
            emb = embed_text(parsed["text"])
            emb_path = save_embedding(resume_id, emb, prefix="resume")
        except Exception as emb_err:
            # If embedding fails, just use empty string
            emb_path = ""
        
        # Save to database
        resume = models.Resume(
            filename=filename,
            parsed_text=parsed["text"],
            skills=",".join(parsed.get("skills", [])),
            outcomes=",".join(parsed.get("outcomes", [])),
            embedding=emb_path
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)

        # Trigger scraping from RapidAPI to refresh internship data (synchronous)
        try:
            # call internal scraper to fetch and persist newest internships
            scrape_internships(query="internship", limit=50, db=db)
        except Exception:
            # If scraping fails, continue and return recommendations from existing data
            pass

        # After saving and scraping, compute recommendations immediately and return them
        try:
            recs = compute_recommendations(db, resume)
        except Exception:
            recs = []

        return {
            "status": "ok",
            "resume_id": resume.id,
            "extracted_skills": parsed.get("skills", []),
            "recommendations": recs
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get-recommendations")
async def get_recommendations(resume_id: int = None, db: Session = Depends(get_db)):
    """
    Get AI internship recommendations based on uploaded resume.
    Returns list of internships with match scores.
    """
    try:
        # Get resume (latest if not specified)
        if resume_id:
            resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
        else:
            resume = db.query(models.Resume).order_by(models.Resume.created_at.desc()).first()

        if not resume:
            return []

        # Delegate to the shared helper
        return compute_recommendations(db, resume)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Frontend API is running"}
