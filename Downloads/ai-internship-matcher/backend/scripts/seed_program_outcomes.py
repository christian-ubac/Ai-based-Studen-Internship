#!/usr/bin/env python
"""
Seed program outcomes for AI/ML focused internship matcher.
Creates programs, learning outcomes, and links them for skill-outcome matching.
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import SessionLocal, engine
from app import models

# Define AI/ML programs and their outcomes
PROGRAMS_DATA = [
    {
        "name": "Bachelor of Science in Computer Science",
        "description": "Undergraduate program focusing on software development, algorithms, and applied AI for industry.",
        "outcomes": [
            {
                "outcome_name": "Software & Systems Development",
                "outcome_description": "Design and build software systems for local businesses and startups.",
                "related_skills": "python,java,javascript,git,rest api,database,testing,ci/cd",
                "internship_keywords": "software,development,backend,frontend,api,web,application"
            },
            {
                "outcome_name": "AI & Machine Learning",
                "outcome_description": "Apply machine learning methods to practical problems like recommendation and prediction.",
                "related_skills": "python,pytorch,tensorflow,scikit-learn,data analysis,mlops",
                "internship_keywords": "machine learning,ml,ai,recommendation,prediction,model"
            },
            {
                "outcome_name": "Natural Language Processing (Filipino)",
                "outcome_description": "Work on NLP systems with a focus on Filipino language resources and applications.",
                "related_skills": "python,spacy,transformers,nlp,text processing,tagging",
                "internship_keywords": "nlp,filipino,tagalog,language,chatbot,translation,analysis"
            }
        ]
    },
    {
        "name": "Bachelor of Science in Data Science",
        "description": "Program emphasizing statistical analysis, data engineering, and business analytics relevant to PH industries.",
        "outcomes": [
            {
                "outcome_name": "Data Analytics for Business",
                "outcome_description": "Extract insights from data to support decision-making in sectors like retail, finance, and government.",
                "related_skills": "python,pandas,sql,tableau,visualization,statistics",
                "internship_keywords": "analytics,data analysis,insights,visualization,sql"
            },
            {
                "outcome_name": "Applied Machine Learning",
                "outcome_description": "Deploy ML solutions for local problems such as traffic, agriculture, and health.",
                "related_skills": "python,scikit-learn,modeling,feature engineering,deployment",
                "internship_keywords": "deployment,model,ml,prediction,agriculture,health"
            }
        ]
    },
    {
        "name": "Bachelor of Science in Electronics and Communications Engineering",
        "description": "Engineering program with applications to embedded AI, IoT, and telecommunications in the Philippines.",
        "outcomes": [
            {
                "outcome_name": "Embedded AI & IoT",
                "outcome_description": "Design edge-AI and IoT solutions for smart agriculture, smart cities, and industry.",
                "related_skills": "c++,python,embedded systems,iot,raspberry pi,microcontrollers",
                "internship_keywords": "iot,embedded,edge ai,agriculture,smart city"
            },
            {
                "outcome_name": "Communications & Networking",
                "outcome_description": "Work on networking, telecommunication systems and connectivity solutions tailored for local infrastructure.",
                "related_skills": "networking,linux,protocols,wireless,telecom",
                "internship_keywords": "network,wireless,telecom,connectivity,5g"
            }
        ]
    }
]

def seed_programs():
    """Seed database with program outcomes"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing program data...")
        db.query(models.StudentOutcome).delete()
        db.query(models.ProgramOutcome).delete()
        db.query(models.Program).delete()
        db.commit()
        
        # Seed programs and outcomes
        print("\nSeeding program outcomes...")
        for program_data in PROGRAMS_DATA:
            program = models.Program(
                name=program_data["name"],
                description=program_data["description"]
            )
            db.add(program)
            db.flush()  # Get the program id
            
            print(f"\n✓ Program: {program.name}")
            
            for outcome_data in program_data["outcomes"]:
                outcome = models.ProgramOutcome(
                    program_id=program.id,
                    outcome_name=outcome_data["outcome_name"],
                    outcome_description=outcome_data["outcome_description"],
                    related_skills=outcome_data["related_skills"],
                    internship_keywords=outcome_data["internship_keywords"]
                )
                db.add(outcome)
                print(f"  └─ Outcome: {outcome.outcome_name}")
        
        db.commit()
        
        # Verify
        programs_count = db.query(models.Program).count()
        outcomes_count = db.query(models.ProgramOutcome).count()
        
        print(f"\n{'='*50}")
        print(f"✅ Seeding complete!")
        print(f"   Programs created: {programs_count}")
        print(f"   Outcomes created: {outcomes_count}")
        print(f"{'='*50}\n")
        
    except Exception as e:
        print(f"❌ Error seeding programs: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def seed_example_student_outcomes():
    """Optional: Add example student-outcome relationships"""
    db = SessionLocal()
    
    try:
        # Get or create a student
        student = db.query(models.Student).first()
        if not student:
            # Create a test student
            ai_program = db.query(models.Program).filter_by(name="Artificial Intelligence").first()
            student = models.Student(
                name="Test Student",
                email="test@university.edu",
                program_id=ai_program.id if ai_program else None,
                gpa=3.8
            )
            db.add(student)
            db.flush()
        
        # Add student outcomes
        ai_research = db.query(models.ProgramOutcome).filter_by(outcome_name="AI Research").first()
        if ai_research and not db.query(models.StudentOutcome).filter_by(
            student_id=student.id, outcome_id=ai_research.id
        ).first():
            student_outcome = models.StudentOutcome(
                student_id=student.id,
                outcome_id=ai_research.id,
                is_primary=True,
                proficiency_level="intermediate"
            )
            db.add(student_outcome)
        
        db.commit()
        print("✅ Example student outcomes added!")
        
    except Exception as e:
        print(f"⚠️  Could not add example student outcomes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("✓ Tables created\n")
    
    # Seed programs and outcomes
    seed_programs()
    
    # Optional: add example student outcomes
    seed_example_student_outcomes()
    
    print("🎓 Program outcomes database ready!")
