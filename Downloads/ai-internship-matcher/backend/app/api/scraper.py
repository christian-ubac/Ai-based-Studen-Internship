import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException
import time
from urllib.parse import urljoin
from ..config import settings
from ..db import get_db
from sqlalchemy.orm import Session
from .. import models
from ..nlp.parser import extract_skills_from_text
from ..utils.location import is_philippines_location

router = APIRouter(prefix="/scrape", tags=["scrape"])
HEADERS = {"User-Agent": "InternshipMatcherBot/0.1 (email@example.com)"}

# RapidAPI configuration for Internships API
RAPIDAPI_KEY = getattr(settings, "RAPID_API_KEY", "")
RAPIDAPI_HOST = getattr(settings, "RAPID_API_HOST", "internships-api.p.rapidapi.com")


@router.get("/internships")
def scrape_internships(query: str = "internship", limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch internship listings from RapidAPI Internships API (primary scraper).
    Requires RAPID_API_KEY and RAPID_API_HOST environment variables.
    Returns structured internship data with skills, locations, and company info.
    """
    if not RAPIDAPI_KEY:
        raise HTTPException(
            status_code=400,
            detail="RAPID_API_KEY not configured. Set it in .env file."
        )

    results = []
    inserted = 0

    url = f"https://{RAPIDAPI_HOST}/search"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {
        "keyword": query,
        "limit": min(limit, 50),  # API may have limits
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"RapidAPI request failed: {str(e)}")

    try:
        data = response.json()
        internships_list = data.get("jobs", data.get("results", data.get("data", [])))
        
        if not isinstance(internships_list, list):
            internships_list = []
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to parse RapidAPI response: {str(e)}")

    for item in internships_list:
        # Map RapidAPI fields to our model
        title = item.get("title") or item.get("job_title") or ""
        company = item.get("company") or item.get("company_name") or ""
        location = item.get("location") or item.get("city") or ""
        description = item.get("description") or item.get("summary") or ""
        posting_url = item.get("url") or item.get("link") or ""
        posted_date_str = item.get("posted_date") or item.get("date") or None
        
        # Extract required skills from description using NLP
        try:
            skills = extract_skills_from_text(description)
            # Also check for skills field in API response if available
            if item.get("skills"):
                api_skills = item.get("skills")
                if isinstance(api_skills, list):
                    skills.extend(api_skills)
                elif isinstance(api_skills, str):
                    skills.extend([s.strip() for s in api_skills.split(",")])
            skills = list(set(skills))  # dedupe
        except Exception:
            skills = []

        # Enforce Philippines-only postings: use stricter helper when possible
        country = item.get("country") or item.get("country_name") or None
        if not is_philippines_location(location, posting_url, description, country):
            results.append({"title": title, "company": company, "saved": False, "reason": "non-PH"})
            continue

        # Dedupe by title + company
        exists = db.query(models.Internship).filter(
            models.Internship.title == title,
            models.Internship.company_name == company
        ).first()
        if exists:
            results.append({"title": title, "company": company, "saved": False})
            continue

        internship = models.Internship(
            title=title or "Unknown",
            company_name=company or "Unknown",
            location=location,
            description=description,
            required_skills=",".join(skills) if skills else "",
            posting_url=posting_url,
            posted_date=posted_date_str,
            is_active=1,
            source="rapidapi"
        )
        db.add(internship)
        db.commit()
        inserted += 1
        results.append({
            "title": title,
            "company": company,
            "location": location,
            "saved": True,
            "skills": skills
        })

    return {
        "source": "RapidAPI Internships",
        "count": len(results),
        "inserted": inserted,
        "items": results
    }
