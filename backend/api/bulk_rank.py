from fastapi import APIRouter, UploadFile, File, HTTPException
import os, uuid
from typing import List
from backend.services.parser import extract_text, parse_resume
from backend.services.embeddings import similarity
from backend.services.scorer import score_candidate

router = APIRouter()
UPLOAD_DIR = "backend/storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/rank")
async def rank_resumes(resumes: List[UploadFile] = File(...), job_description: UploadFile = File(...)):
    if not job_description.filename.lower().endswith((".pdf",".docx",".txt")):
        raise HTTPException(400, "Invalid JD format")
    jd_id = str(uuid.uuid4())
    jd_path = os.path.join(UPLOAD_DIR, f"{jd_id}_{job_description.filename}")
    with open(jd_path, "wb") as f:
        f.write(await job_description.read())
    jd_text = extract_text(jd_path)
    results = []
    for resume in resumes:
        if not resume.filename.lower().endswith((".pdf",".docx")):
            continue
        r_id = str(uuid.uuid4())
        r_path = os.path.join(UPLOAD_DIR, f"{r_id}_{resume.filename}")
        with open(r_path, "wb") as f:
            f.write(await resume.read())
        resume_text = extract_text(r_path)
        resume_data = parse_resume(resume_text)
        semantic_score = similarity(resume_text, jd_text)
        jd_data = {"skills": resume_data["skills"], "min_experience": 2}
        analysis = score_candidate(resume_data, jd_data, semantic_score)
        results.append({"filename": resume.filename, **analysis})
        os.remove(r_path)
    os.remove(jd_path)
    ranked = sorted(results, key=lambda x: x["match_score"], reverse=True)
    for i, r in enumerate(ranked, start=1):
        r["rank"] = i
    return {"total_candidates": len(ranked), "ranked_candidates": ranked}
