Backend instructions:
- Create PostgreSQL DB and set `DATABASE_URL` env var (or use `backend/.env`).
- Install dependencies from `requirements.txt`.
- Run the API via uvicorn: `uvicorn app.main:app --reload --port 8000`
- RapidAPI requirement: This project sources internships using the RapidAPI Internships API.
	- Add `RAPID_API_KEY` and `RAPID_API_HOST` to `backend/.env` or your environment.
	- Example (PowerShell):
		```powershell
		$env:RAPID_API_KEY = 'your-rapidapi-key'
		$env:RAPID_API_HOST = 'internships-api.p.rapidapi.com'
		```
- Seed internships (Philippines-focused) using the scraper-backed seeder:
	```powershell
	cd backend
	python .\scripts\seed_internships.py
	```
- Seed program outcomes (Philippine-focused) if needed:
	```powershell
	python .\scripts\seed_program_outcomes.py
	```
- Train ranker (optional): `python backend/scripts/train_ranker.py`
