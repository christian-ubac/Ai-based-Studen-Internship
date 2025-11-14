# AI-Based Student Internship Matcher (Pilot)

This repository is a thesis-level pilot system for matching students (CCIS: IT/CS/IS) to internship departments with bias-mitigation practices.

Contents:
- `backend/` - FastAPI backend, NLP parsing, embedding, simple ranker, scraper prototype
- `frontend/` - Vue 3 minimal frontend (Vite)
- scripts to seed DB and train ranker

Quick start (local pilot):
1. Create PostgreSQL database and export DATABASE_URL env var.
2. Backend:
   - `cd backend`
   - `python -m venv venv && source venv/bin/activate`
   - `pip install -r requirements.txt`
   - `python -c "from app.db import Base, engine; from app import models; Base.metadata.create_all(bind=engine)"`
   - `python scripts/seed_db.py`
   - `uvicorn app.main:app --reload --port 8000`
3. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev` (open displayed port)

Bias & fairness:
- Protected attributes (age, name, email) are *not used* by the matching model.
- Explanations are generated without demographics.
- Include fairness audits in thesis methodology.

Notes:
- The web scraper is a research skeleton. Check `robots.txt` and JobStreet terms before scraping.
- LLM explainers are optional and require API keys.
