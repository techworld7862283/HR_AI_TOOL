from fastapi import APIRouter
from collections import Counter

router = APIRouter()

@router.post("/analyze")
async def analyze_candidates(payload: dict):
    candidates = payload.get("candidates", [])
    if not candidates:
        return {"error": "No candidate data provided"}
    all_skills, verdicts, scores, experience_flags = [], [], [], []
    for c in candidates:
        all_skills.extend(c.get("matched_skills", []))
        verdicts.append(c.get("verdict"))
        scores.append(c.get("match_score"))
        experience_flags.append(c.get("experience_gap"))
    analytics = {
        "total_candidates": len(candidates),
        "average_match_score": round(sum(scores)/len(scores),2),
        "skill_distribution": dict(Counter(all_skills)),
        "verdict_distribution": dict(Counter(verdicts)),
        "experience_gap_distribution": dict(Counter(experience_flags))
    }
    return analytics
