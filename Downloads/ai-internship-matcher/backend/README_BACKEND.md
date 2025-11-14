Backend instructions:
- Create PostgreSQL DB and set DATABASE_URL env var.
- Install dependencies from requirements.txt.
- Run `python -m app.main` via uvicorn: `uvicorn app.main:app --reload --port 8000`
- Seed DB: `python backend/scripts/seed_db.py`
- Train ranker (optional): `python backend/scripts/train_ranker.py`
