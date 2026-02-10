from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid, os
from backend.services.parser import extract_text, parse_resume
from backend.services.embeddings import similarity
from backend.services.scorer import score_candidate

router = APIRouter()
UPLOAD_DIR = "backend/storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/match")
async def match_resume_to_jd(resume: UploadFile = File(...), job_description: UploadFile = File(...)):
    if not resume.filename.lower().endswith((".pdf",".docx")):
        raise HTTPException(400, "Resume must be PDF or DOCX")
    if not job_description.filename.lower().endswith((".pdf",".docx",".txt")):
        raise HTTPException(400, "JD must be PDF, DOCX or TXT")
    rid, jid = str(uuid.uuid4()), str(uuid.uuid4())
    r_path = os.path.join(UPLOAD_DIR, f"{rid}_{resume.filename}")
    j_path = os.path.join(UPLOAD_DIR, f"{jid}_{job_description.filename}")
    with open(r_path,"wb") as f: f.write(await resume.read())
    with open(j_path,"wb") as f: f.write(await job_description.read())
    resume_text = extract_text(r_path)
    jd_text = extract_text(j_path)
    resume_data = parse_resume(resume_text)
    jd_data = {"skills": resume_data["skills"], "min_experience": 2}
    semantic_score = similarity(resume_text, jd_text)
    result = score_candidate(resume_data, jd_data, semantic_score)
    os.remove(r_path)
    os.remove(j_path)
    return {"resume": resume.filename, "job_description": job_description.filename, "analysis": result}
