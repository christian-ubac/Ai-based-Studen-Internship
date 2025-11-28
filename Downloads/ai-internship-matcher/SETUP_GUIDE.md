# AI Internship Matcher - Setup & Running Guide

## Overview
This application matches AI/ML students with relevant internship opportunities using resume analysis and skill matching.

- **Frontend**: Vue 3 (Vite)
- **Backend**: FastAPI with PostgreSQL
- **Features**: Resume upload, skill extraction, internship matching, recommendation ranking

---

## Prerequisites
- Python 3.8+
- Node.js 16+

# AI Internship Matcher — Setup & Running Guide

This document walks through setting up the project (frontend + backend) on Windows
using PowerShell. It covers environment setup, database creation, seeding, and running
the application end-to-end.

Workspace root (example):
`c:\Users\ACER\Downloads\final na jud ni xd\Ai-based-Studen-Internship\Downloads\ai-internship-matcher`

---

## 1 — Prerequisites
- Python 3.8+ (recommend 3.10/3.11)
- Node.js 16+ and npm
- PostgreSQL (local) or Docker
- PowerShell (you have v5.1)
- git

Optional: Docker for Postgres or pgAdmin

---

## 2 — Backend setup (venv, deps, env)

1. Open PowerShell and create/activate a virtual environment in `backend`:

```powershell
cd "<repo-root>\backend"
python -m venv .venv
. .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
# Install requirements. Note: on Windows `pgvector` may fail to build; see Troubleshooting.
pip install -r requirements.txt
```

2. Create `backend/.env` (or set env vars in PowerShell). Minimum keys:

```
DATABASE_URL=postgresql://internship_user:Internship%402025@localhost:5432/internshipdb
RAPID_API_KEY=your_rapidapi_key_here
RAPID_API_HOST=internships-api.p.rapidapi.com
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
OPENAI_API_KEY=
JOBSCRAPER_RATE_LIMIT=1.0
ALLOW_DEV_SEED=False
```

Use PowerShell to set for the session (example):

```powershell
$env:DATABASE_URL='postgresql://internship_user:Internship%402025@localhost:5432/internshipdb'
$env:RAPID_API_KEY='your_rapidapi_key_here'
$env:RAPID_API_HOST='internships-api.p.rapidapi.com'
```

Note: Passwords with special characters must be URL-encoded in `DATABASE_URL` (e.g. `@` → `%40`).

---

## 3 — Create PostgreSQL database

Option A — local Postgres (psql):

```powershell
# Run as a user with rights to create roles/databases (often 'postgres')
psql -U postgres -h localhost -p 5432
# In psql:
CREATE ROLE internship_user WITH LOGIN PASSWORD 'Internship@2025';
CREATE DATABASE internshipdb OWNER internship_user;
\q
```

Option B — use helper script (from backend, venv active):

```powershell
python .\scripts\create_db.py
# If your postgres superuser requires a password, set SUPERPASS in env first:
$env:SUPERPASS='your_postgres_super_password'
python .\scripts\create_db.py
```

Option C — Docker Postgres:

```powershell
docker run --name ai-internship-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=internshipdb -p 5432:5432 -d postgres:15
```

### 3.1 — Enable `pgvector` extension (optional, recommended)

If you plan to store embeddings in Postgres and run vector similarity queries, enable `pgvector`:

```powershell
# Connect as superuser
psql -U postgres -h localhost -p 5432
# In psql:
CREATE EXTENSION IF NOT EXISTS vector;
\q
```

Note: `pgvector` requires the Postgres extension; the Python package `pgvector` lets SQLAlchemy use it. On Windows installing the `pgvector` Python package may be difficult; see Troubleshooting.

---

## 4 — Seed the database

1. Seed program outcomes (Philippine-focused):

```powershell
cd <repo-root>\backend
. .venv\Scripts\Activate.ps1
python .\scripts\seed_program_outcomes.py
```

2. Create example students/resume (optional):

