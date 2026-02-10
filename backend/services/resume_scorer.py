import re

COMMON_SKILLS = {
    "python": 90,
    "java": 70,
    "sql": 80,
    "machine learning": 85,
    "fastapi": 75,
    "django": 70,
    "docker": 65,
    "aws": 60
}

def analyze_resume(text: str):
    text_lower = text.lower()
    skills_found = {}
    missing_skills = []

    for skill, weight in COMMON_SKILLS.items():
        if re.search(rf"\b{skill}\b", text_lower):
            skills_found[skill] = weight
        else:
            missing_skills.append(skill)

    experience_years = extract_experience(text_lower)
    score = calculate_score(skills_found, experience_years)

    return {
        "score": score,
        "experience_years": experience_years,
        "skills": skills_found,
        "missing_skills": missing_skills,
        "summary": generate_summary(score, skills_found, missing_skills)
    }

def extract_experience(text):
    match = re.search(r"(\d+)\+?\s+years", text)
    return int(match.group(1)) if match else 0

def calculate_score(skills, experience):
    skill_score = sum(skills.values()) / max(len(COMMON_SKILLS), 1)
    experience_score = min(experience * 5, 30)
    return min(int(skill_score + experience_score), 100)

def generate_summary(score, skills, missing):
    if score >= 80:
        return "Strong candidate with relevant skills."
    elif score >= 60:
        return "Moderate match, some upskilling recommended."
    else:
        return "Low match for the role."
