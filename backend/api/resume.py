from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
import uuid, os
from backend.services.extract_text_from_file import extract_text_from_file
from backend.services.resume_scorer import analyze_resume

router = APIRouter(prefix="/api/resume", tags=["Resume"])

UPLOAD_DIR = "backend/storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze_resume")
async def analyze_resume_api(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    if not file.filename.lower().endswith((".pdf", ".docx", ".csv")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    text = extract_text_from_file(file)

    result = analyze_resume(text)

    return result


@router.post("/analyze_resume_csv")
async def analyze_resume_csv(
    file: UploadFile = File(...)
):
    from backend.services.csv_exporter import resume_result_to_csv

    text = extract_text_from_file(file)
    result = analyze_resume(text)

    csv_buffer = resume_result_to_csv(result)

    from fastapi.responses import StreamingResponse

    return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=resume_analysis.csv"}
    )
