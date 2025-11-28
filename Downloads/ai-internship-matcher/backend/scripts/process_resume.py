"""
Helper to process a resume file: parse text, create embedding, save Resume record.

Provides `process_resume_file(db, path, filename, run_scrape=False)` which
returns a tuple `(resume_id, parsed, embedding_path)`.

This module intentionally keeps responsibilities narrow so it's reusable
from API endpoints and CLI scripts.
"""
from datetime import datetime
from typing import Optional, Tuple
import os
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.nlp.parser import parse_resume
from app.nlp.embedding import embed_text, save_embedding
from app import models

try:
    # scraper import (callable expects `db` parameter)
    from app.api.scraper import scrape_internships
except Exception:
    scrape_internships = None


def process_resume_file(path: str, filename: Optional[str] = None, db: Optional[Session] = None, run_scrape: bool = False) -> Tuple[int, dict, str]:
    """Parse, embed and persist a resume file.

    - `path`: filesystem path to uploaded file
    - `filename`: original filename (optional)
    - `db`: optional SQLAlchemy Session; if None a new SessionLocal will be used
    - `run_scrape`: if True will attempt to call `scrape_internships(..., db=...)` after saving

    Returns: `(resume_id, parsed_dict, embedding_path)`
    """
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        parsed = parse_resume(path)

        resume = models.Resume(
            filename=filename or os.path.basename(path),
            parsed_text=parsed.get("text", ""),
            skills=",".join(parsed.get("skills", [])),
            outcomes=",".join(parsed.get("outcomes", [])),
            created_at=datetime.utcnow()
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)

        emb_path = ""
        try:
            emb = embed_text(parsed.get("text", ""))
            # If model is available, store vector directly in DB (pgvector)
            try:
                # accept numpy arrays or lists
                resume.embedding = emb.tolist() if hasattr(emb, 'tolist') else list(emb)
                db.add(resume)
                db.commit()
            except Exception:
                # Fallback: save to disk and store path
                db.rollback()
                emb_path = save_embedding(resume.id, emb, prefix="resume")
                resume.embedding = emb_path
                db.add(resume)
                db.commit()
        except Exception:
            # embedding optional; continue
            db.rollback()

        # Optional: refresh internships via scraper
        if run_scrape and callable(scrape_internships):
            try:
                # call scraper with same db session
                scrape_internships(query="internship", limit=50, db=db)
            except Exception:
                # do not propagate scraper errors
                pass

        return resume.id, parsed, emb_path
    finally:
        if own_session:
            db.close()
