import re
from pdfminer.high_level import extract_text
from docx import Document
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

SKILL_VOCAB = set([
    "python","java","c++","c#","javascript","react","vue","django","flask","sql",
    "postgresql","mongodb","tensorflow","pytorch","keras","machine learning","data analysis",
    "git","docker","html","css","node.js","express","linux","networking"
])

def extract_text_from_pdf(path):
    return extract_text(path)

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def parse_resume(file_path):
    text = ""
    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

    text_norm = re.sub(r"\s+", " ", text)
    gpa = None
    m = re.search(r"(?i)(GPA|Grade Point Average)[:\s]*([0-9]\.?[0-9]?)", text)
    if m:
        try:
            gpa = float(m.group(2))
        except:
            gpa = None

    doc = nlp(text_norm.lower())
    found_skills = set()
    for token in doc:
        if token.lemma_ in SKILL_VOCAB or token.text in SKILL_VOCAB:
            found_skills.add(token.text)
    for nc in doc.noun_chunks:
        phrase = nc.text.strip()
        if phrase in SKILL_VOCAB:
            found_skills.add(phrase)

    outcomes = []
    outcome_map = {
        "software development": ["software","development","programming"],
        "data analysis": ["data analysis","statistics","data science"],
        "networking": ["network","routing","switching"],
    }
    for key, kws in outcome_map.items():
        for kw in kws:
            if kw in text_norm.lower():
                outcomes.append(key); break

    return {
        "text": text_norm,
        "gpa": gpa,
        "skills": list(found_skills),
        "outcomes": outcomes
    }


def extract_skills_from_text(text):
    """Return a list of skills found in arbitrary job or resume text using SKILL_VOCAB."""
    if not text:
        return []
    doc = nlp(text.lower())
    found = set()
    for token in doc:
        if token.lemma_ in SKILL_VOCAB or token.text in SKILL_VOCAB:
            found.add(token.text)
    for nc in doc.noun_chunks:
        phrase = nc.text.strip()
        if phrase in SKILL_VOCAB:
            found.add(phrase)
    return list(found)
