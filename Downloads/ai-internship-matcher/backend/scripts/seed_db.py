"""
Database seeding script for AI Internship Matcher (fixed to match models).
Creates a few programs, students, internships, a resume and simple recommendations.
Run from the `backend` folder with the project's virtualenv active:

    python scripts/seed_db.py

This script uses the SQLAlchemy models defined in `app.models` and the
embedding helpers in `app.nlp.embedding`.
"""
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys
import os

# Ensure project root is importable
base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir))

from app.db import SessionLocal, engine
from app.models import Base, Student, Resume, Internship, InternshipDepartment, Recommendation, Program, ProgramOutcome
from app.nlp.embedding import embed_text, save_embedding

# Small sample data
AI_SKILLS = [
    "python", "pytorch", "tensorflow", "machine learning", "deep learning",
    "nlp", "computer vision", "data analysis", "docker", "git"
]

COMPANIES = [
    {"name": "OpenAI Labs", "locations": ["San Francisco, CA", "Remote"]},
    {"name": "DeepVision", "locations": ["New York, NY", "Remote"]},
    {"name": "DataWorks", "locations": ["Boston, MA", "Remote"]}
]

INTERNSHIP_TEMPLATES = [
    {"title": "Machine Learning Intern", "description": "{company} seeks an ML Intern to work on {skills}. Additional skills: {additional_skills}."},
    {"title": "NLP Research Intern", "description": "Join {company} to build NLP models for real-world tasks. Required: {skills}."},
    {"title": "Computer Vision Intern", "description": "Work on CV pipelines at {company}. Focus: {skills}."}
]

SAMPLE_RESUMES = [
    {
        "name": "Alex Chen",
        "email": "alex.chen@example.com",
        "gpa": 3.8,
        "skills": ["python", "pytorch", "docker", "git"],
        "outcomes": ["machine learning", "research"]
    }
]


def make_description(template, company, skills):
    return template["description"].format(
        company=company["name"],
        skills=", ".join(skills[:3]),
        additional_skills=", ".join(skills[3:])
    )


def seed_database():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Clear existing data conservatively
        print("Clearing existing internships, resumes, students, recommendations...")
        db.query(Recommendation).delete()
        db.query(Resume).delete()
        db.query(Internship).delete()
        db.query(InternshipDepartment).delete()
        db.query(ProgramOutcome).delete()
        db.query(Program).delete()
        db.query(Student).delete()
        db.commit()

        # Create a sample program and outcomes
        program = Program(name="Computer Science", description="CS program focusing on AI/ML")
        db.add(program)
        db.commit()

        outcome_ml = ProgramOutcome(program_id=program.id, outcome_name="Machine Learning", related_skills=",".join(["machine learning","deep learning","pytorch"]))
        outcome_ds = ProgramOutcome(program_id=program.id, outcome_name="Data Science", related_skills=",".join(["data analysis","sql","python"]))
        db.add_all([outcome_ml, outcome_ds])
        db.commit()

        # Seed students
        students = []
        for r in SAMPLE_RESUMES:
            s = Student(name=r["name"], email=r["email"], gpa=r["gpa"], program_id=program.id)
            db.add(s)
            students.append(s)
        db.commit()

        # Create internships
        internships = []
        for comp in COMPANIES:
            for tmpl in INTERNSHIP_TEMPLATES:
                skills = random.sample(AI_SKILLS, k=4)
                ins = Internship(
                    title=tmpl["title"],
                    company_name=comp["name"],
                    location=random.choice(comp["locations"]),
                    description=make_description(tmpl, comp, skills),
                    required_skills=",".join(skills),
                    outcome_focus=random.choice(["Machine Learning", "Data Science"]),
                    posting_url=f"https://careers.{comp['name'].lower().replace(' ', '')}.com/apply",
                    posted_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                    is_active=1,
                    source="seed"
                )
                db.add(ins)
                internships.append(ins)
        db.commit()

        # Create a resume for the first student
        student = students[0]
        resume_text = "\n".join([f"Worked on {s} projects" for s in SAMPLE_RESUMES[0]["skills"]])
        resume = Resume(
            student_id=student.id,
            filename=f"{student.name.replace(' ', '_').lower()}_resume.pdf",
            parsed_text=resume_text,
            skills=",".join(SAMPLE_RESUMES[0]["skills"]),
            outcomes=",".join(SAMPLE_RESUMES[0]["outcomes"]),
            created_at=datetime.utcnow()
        )
        db.add(resume)
        db.commit()

        # Create embedding for resume (if sentence-transformers available)
        try:
            emb = embed_text(resume.parsed_text + " " + resume.skills + " " + resume.outcomes)
            emb_path = save_embedding(resume.id, emb, prefix="resume")
            resume.embedding = emb_path
            db.add(resume)
            db.commit()
        except Exception as e:
            print("Warning: failed to create embedding (model may be missing):", e)
            db.rollback()

        # Generate simple recommendation scores by skill overlap
        print("Generating recommendations based on simple skill overlap...")
        for ins in internships:
            student_skills = set(resume.skills.split(","))
            ins_skills = set(ins.required_skills.split(",")) if ins.required_skills else set()
            overlap = len(student_skills.intersection(ins_skills))
            # Score 0-100
            score = min(100, 20 * overlap + random.randint(0, 20))
            rec = Recommendation(
                student_id=student.id,
                internship_id=ins.id,
                department_id=None,
                outcome_match=ins.outcome_focus,
                score=float(score),
                skill_match_score=float(min(100, 25 * overlap)),
                outcome_match_score=50.0 if ins.outcome_focus in resume.outcomes else 10.0,
                reason=f"Matched skills: {', '.join(student_skills.intersection(ins_skills))}" if overlap else "No direct skills matched"
            )
            db.add(rec)
        db.commit()

        print("Seeding complete: added", len(students), "student(s)", len(internships), "internships and recommendations.")

    except Exception as e:
        db.rollback()
        print("Error during seeding:", e)
        raise
    finally:
        db.close()


if __name__ == '__main__':
    seed_database()
