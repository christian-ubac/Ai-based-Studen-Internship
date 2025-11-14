# Program Outcomes Schema for AI Internship Matcher

## Overview

This database schema supports **outcome-based matching** for AI/ML student internships. It tracks student career goals (outcomes) and matches them with internship opportunities based on outcome focus.

---

## Database Schema

### 1. **Program** Table
Represents university AI/ML programs.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Program name (e.g., "Artificial Intelligence", "Data Science") |
| description | Text | Program description |
| created_at | DateTime | Creation timestamp |

**Example:**
```
Program: Artificial Intelligence
Program: Data Science
Program: Computer Science
```

---

### 2. **ProgramOutcome** Table
Learning outcomes/career paths for each program.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| program_id | Integer | Foreign key to Program |
| outcome_name | String | Outcome name (e.g., "AI Research", "ML Engineering") |
| outcome_description | Text | What students learn in this outcome |
| related_skills | Text | Comma-separated skills for this outcome |
| internship_keywords | Text | Keywords to match with internship descriptions |
| created_at | DateTime | Creation timestamp |

**Example Outcomes:**
```
AI Program → AI Research
           → AI Engineering
           → Machine Learning

Data Science Program → Data Analysis
                   → Data Science
                   → Business Intelligence

Computer Science Program → Software Development
                        → Natural Language Processing
                        → Computer Vision
```

---

### 3. **Student** Table
Student profiles (updated to support programs/outcomes).

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Student name |
| email | String | Student email (unique) |
| program_id | Integer | Foreign key to Program |
| gpa | Float | Student GPA |
| protected_age | Integer | Age (privacy-protected) |
| created_at | DateTime | Registration date |

**Relationships:**
- Student → Program (many students per program)
- Student → StudentOutcome (many outcomes per student)
- Student → Resume (many resumes per student)
- Student → Recommendation (many recommendations per student)

---

### 4. **StudentOutcome** Table
Tracks which career outcomes each student is pursuing.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| student_id | Integer | Foreign key to Student |
| outcome_id | Integer | Foreign key to ProgramOutcome |
| is_primary | Boolean | Is this the main career goal? |
| proficiency_level | String | beginner / intermediate / advanced |
| created_at | DateTime | When student selected this outcome |

**Usage:**
- A student can have multiple outcomes (e.g., "AI Research" + "AI Engineering")
- Mark one as `is_primary=true` for the main goal
- Track proficiency to match with opportunity difficulty level

---

### 5. **Resume** Table
Student resumes (unchanged structure, same content).

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| student_id | Integer | Foreign key to Student |
| filename | String | Uploaded file name |
| parsed_text | Text | Extracted resume text |
| skills | Text | Comma-separated extracted skills |
| outcomes | Text | Detected outcomes from resume |
| embedding | Text | Vector embedding for matching |
| created_at | DateTime | Upload date |

---

### 6. **Internship** Table
Job postings with outcome focus (new fields).

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | String | Job title (e.g., "ML Engineering Intern") |
| company_name | String | Company name |
| location | String | Location |
| description | Text | Full job description |
| required_skills | Text | Comma-separated required skills |
| **outcome_focus** | String | **NEW:** Which outcome this aligns with |
| posting_url | String | Apply link |
| posted_date | DateTime | Posted date |
| is_active | Integer | Active (1) or archived (0) |
| source | String | Source (RapidAPI, JobStreet, etc.) |
| created_at | DateTime | Scraping date |

**New Field `outcome_focus`:**
- Stores outcome name (e.g., "AI Research", "Data Analysis")
- Extracted from job title/description or added during scraping
- Used to match with student outcomes

---

### 7. **Recommendation** Table
Internship recommendations with outcome matching (enhanced).

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| student_id | Integer | Foreign key to Student |
| internship_id | Integer | Foreign key to Internship |
| department_id | Integer | Foreign key to Department (legacy) |
| **outcome_match** | String | **NEW:** Which outcome matched |
| **score** | Float | **NEW:** Overall match score (0-100) |
| **skill_match_score** | Float | **NEW:** Skill overlap % |
| **outcome_match_score** | Float | **NEW:** Outcome alignment % |
| reason | Text | Human-readable explanation |
| created_at | DateTime | Recommendation date |

**Scoring:**
- Overall Score = 0.7 × skill_match + 0.3 × outcome_match
- Prioritizes skill overlap but heavily weights outcome alignment

---

## Database Relationships Diagram

```
Program (1) ─── (Many) ProgramOutcome
  │                         │
  │                         │
  └─── (Many) Student       │
         │                  │
         ├─ (1:Many) Resume │
         ├─ (1:Many) StudentOutcome ──── (Many:1) ProgramOutcome
         └─ (1:Many) Recommendation


Internship (Many) ─── (1) Recommendation ──── (Many) Student
```

---

## How Outcome-Based Matching Works

### Step 1: Student Selects Outcomes
When creating a profile or uploading a resume:
```
Student selects:
  ✓ Primary Outcome: "AI Research" (is_primary=true)
  ✓ Secondary Outcome: "Machine Learning" (is_primary=false)
```

### Step 2: Resume Parsing Detects Outcomes
Parser looks for outcome keywords in resume:
```
Resume text: "Conducted research on neural networks and published papers"
Detected outcomes: "AI Research"  (keywords: research, papers)
                  "Deep Learning" (keywords: neural networks)
```

