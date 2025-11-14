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


def seed_from_static(db):
    """Fallback static internships used when RapidAPI credentials are not available."""
    INTERNSHIPS = [
        {
            "title": "Machine Learning Engineering Intern",
            "company_name": "Google AI",
            "location": "Mountain View, CA",
            "description": "Work on cutting-edge machine learning models and contribute to Google's AI research initiatives.",
            "required_skills": "Python,TensorFlow,PyTorch,Deep Learning,Neural Networks",
            "posting_url": "https://careers.google.com/jobs/ml-intern",
            "posted_date": datetime.now() - timedelta(days=5)
        },
        {
            "title": "Data Science Intern",
            "company_name": "Microsoft Research",
            "location": "Redmond, WA",
            "description": "Analyze large datasets and build predictive models for Azure cloud services.",
            "required_skills": "Python,SQL,Data Analysis,Statistics,Machine Learning",
            "posting_url": "https://careers.microsoft.com/jobs/ds-intern",
            "posted_date": datetime.now() - timedelta(days=3)
        },
        # ... keep a small curated set (can be extended)
    ]

    inserted = 0
    for data in INTERNSHIPS:
        exists = db.query(models.Internship).filter(
            models.Internship.title == data["title"],
            models.Internship.company_name == data["company_name"]
        ).first()
        if exists:
            continue
        internship = models.Internship(
            title=data["title"],
            company_name=data["company_name"],
            location=data.get("location", ""),
            description=data.get("description", ""),
            required_skills=data.get("required_skills", ""),
            posting_url=data.get("posting_url", ""),
            posted_date=data.get("posted_date"),
            is_active=1,
            source="seed_static"
        )
        db.add(internship)
        inserted += 1
    db.commit()
    return inserted


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
    for item in internships_list:
        title = item.get("title") or item.get("job_title") or ""
        company = item.get("company") or item.get("company_name") or ""
        location = item.get("location") or item.get("city") or ""
        description = item.get("description") or item.get("summary") or ""
        posting_url = item.get("url") or item.get("link") or ""
        posted_date_str = item.get("posted_date") or item.get("date") or None

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
    return inserted


def seed_database(use_rapidapi=True, query="internship", limit=50):
    """Main entry: create tables and seed internships either from RapidAPI or static data."""
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(models.Internship).count()
        if existing > 0:
            print(f"Database already has {existing} internships. Skipping seed.")
            return

        inserted = 0
        if use_rapidapi:
            try:
                print("Seeding from RapidAPI...")
                inserted = seed_from_rapidapi(db, query=query, limit=limit)
                print(f"Inserted {inserted} internships from RapidAPI.")
            except Exception as e:
                print(f"RapidAPI seeding failed: {e}. Falling back to static seed.")
                inserted = seed_from_static(db)
                print(f"Inserted {inserted} internships from static list.")
        else:
            print("Seeding from static list...")
            inserted = seed_from_static(db)
            print(f"Inserted {inserted} internships from static list.")

    finally:
        db.close()


if __name__ == "__main__":
    # Decide whether to use RapidAPI by checking settings
    use_rapidapi = bool(getattr(settings, "RAPID_API_KEY", None))
    print("Starting database seed... (using RapidAPI:", use_rapidapi, ")")
    seed_database(use_rapidapi=use_rapidapi, query="internship", limit=50)
    print("Done!")
