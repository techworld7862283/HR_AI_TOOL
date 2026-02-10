import re
import spacy

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

SKILLS_DB = {
    "python", "java", "sql", "machine learning", "deep learning",
    "fastapi", "django", "flask", "excel", "power bi",
    "communication", "leadership", "docker", "aws"
}

def parse_resume(text: str) -> dict:
    doc = get_nlp()(text.lower())
    email = re.findall(r"[a-z0-9\._%+-]+@[a-z0-9\.-]+\.[a-z]{2,}", text)
    phone = re.findall(r"\+?\d[\d\s\-]{8,}", text)
    skills = sorted({token.text for token in doc if token.text in SKILLS_DB})
    experience_years = re.findall(r"(\d+)\+?\s+years?", text)
    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "skills": skills,
        "experience_years": max(map(int, experience_years)) if experience_years else 0
    }

def extract_text(file_path: str) -> str:
    from docx import Document
    import pdfplumber
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type")


