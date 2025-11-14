# ✅ Your RapidAPI Configuration is Ready!

## Configuration Summary
Your `backend/.env` has been set up with:

```
RAPID_API_KEY=61d2bbe17cmshf9c0f78736a491?p128608jsn0416f849ea82
RAPID_API_HOST=internships-api.p.rapidapi.com
DATABASE_URL=postgresql://postgres:password@localhost:5432/internshipdb
```

## Next Steps: Run Your Application

### Terminal 1: Start the Backend
```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start the Frontend
```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\frontend
npm install
npm run dev
```

Expected output:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

## Test Your Setup (once both are running)

### Test 1: Health Check
```powershell
curl.exe http://localhost:8000/api/health
```
Expected: `{"status":"ok","message":"Frontend API is running"}`

### Test 2: RapidAPI Scraper
```powershell
curl.exe "http://localhost:8000/scrape/internships?query=internship&limit=5"
```
Expected: JSON with internship listings

### Test 3: Open Frontend
Open browser: **http://localhost:5173**

You should see:
- ✅ "Upload Your Resume" card with upload area
- ✅ Professional purple/indigo styled UI
- ✅ File upload button (drag & drop enabled)

## Complete Flow to Test

1. **Upload Resume**
   - Click "Choose File" or drag-drop a PDF/DOC/DOCX
   - Sample file: `C:\Users\ACER\Downloads\ai-internship-matcher\sample_resume.txt`
   - Click "Upload & Find Internships"

2. **Backend Processing**
   - Extracts skills from resume
   - Triggers RapidAPI scraper to fetch internships
   - Saves to PostgreSQL database
   - Returns resume_id

3. **View Recommendations**
   - Automatically redirects to Recommendations page
   - Fetches `/api/get-recommendations?resumeId=<id>`
   - Shows matched internships with:
     - Match score (0-100%)
     - Company name & location
     - Matched skills
     - Apply link

## Database Setup (Optional for Production)

If you want to use PostgreSQL instead of SQLite:

```powershell
# Install PostgreSQL locally or use a cloud instance
# Update .env DATABASE_URL to your actual PostgreSQL connection:
# DATABASE_URL=postgresql://user:password@localhost:5432/internshipdb

# Then run migration (if needed):
# python scripts/seed_internships.py
```

## Troubleshooting

### Backend fails to start
- Check Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is available: `netstat -ano | findstr :8000`

### Frontend fails to start
- Check Node.js: `node --version` & `npm --version`
- Clear cache: `Remove-Item -Recurse node_modules`
- Reinstall: `npm install`

### RapidAPI returns no results
- Verify API key is correct in `.env`
- Confirm you're subscribed to the Internships API on RapidAPI
- Try different query: `?query=graduate&limit=10`
- Check RapidAPI free tier limits

### File upload fails
- Ensure backend is running
- Check browser console for error messages
- Try with sample_resume.txt first
- Verify file is PDF/DOC/DOCX

## File Structure
```
ai-internship-matcher/
├── backend/
│   ├── .env                    ✅ Created with your RapidAPI key
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── frontend_api.py
│   │   │   ├── scraper.py
│   │   │   └── ...
│   │   └── ...
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadResume.vue
│   │   │   └── Recommendations.vue
│   │   └── router/
│   │       └── index.js
│   └── package.json
└── sample_resume.txt
```

## Success Indicators

✅ Backend running at http://localhost:8000
✅ Frontend running at http://localhost:5173
✅ Can upload resume file
✅ Can see internship recommendations
✅ Match scores show skill overlap
✅ RapidAPI data is being fetched

---

**You're all set!** 🚀 Your AI Internship Matcher is ready to use.

Start both servers and begin uploading resumes to match with AI internships!
