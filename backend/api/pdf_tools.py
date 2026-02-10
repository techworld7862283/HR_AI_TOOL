from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pdf2docx import Converter
import os, uuid

router = APIRouter()
UPLOAD_DIR = "backend/uploads"
OUTPUT_DIR = "backend/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

@router.post("/pdf_to_word")
async def pdf_to_word(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF allowed")
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")

    uid = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{uid}.pdf")
    docx_path = os.path.join(OUTPUT_DIR, f"{uid}.docx")

    with open(pdf_path, "wb") as f: f.write(file_bytes)

    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        if background_tasks:
            background_tasks.add_task(os.remove, pdf_path)
            background_tasks.add_task(os.remove, docx_path)
        return FileResponse(docx_path,
                            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            filename="converted.docx")
    except Exception as e:
        raise HTTPException(500, f"PDF→Word failed: {e}")