### Step 3: Scraper Tags Internships with Outcomes
RapidAPI scraper extracts internship outcome focus:
```
Internship: "ML Research Engineer at Google AI"
  Description mentions: "research", "algorithms", "papers"
  outcome_focus: "AI Research"
```

### Step 4: Recommendation Engine Matches
Compares student outcomes with internship focus:
```
Student outcomes: ["AI Research", "Machine Learning"]
Internship outcome_focus: "AI Research"

Match: ✅ Direct outcome match!
outcome_match_score: 95%

Plus:
skill_match_score: 85% (Python, TensorFlow, Deep Learning)

Final score: 0.7 × 85 + 0.3 × 95 = 88%
```

### Step 5: Return Ranked Recommendations
Internships sorted by outcome + skill alignment.

---

## Setup Instructions

### 1. Create Tables
The tables are auto-created when you start the backend:
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Seed Program Outcomes
```powershell
python scripts/seed_program_outcomes.py
```

Output:
```
Creating database tables...
✓ Tables created

Seeding program outcomes...

✓ Program: Artificial Intelligence
  └─ Outcome: AI Research
  └─ Outcome: AI Engineering
  └─ Outcome: Machine Learning

✓ Program: Data Science
  └─ Outcome: Data Analysis
  └─ Outcome: Data Science
  └─ Outcome: Business Intelligence

✓ Program: Computer Science
  └─ Outcome: Software Development
  └─ Outcome: Natural Language Processing
  └─ Outcome: Computer Vision

==================================================
✅ Seeding complete!
   Programs created: 3
   Outcomes created: 9
==================================================

✅ Example student outcomes added!

🎓 Program outcomes database ready!
```

### 3. Verify in PostgreSQL
```powershell
psql -U internship_user -d internshipdb -h localhost
```

Check programs:
```sql
SELECT id, name FROM programs;
```

Check outcomes:
```sql
SELECT po.outcome_name, p.name FROM program_outcomes po 
JOIN programs p ON po.program_id = p.id;
```

---

## Adding Custom Outcomes

Edit `backend/scripts/seed_program_outcomes.py` and add to `PROGRAMS_DATA`:

```python
{
    "name": "Your Program Name",
    "description": "Program description",
    "outcomes": [
        {
            "outcome_name": "Career Path Name",
            "outcome_description": "What students do in this path",
            "related_skills": "python,skill2,skill3",
            "internship_keywords": "keyword1,keyword2,keyword3"
        }
    ]
}
```

Then re-run the seed script:
```powershell
python scripts/seed_program_outcomes.py
```

---

## API Integration (Future)

### Endpoint: Get Student Outcomes
```bash
GET /api/students/{student_id}/outcomes
```

Response:
```json
{
  "student_id": 1,
  "program": "Artificial Intelligence",
  "outcomes": [
    {
      "id": 5,
      "outcome_name": "AI Research",
      "is_primary": true,
      "proficiency_level": "intermediate"
    }
  ]
}
```

### Endpoint: Get Recommendations by Outcome
```bash
GET /api/recommendations?outcome=AI%20Research
```

Response:
```json
{
  "outcome": "AI Research",
  "internships": [
    {
      "id": 42,
      "title": "AI Research Intern",
      "company": "Google DeepMind",
      "outcome_match_score": 95,
      "skill_match_score": 88,
      "overall_score": 90
    }
  ]
}
```

---

## Example Data

### Programs (Created by seed)
```
1. Artificial Intelligence
2. Data Science
3. Computer Science
```

### Outcomes (9 total)
```
AI Program:
  1. AI Research (skills: python, pytorch, research, papers)
  2. AI Engineering (skills: python, deployment, docker, mlops)
  3. Machine Learning (skills: python, scikit-learn, models)

Data Science Program:
  4. Data Analysis (skills: python, sql, visualization)
  5. Data Science (skills: python, modeling, prediction)
  6. Business Intelligence (skills: sql, tableau, analytics)

Computer Science Program:
  7. Software Development (skills: python, design, git)
  8. Natural Language Processing (skills: nlp, bert, transformers)
  9. Computer Vision (skills: opencv, cnn, image processing)
```

---

## Key Features

✅ **Outcome-Based Matching:** Match internships to career goals, not just skills
✅ **Flexible Programs:** Add as many programs and outcomes as needed
✅ **Student Goals:** Track primary/secondary outcomes
✅ **Internship Tagging:** Tag internships with outcome focus
✅ **Weighted Scoring:** Outcome + skill alignment for better matches
✅ **Scalable:** Supports multiple programs and outcomes
✅ **Privacy:** No personal data tracking, skill/outcome focused

---

## Thesis Alignment

This schema directly supports the thesis: **"AI-Based Student Internship Matcher"**

- ✅ **AI-Powered:** Uses NLP to extract outcomes from resumes and job descriptions
- ✅ **Outcome Focused:** Matches students to internships based on learning outcomes
- ✅ **Data-Driven:** Scoring uses skill overlap + outcome alignment
- ✅ **Scalable:** Supports any number of programs and outcomes

---

## Next Steps

1. ✅ Run `seed_program_outcomes.py` to populate outcomes
2. ✅ Update frontend to capture student outcomes during signup
3. ✅ Modify recommendation API to use outcome matching
4. ✅ Tag RapidAPI internships with outcome focus
5. ✅ Display outcome-aligned matches in frontend

Your AI Internship Matcher now supports full outcome-based career path matching! 🎓🚀
