from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime
try:
    # optional: use pgvector for efficient vector storage/search in Postgres
    from pgvector.sqlalchemy import Vector
except Exception:
    Vector = None

class Program(Base):
    """University AI/ML Programs"""
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g., "Computer Science", "Data Science"
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    outcomes = relationship("ProgramOutcome", back_populates="program")
    students = relationship("Student", back_populates="program_rel")

class ProgramOutcome(Base):
    """Learning outcomes/career paths for each program"""
    __tablename__ = "program_outcomes"
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    outcome_name = Column(String, nullable=False)  # e.g., "AI Research", "ML Engineering", "Data Science"
    outcome_description = Column(Text)
    related_skills = Column(Text)  # comma-separated skills for this outcome
    internship_keywords = Column(Text)  # keywords to match with internships (e.g., "research, papers, algorithm")
    created_at = Column(DateTime, default=datetime.utcnow)
    program = relationship("Program", back_populates="outcomes")
    student_outcomes = relationship("StudentOutcome", back_populates="outcome")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)
    gpa = Column(Float)
    protected_age = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resumes = relationship("Resume", back_populates="student")
    recommendations = relationship("Recommendation", back_populates="student")
    student_outcomes = relationship("StudentOutcome", back_populates="student")
    program_rel = relationship("Program", back_populates="students")

class StudentOutcome(Base):
    """Student's selected career outcomes/goals"""
    __tablename__ = "student_outcomes"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    outcome_id = Column(Integer, ForeignKey("program_outcomes.id"), nullable=False)
    is_primary = Column(Boolean, default=False)  # Main career goal
    proficiency_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    created_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="student_outcomes")
    outcome = relationship("ProgramOutcome", back_populates="student_outcomes")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    filename = Column(String)
    parsed_text = Column(Text)
    skills = Column(Text)  # comma-separated extracted skills
    outcomes = Column(Text)  # comma-separated detected outcomes from resume
    created_at = Column(DateTime, default=datetime.utcnow)
    # embedding: store as pgvector when available, otherwise store as text path or JSON
    if Vector is not None:
        embedding = Column(Vector(384))
    else:
        embedding = Column(Text)
    student = relationship("Student", back_populates="resumes")

class InternshipDepartment(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    program_focus = Column(String)
    description = Column(Text)
    required_skills = Column(Text)
    if Vector is not None:
        embedding = Column(Vector(384))
    else:
        embedding = Column(Text)

class Internship(Base):
    __tablename__ = "internships"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    location = Column(String)
    description = Column(Text)
    required_skills = Column(Text)  # comma-separated
    outcome_focus = Column(String)  # which outcome this internalizes fits (AI Research, ML Engineering, etc.)
    posting_url = Column(String)
    posted_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)
    source = Column(String)  # where it was scraped from (rapidapi, jobstreet, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)
    # optional vector field for semantic search (requires pgvector in DB)
    if Vector is not None:
        embedding = Column(Vector(384))
    else:
        embedding = Column(Text)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    outcome_match = Column(String)  # which outcome this matches (AI Research, etc.)
    score = Column(Float)  # overall match score (0-100)
    skill_match_score = Column(Float)  # skill overlap %
    outcome_match_score = Column(Float)  # outcome alignment %
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="recommendations")

