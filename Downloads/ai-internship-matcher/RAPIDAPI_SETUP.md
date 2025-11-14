# RapidAPI Internships Integration Setup

## Overview
The scraper now supports fetching internship data from **RapidAPI Internships API**, providing real, structured internship listings with company info, locations, and requirements.

## Steps to Enable RapidAPI

### 1. Sign Up for RapidAPI
1. Go to [RapidAPI.com](https://rapidapi.com)
2. Sign up for a free account
3. Search for "Internships API" or "Job Board API" 
4. Subscribe to the API (free tier usually available)

### 2. Get Your API Credentials
1. In RapidAPI dashboard, go to your subscribed API
2. Copy your **X-RapidAPI-Key** (your API key)
3. Note the **X-RapidAPI-Host** value (usually provided in the API documentation)

### 3. Configure Your Backend
1. Open `backend/.env` and add your credentials:
   ```
   RAPID_API_KEY=your_api_key_here
   RAPID_API_HOST=internships-api.p.rapidapi.com
   ```
   (Replace with actual values from RapidAPI)

2. Ensure `backend/requirements.txt` includes `requests` (it should)

### 4. Use the RapidAPI Scraper

**Option A: Via HTTP (from browser or curl)**
```bash
# Trigger RapidAPI scraper with default settings
curl "http://localhost:8000/scrape/rapidapi-internships?query=internship&limit=20"

# Or from PowerShell
curl.exe "http://localhost:8000/scrape/rapidapi-internships?query=ai&limit=25"
```

**Option B: From the Frontend**
Currently the frontend triggers the JobStreet scraper. To use RapidAPI instead:
1. Edit `frontend/src/components/UploadResume.vue` 
2. Change the fetch URL from:
   ```javascript
   await fetch('/scrape/jobstreet?pages=1');
   ```
   to:
   ```javascript
   await fetch('/scrape/rapidapi-internships?query=internship&limit=20');
   ```

### 5. What Data You'll Get
Each scraped internship will have:
- **Title** – Job position (e.g., "Machine Learning Intern")
- **Company** – Company name (e.g., "Google", "Meta")
- **Location** – City/region
- **Description** – Full job description
- **Required Skills** – Extracted from description + API fields (Python, TensorFlow, etc.)
- **Posting URL** – Link to apply
- **Posted Date** – When the internship was posted
- **Source** – Marked as "rapidapi"

### 6. Database Storage
All scraped internships are saved to the `internships` table in PostgreSQL:
- Automatic deduplication (no duplicates by title + company)
- Skills stored as comma-separated list
- Used by recommendations endpoint to match with resume

## Example Response
```json
{
  "source": "RapidAPI Internships",
  "count": 20,
  "inserted": 18,
  "items": [
    {
      "title": "Machine Learning Engineering Intern",
      "company": "Google AI",
      "location": "Mountain View, CA",
      "saved": true,
      "skills": ["Python", "TensorFlow", "Deep Learning", "PyTorch"]
    },
    {
      "title": "NLP Research Intern",
      "company": "Meta AI",
      "location": "Menlo Park, CA",
      "saved": true,
      "skills": ["Python", "BERT", "NLP", "Transformers"]
    }
    ...
  ]
}
```

## Troubleshooting

### "RAPID_API_KEY not configured"
- Ensure you've added `RAPID_API_KEY` to `backend/.env`
- Restart the backend server after editing `.env`
- Check that the key is not empty

### "RapidAPI request failed"
- Verify your API key is correct (copy from RapidAPI dashboard)
- Check that you're subscribed to the API
- Ensure your RapidAPI account has available API calls
- Check network connectivity

### No internships returned
- Try different query keywords: `"internship"`, `"graduate program"`, `"entry level"`
- Increase the `limit` parameter (up to 50)
- Check RapidAPI API response format to ensure field names match

### Skills not extracted
- The NLP parser has a predefined skill vocabulary. If a skill isn't recognized:
  - Add it to `SKILL_VOCAB` in `backend/app/nlp/parser.py`
  - Or use OpenAI API to extract skills (set `OPENAI_API_KEY` in `.env`)

## Free Tier Limits
Most RapidAPI internship APIs have:
- 100-500 free requests per month
- Rate limits (e.g., 10 requests/minute)
- Limited number of results per request

Plan your scraping accordingly. For production:
- Consider upgrading to a paid tier
- Cache results in your database
- Scrape periodically (e.g., daily or weekly) rather than on every upload

## Next Steps
1. Set up your RapidAPI account and get credentials
2. Update `.env` with your API key
3. Test with: `curl "http://localhost:8000/scrape/rapidapi-internships?query=internship&limit=10"`
4. Verify internships appear in the database
5. (Optional) Update the frontend to use the RapidAPI scraper

## Alternative Approach: Combine Both Scrapers
You can also use both JobStreet and RapidAPI:
- JobStreet for local listings
- RapidAPI for broader/international listings
- The database deduplicates, so you get a comprehensive internship database

