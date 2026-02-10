def score_candidate(resume: dict, jd: dict, semantic_score: float) -> dict:
    resume_skills = set(resume.get("skills", []))
    jd_skills = set(jd.get("skills", []))
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    skill_score = (len(matched) / max(len(jd_skills), 1)) * 100
    final_score = round((0.6 * semantic_score) + (0.4 * skill_score), 2)
    experience_gap = "Below requirement" if resume.get("experience_years", 0) < jd.get("min_experience", 0) else "Meets requirement"
    verdict = "Strong Match" if final_score >= 80 else "Potential Match" if final_score >= 60 else "Weak Match"
    return {
        "match_score": final_score,
        "semantic_similarity": semantic_score,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "experience_gap": experience_gap,
        "verdict": verdict
    }
