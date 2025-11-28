#!/usr/bin/env python
"""
Seed database with sample AI internship data for testing and demonstration.
Run this script to populate the database with realistic internship listings.
"""

import sys
import os
import time
from datetime import datetime, timedelta
import random
import requests

# Add parent dir to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import SessionLocal, engine
from app import models
from app.config import settings
from app.nlp.parser import extract_skills_from_text


# Note: The project should rely on the RapidAPI scraper for internships.
# We intentionally do not include a local/static seed list. This enforces
# that internships are populated by web scraping (RapidAPI) only.


def seed_from_rapidapi(db, query="internship", limit=50):
    """Fetch internships from RapidAPI and persist to the database."""
    key = getattr(settings, "RAPID_API_KEY", None)
    host = getattr(settings, "RAPID_API_HOST", None)
    if not key or not host:
        raise RuntimeError("RapidAPI key/host not configured in settings/.env")

    url = f"https://{host}/search"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": host
    }
    params = {"keyword": query, "limit": min(limit, 50)}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        raise RuntimeError(f"RapidAPI request failed: {e}")

    internships_list = data.get("jobs", data.get("results", data.get("data", [])))
    if not isinstance(internships_list, list):
        internships_list = []

    inserted = 0
    skipped_non_ph = 0
    # Philippine location keywords (lowercase) to enforce local-only insertions
    PH_LOCATIONS = [
        "philippin", "philippines", "manila", "metro manila", "quezon city", "quezon",
        "makati", "cebu", "davao", "iloilo", "bacolod", "baguio", "cagayan",
        "zamboanga", "pasig", "muntinlupa", "taguig", "las piñas", "valenzuela",
        "laguna", "batangas", "cebu city", "cebu",
        "visayas", "mindanao", "luzon", "butuan"
    ]
    for item in internships_list:
        title = item.get("title") or item.get("job_title") or ""
        company = item.get("company") or item.get("company_name") or ""
        location = item.get("location") or item.get("city") or ""
        description = item.get("description") or item.get("summary") or ""
        posting_url = item.get("url") or item.get("link") or ""
        posted_date_str = item.get("posted_date") or item.get("date") or None

        # Enforce Philippines-only postings: check location or posting_url for PH hints
        loc_text = (location or "" ).lower()
        url_text = (posting_url or "").lower()
        is_ph = any(k in loc_text for k in PH_LOCATIONS) or any(k in url_text for k in [".ph", "philippines"]) 
        if not is_ph:
            skipped_non_ph += 1
            continue

        # Basic dedupe
        exists = db.query(models.Internship).filter(
            models.Internship.title == title,
            models.Internship.company_name == company
        ).first()
        if exists:
            continue

        # Extract skills using NLP helper
        try:
            skills = extract_skills_from_text(description)
            if item.get("skills"):
                api_skills = item.get("skills")
                if isinstance(api_skills, list):
                    skills.extend(api_skills)
                elif isinstance(api_skills, str):
                    skills.extend([s.strip() for s in api_skills.split(",")])
            skills = list(dict.fromkeys([s for s in skills if s]))
        except Exception:
            skills = []

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
        inserted += 1

    db.commit()
    if skipped_non_ph:
        print(f"Skipped {skipped_non_ph} non-Philippine internship(s)")
    return inserted


def seed_database(query="internship philippines", limit=50):
    """Main entry: create tables and seed internships from RapidAPI scraper.

    This function requires `RAPID_API_KEY` and `RAPID_API_HOST` to be set in
    `backend/.env` (or environment). It will only use the RapidAPI source and
    will not fall back to local static seed data.
    """
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(models.Internship).count()
        if existing > 0:
            print(f"Database already has {existing} internships. Skipping seed.")
            return

        print("Seeding from RapidAPI (Philippines-focused)...")
        inserted = seed_from_rapidapi(db, query=query, limit=limit)
        print(f"Inserted {inserted} internships from RapidAPI.")

    finally:
        db.close()


if __name__ == "__main__":
    # Decide whether to use RapidAPI by checking settings
    use_rapidapi = bool(getattr(settings, "RAPID_API_KEY", None))
    print("Starting database seed... (using RapidAPI:", use_rapidapi, ")")
    seed_database(use_rapidapi=use_rapidapi, query="internship", limit=50)
    print("Done!")