```powershell
python .\scripts\seed_db.py
```

3. Seed internships (RapidAPI-backed, Philippines-only):

```powershell
# helper that loads backend/.env and runs the seeder (checks RAPID_API_KEY)
\<repo-root>\backend\scripts\run_seed_internships.ps1
# or run directly (ensure RAPID_API_KEY is in env)
cd backend
python .\scripts\seed_internships.py
```

Notes:
- `seed_internships.py` now enforces PH-only insertions by matching location text and `.ph` URLs.
- Ensure `RAPID_API_KEY` and `RAPID_API_HOST` are set in `.env` or env before running the seeder.

### 4.1 — Seed via API (guarded)

If you prefer to trigger seeding from the running backend (useful for remote VMs), there's a guarded developer endpoint. Only enable when you trust the environment.

1. Set `ALLOW_DEV_SEED=True` in `backend/.env`.
2. Start the backend (see next section).
3. Call the endpoint:

```powershell
Invoke-RestMethod -Method POST -Uri http://localhost:8000/api/dev/seed
```

This endpoint runs `seed_program_outcomes.py` and `seed_internships.py` and returns a JSON report. It is disabled by default (`ALLOW_DEV_SEED=False`).

---

## 5 — Start the backend server

From `backend/` with venv active:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```powershell
Invoke-RestMethod -Method GET -Uri http://localhost:8000/api/health
# expected: {"status":"ok","message":"Frontend API is running"}
```

---

## 6 — Frontend setup & run (Vite)

Open a new PowerShell terminal and run:

```powershell
cd <repo-root>\frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser. The frontend proxies API requests to the backend (port 8000).

---

## 7 — Verify end-to-end

1. Open frontend UI and upload a resume (PDF/DOCX/TXT); the frontend calls `POST /api/upload-resume`.
2. The upload returns `resume_id` and extracted skills; recommendations will be computed from internships in DB.
3. If you want updated recommendations after scraping completes, poll `GET /api/get-recommendations?resume_id=<id>`.

### 7.1 — Verify DB connectivity and pgvector

Run the included helper:

```powershell
cd <repo-root>\backend
. .venv\Scripts\Activate.ps1
python .\scripts\verify_db_connection.py
```

This prints a masked `DATABASE_URL`, public table count, and whether `pgvector` is installed in the DB.

---

## 8 — Optional: pgAdmin

Add a server in pgAdmin:
- Host: `localhost`
- Port: `5432`
- Username: `internship_user` (or your DB user)
- Password: the DB password

Use Query Tool to inspect tables, e.g. `SELECT tablename FROM pg_tables WHERE schemaname='public';`.

---

## 9 — Troubleshooting, seed diagnostics & cleanup

- **Database connection**: verify `DATABASE_URL`, Postgres is running, and credentials are correct. URL-encode special characters in the password (e.g. `@` → `%40`).
- **RapidAPI errors**: ensure `RAPID_API_KEY` and `RAPID_API_HOST` are set in `backend/.env` or the process environment and you haven’t exceeded rate limits.
- **Embedding model downloads**: `sentence-transformers` downloads models on first use; ensure sufficient disk space and network access.
- **spaCy model**: run `python -m spacy download en_core_web_sm` if parsing fails.
- **Frontend `ECONNREFUSED` to `/api`**: start the backend first or adjust proxy in `frontend/vite.config.js`.

Specific `pip install -r requirements.txt` failures (common on Windows):

- If installation fails with `pgvector` or wheel-build errors, try:

```powershell
cd "<repo-root>\backend"
. .venv\Scripts\Activate.ps1
pip install pgvector-binary
pip install -r requirements.txt
```

`pgvector-binary` provides prebuilt wheels for common platforms and often avoids building from source on Windows. If that still fails, alternatives:

- Use WSL2 or a Linux container for backend development (recommended for ML/native libs on Windows).
- Skip `pgvector` and use file-based embeddings — the app falls back to storing `.npy` paths in the `embedding` column and works without pgvector.

If `pip install` exits with code 1, inspect the pip output closely and try installing the failing package individually; capture logs and share them if you want help interpreting the traceback.

### Seed scripts exit with non-zero code — focused troubleshooting

If `python .\scripts\seed_program_outcomes.py` or `python .\scripts\seed_internships.py` exit with `Exit Code 1`, do the following:

1. Activate venv and ensure dependencies installed:

```powershell
cd "<repo-root>\backend"
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Confirm env vars in `backend/.env` (especially `DATABASE_URL`, `RAPID_API_KEY`, `RAPID_API_HOST`):

