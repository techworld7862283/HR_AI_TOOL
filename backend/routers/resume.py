from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from backend.utils.file_uploader import extract_text_from_file
from backend.services.resume_scorer import analyze_resume
from backend.services.csv_exporter import resume_result_to_csv

router = APIRouter(prefix="/api/resume", tags=["Resume"])
router = APIRouter(tags=["Resume Analysis"])

@router.post("/analyze_resume")
async def analyze_resume_json(file: UploadFile = File(...)):
    text = extract_text_from_file(file)
    return analyze_resume(text)
@router.post("/analyze_resume")
async def analyze_resume_api(file: UploadFile = File(...)):
    text = extract_text_from_file(file)
    return analyze_resume(text)

@router.post("/analyze_resume_csv")
async def analyze_resume_csv(file: UploadFile = File(...)):
    text = extract_text_from_file(file)
    result = analyze_resume(text)
    csv_buffer = resume_result_to_csv(result)

    return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=resume_analysis.csv"
        }
    )
