import os
from ..config import settings

def explain_match(student, resume, department, score):
    provider = settings.LLM_PROVIDER
    prompt = f"""Provide a short (1-2 sentence) explanation why student '{student.name}' (GPA {student.gpa}) matches department '{department.name}' with score {score:.2f}. Mention skills that matched and program focus, avoid personal demographics."""
    if provider == "openai" and settings.OPENAI_API_KEY:
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content":"You are an assistant that creates neutral, concise match explanations."},
                          {"role":"user","content":prompt}],
                max_tokens=100
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            pass
    skills = resume.skills if resume.skills else "skills not listed"
    return f"Matches because {skills} align with department's focus ({department.program_focus})."