```powershell
Get-Content backend\.env
```

3. Run the DB verifier to check connectivity and `pgvector` presence:

```powershell
python .\scripts\verify_db_connection.py
```

4. Capture full seeder output to a log file for inspection:

```powershell
python -u .\scripts\seed_program_outcomes.py 2>&1 | Tee-Object seed_program_outcomes.log
notepad seed_program_outcomes.log
```

5. Common causes and fixes:
- **OperationalError: could not connect to server** — Postgres not running or `DATABASE_URL` incorrect.
- **ModuleNotFoundError** — venv not activated or `pip install` failed.
- **Permission errors creating tables** — create DB with a superuser or give the DB user CREATE privileges, or run the helper `create_db.py` as a superuser.
- **pgvector-related install errors** — either install `pgvector-binary`, use WSL, or skip pgvector and rely on disk-based embeddings.

If you paste the top 20 lines of the seeder log here, I can help interpret and suggest the next patch.

---

## Repository cleanup performed (what changed)

- Removed frontend build artifacts in `frontend/dist/` (these are generated, not source).
- Removed deprecated seed scripts: `backend/scripts/seed_db.py` and `backend/scripts/seed_data.py`.
- Removed an optional helper `backend/scripts/git_remove_file.ps1`.
- Added `backend/.env.example` and updated `.gitignore` to ignore `backend/.env`, `__pycache__/`, `*.pyc`, and `frontend/dist/`.

If you have an existing `backend/.env` tracked in git and want to stop tracking it (keep it locally), run locally:

```powershell
git rm --cached backend/.env
git add backend/.env.example .gitignore
git commit -m "chore: add .env.example, ignore backend/.env and clean generated files"
git push
```

---

## 10 — Security & housekeeping

- Do NOT commit `backend/.env` with secrets. Consider adding `backend/.env` to `.gitignore` and create `backend/.env.example` with placeholders.
- Rotate any API keys accidentally committed.

---

## Quick copy-paste checklist

```powershell
# Backend
cd <repo-root>\backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# set env or edit backend/.env
python .\scripts\create_db.py   # optional helper
python .\scripts\seed_program_outcomes.py
\<repo-root>\backend\scripts\run_seed_internships.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (new shell)
cd <repo-root>\frontend
npm install
npm run dev
```

---

If you want, I can now:
- Add `backend/.env.example` and add `backend/.env` to `.gitignore` (recommended).
- Make the Philippines filter stricter (match canonical city list and country fields).
- Create a small `verify_db_connection.py` script you can run locally to test DB connectivity.

End of guide.
   - Update connection string in `.env` file

2. **Add Web Scraping**
   - Implement scraper in `backend/app/api/scraper.py`
   - Populate internships from career websites

3. **Improve Matching Algorithm**
   - Train ranker model in `backend/scripts/train_ranker.py`
   - Use embeddings for semantic matching

4. **Add User Accounts**
   - Implement authentication (JWT tokens)
   - Save user profiles and saved internships

5. **Deploy to Production**
   - Backend: Deploy to Heroku, AWS, or your server
   - Frontend: Deploy to Vercel, Netlify, or AWS S3

---

## Support
For issues or questions, check the logs:
- Backend: Terminal where `uvicorn` is running
- Frontend: Browser console (F12)
- Database: Check `backend/app/db.py` for log output
