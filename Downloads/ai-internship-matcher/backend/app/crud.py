from sqlalchemy.orm import Session
from . import models
from datetime import datetime

def create_student(db: Session, name:str, email:str, program:str, gpa:float=None, protected_age:int=None):
    s = models.Student(name=name, email=email, program=program, gpa=gpa, protected_age=protected_age)
    db.add(s); db.commit(); db.refresh(s)
    return s

def get_student(db: Session, student_id:int):
    return db.query(models.Student).filter(models.Student.id==student_id).first()

def list_students(db: Session, skip:int=0, limit:int=100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_resume(db: Session, student_id:int, filename:str, parsed_text:str, skills:str, outcomes:str, embedding_path:str):
    r = models.Resume(student_id=student_id, filename=filename, parsed_text=parsed_text, skills=skills, outcomes=outcomes, embedding=embedding_path)
    db.add(r); db.commit(); db.refresh(r)
    return r

def create_department(db: Session, name:str, program_focus:str, description:str, required_skills:str, embedding_path:str=None):
    d = models.InternshipDepartment(name=name, program_focus=program_focus, description=description, required_skills=required_skills, embedding=embedding_path)
    db.add(d); db.commit(); db.refresh(d)
    return d

def get_all_departments(db: Session):
    return db.query(models.InternshipDepartment).all()

def create_recommendation(db: Session, student_id:int, department_id:int, score:float, reason:str):
    rec = models.Recommendation(student_id=student_id, department_id=department_id, score=score, reason=reason, created_at=datetime.utcnow())
    db.add(rec); db.commit(); db.refresh(rec)
    return rec
