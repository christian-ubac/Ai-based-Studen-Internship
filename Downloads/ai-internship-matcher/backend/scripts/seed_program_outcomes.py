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
        "name": "Artificial Intelligence",
        "description": "Study of intelligent systems, machine learning, and AI algorithms",
        "outcomes": [
            {
                "outcome_name": "AI Research",
                "outcome_description": "Conduct cutting-edge AI research, publish papers, develop novel algorithms",
                "related_skills": "python,pytorch,tensorflow,research,algorithms,deep learning,neural networks,papers",
                "internship_keywords": "research,papers,algorithm,novel,experiment,publication,academic"
            },
            {
                "outcome_name": "AI Engineering",
                "outcome_description": "Build production AI systems, deploy models, optimize performance",
                "related_skills": "python,fastapi,deployment,docker,kubernetes,mlops,ci/cd,monitoring",
                "internship_keywords": "production,deployment,engineer,system,optimization,scale"
            },
            {
                "outcome_name": "Machine Learning",
                "outcome_description": "Develop ML models, feature engineering, model training and evaluation",
                "related_skills": "python,scikit-learn,pandas,numpy,data analysis,feature engineering,models",
                "internship_keywords": "machine learning,ml,models,training,features,data science"
            }
        ]
    },
    {
        "name": "Data Science",
        "description": "Analysis of data, statistical modeling, and business intelligence",
        "outcomes": [
            {
                "outcome_name": "Data Analysis",
                "outcome_description": "Analyze large datasets, extract insights, create visualizations",
                "related_skills": "python,pandas,sql,tableau,power bi,statistics,visualization,analysis",
                "internship_keywords": "analysis,data,insights,analytics,visualization,dashboard,sql"
            },
            {
                "outcome_name": "Data Science",
                "outcome_description": "Build predictive models using data science techniques",
                "related_skills": "python,scikit-learn,statistical analysis,modeling,prediction,machine learning",
                "internship_keywords": "data science,predictive,model,analytics,science"
            },
            {
                "outcome_name": "Business Intelligence",
                "outcome_description": "Transform data into actionable business insights",
                "related_skills": "sql,tableau,power bi,analytics,business,reporting,dashboard",
                "internship_keywords": "business,intelligence,analytics,insights,reporting,bi"
            }
        ]
    },
    {
        "name": "Computer Science",
        "description": "General computer science with applications in AI/ML",
        "outcomes": [
            {
                "outcome_name": "Software Development",
                "outcome_description": "Develop software applications, write clean code, build systems",
                "related_skills": "python,java,c++,software development,design patterns,testing,git",
                "internship_keywords": "software,development,engineer,code,application,build"
            },
            {
                "outcome_name": "Natural Language Processing",
                "outcome_description": "Work on NLP tasks: sentiment analysis, translation, generation",
                "related_skills": "python,nltk,spacy,transformers,bert,nlp,text processing,nlp",
                "internship_keywords": "nlp,language,text,nlp,nlp,generation,sentiment,translation"
            },
            {
                "outcome_name": "Computer Vision",
                "outcome_description": "Build vision systems: image classification, object detection, segmentation",
                "related_skills": "python,opencv,pytorch,cnn,computer vision,image,deep learning",
                "internship_keywords": "computer vision,vision,image,object detection,segmentation,cv"
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
