"""
Database seeding script for AI Internship Matcher.
Creates realistic AI internship listings, sample resumes, and initial recommendations.
"""

import os
import sys
from datetime import datetime, timedelta
import random
from pathlib import Path
from typing import List, Dict

# Add the parent directory to the path so we can import app
base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir))

from app.db import SessionLocal, engine
from app.models import Base, Internship, Resume, Skill, User, Match
from app.nlp.embedding import embed_text, save_embedding, cosine_similarity
from scripts.seed_data import COMPANIES, AI_SKILLS, INTERNSHIP_TEMPLATES, SAMPLE_RESUMES

def generate_internship_description(template: dict, company: dict, skills: List[str]) -> Dict:
    """Generate a realistic internship posting from a template."""
    today = datetime.now()
    description = template["description"].format(
        company=company["name"],
        skills=", ".join(skills[:3]),
        additional_skills=", ".join(skills[3:]),
        location=random.choice(company["locations"])
    )
    
    return {
        "title": template["title"],
        "company_name": company["name"],
        "location": random.choice(company["locations"]),
        "description": description,
        "required_skills": skills,
        "posting_date": today - timedelta(days=random.randint(0, 14)),
        "is_active": True,
        "salary_range": f"${random.randint(20, 50)}k - ${random.randint(51, 80)}k",
        "application_url": f"https://careers.{company['name'].lower().replace(' ', '')}.com/intern",
        "employment_type": "Internship",
        "duration": f"{random.randint(3, 6)} months"
    }

def seed_database():
    """Seed the database with realistic AI internship data and sample resumes."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(Match).delete()
        db.query(Resume).delete()
        db.query(Internship).delete()
        db.query(Skill).delete()
        db.query(User).delete()
        db.commit()
        
        # Seed skills first
        print("\nSeeding AI skills...")
        skills_dict = {}
        for skill_name in AI_SKILLS:
            skill = Skill(name=skill_name)
            db.add(skill)
            skills_dict[skill_name] = skill
        db.commit()
        print(f"Added {len(skills_dict)} skills")
    
        print("\nSeeding students...")
        students = []
        for student_data in STUDENTS:
            student = Student(**student_data)
            db.add(student)
            students.append(student)
        db.commit()
        print(f"Added {len(students)} students")
    
        print("\nCreating sample resume...")
        # Create resume for first student (Alex Chen)
        resume = Resume(
            student_id=students[0].id,
            filename="alex_chen_resume.pdf",
            parsed_text=SAMPLE_RESUME_TEXT,
            skills="python,pytorch,tensorflow,machine learning,docker,git",
            outcomes="ml research,sentiment analysis,object detection",
            created_at=datetime.utcnow()
        )
        db.add(resume)
        db.commit()
    
        # Create embedding for resume
        resume_embedding = embed_text(f"{resume.parsed_text} {resume.skills} {resume.outcomes}")
        resume.embedding = save_embedding(resume.id, resume_embedding, prefix="resume")
        db.add(resume)
        db.commit()
    
        print("\nGenerating recommendations...")
        # Create some sample recommendations
        for dept in departments[:3]:  # Top 3 matches for Alex
            score = 0.0
            if "machine learning" in dept.required_skills:
                score += 0.3
            if "python" in dept.required_skills:
                score += 0.2
            if any(skill in dept.required_skills for skill in ["pytorch", "tensorflow"]):
                score += 0.3
            if "deep learning" in dept.required_skills:
                score += 0.2
            
            recommendation = Recommendation(
                student_id=students[0].id,
                department_id=dept.id,
                score=min(score + 0.1, 1.0),  # Normalize to 0-1
                reason=f"Skills match: {', '.join(set(dept.required_skills.split(',')) & set(resume.skills.split(',')))}"
            )
            db.add(recommendation)
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == '__main__':
    seed()
