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
- PostgreSQL (or SQLite for development)
- pip and npm package managers

---

## Backend Setup

### 1. Install Backend Dependencies
```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\backend
pip install -r requirements.txt
```

### 2. Set Up Database
The database is automatically created when you run the backend. To seed it with sample internships:

```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\backend
python scripts/seed_internships.py
```

This populates the database with 12 sample AI internship listings from major tech companies.

Before running the backend, copy the example env file and update credentials:

```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\backend
copy .env.example .env
# then edit .env to set DATABASE_URL and any API keys
```

### 3. Run the Backend
```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at: `http://localhost:8000`

**Available Endpoints:**
- `POST /api/upload-resume` - Upload a resume file
- `GET /api/get-recommendations` - Get internship recommendations based on resume
- `GET /api/health` - Health check endpoint
- `POST /upload/resume/{student_id}` - Original upload endpoint (legacy)
- `GET /recommend/student/{student_id}` - Original recommendations endpoint (legacy)

---

## Frontend Setup

### 1. Install Frontend Dependencies
```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\frontend
npm install
npm install vue-router@4
```

### 2. Run Development Server
```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\frontend
npm run dev
```

The frontend will start at: `http://localhost:5173` (or similar Vite port)

---

## Testing the Full Flow

### 1. Upload a Resume
1. Open frontend at `http://localhost:5173`
2. Click "Upload Your Resume"
3. Select the sample resume: `C:\Users\ACER\Downloads\ai-internship-matcher\sample_resume.txt`
4. Or drag and drop a PDF/DOC/DOCX file
5. Click "Upload & Find Internships"

### 2. View Recommendations
After upload, you'll see a list of matched AI internships with:
- Match percentage based on skill overlap
- Company name and location
- Job description
- Matched skills from your resume
- Link to apply

### 3. Sample Skills Extracted from Resume
The sample resume contains these AI/ML skills:
- Python
- TensorFlow
- PyTorch
- Deep Learning
- Machine Learning
- Neural Networks
- Data Analysis
- NLP
- Computer Vision
- SQL
- Scikit-learn
- And more...

These will be matched against internship requirements to generate recommendations.

---

## API Request/Response Examples

### Upload Resume
```bash
POST /api/upload-resume
Content-Type: multipart/form-data

{
  "file": <binary resume file>
}

Response:
{
  "status": "ok",
  "resume_id": 1,
  "extracted_skills": ["Python", "TensorFlow", "Deep Learning", ...]
}
```

### Get Recommendations
```bash
GET /api/get-recommendations?resume_id=1

Response:
[
  {
    "id": 1,
    "title": "Machine Learning Engineering Intern",
    "company_name": "Google AI",
    "location": "Mountain View, CA",
    "description": "Work on cutting-edge ML models...",
    "posting_url": "https://careers.google.com/...",
    "matched_skills": ["Python", "TensorFlow", "Deep Learning"],
    "match_score": 85,
    "posted_date": "2025-11-07T10:30:00"
  },
  ...
]
```

---

## Project Structure

```
ai-internship-matcher/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── frontend_api.py    # NEW: Frontend endpoints
│   │   │   ├── uploads.py          # Resume upload
│   │   │   ├── recommendations.py  # Recommendations
│   │   │   └── scraper.py          # Web scraping
│   │   ├── models.py               # Database models (Internship, Resume, etc)
│   │   ├── crud.py                 # Database operations
│   │   ├── db.py                   # Database setup
│   │   ├── main.py                 # FastAPI app
│   │   ├── nlp/
│   │   │   ├── parser.py           # Resume parsing
│   │   │   ├── embedding.py        # Text embeddings
│   │   │   └── ranker.py           # ML ranking
│   │   └── llm/
│   │       └── llm_client.py       # LLM integration
│   ├── scripts/
│   │   ├── seed_internships.py     # NEW: Populate DB with sample data
│   │   └── seed_db.py              # Original seed script
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadResume.vue    # Resume upload (Vue 3)
│   │   │   └── Recommendations.vue # Results display (Vue 3)
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css               # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.cjs
│
└── sample_resume.txt               # NEW: Example resume for testing
```

---

## Troubleshooting

### Backend Issues

**Error: "Port 8000 already in use"**
```powershell
# Change the port:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Error: Database connection failed**
- Ensure PostgreSQL is running (or using SQLite)
- Check `backend/app/db.py` for connection string

**Error: Resume parsing fails**
- Install required PDF parsing libraries: `pip install pdf2image pytesseract pdfminer.six`
- Ensure uploaded file is valid PDF/DOC/DOCX

### Frontend Issues

**Error: "vue-router" module not found**
```powershell
npm install vue-router@4
npm run dev
```

**Error: CORS errors from backend**
- Backend already has CORS enabled in `main.py`
- Ensure both frontend and backend are running
- Check browser console for actual error message

**Styling issues (white page)**
- Run `npm run dev` to rebuild with Tailwind/PostCSS
- Check browser DevTools for CSS file load status

---

## Next Steps

1. **Connect to Real Database**
   - Update `backend/app/db.py` to use PostgreSQL instead of SQLite
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
