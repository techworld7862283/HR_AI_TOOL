from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from docx2pdf import convert
import os, uuid

router = APIRouter()

UPLOAD_DIR = "backend/uploads"
OUTPUT_DIR = "backend/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/word-to-pdf")
async def word_to_pdf(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only DOCX allowed")

    uid = str(uuid.uuid4())
    docx_path = f"{UPLOAD_DIR}/{uid}.docx"
    pdf_path = f"{OUTPUT_DIR}/{uid}.pdf"

    with open(docx_path, "wb") as f:
        f.write(await file.read())

    try:
        convert(docx_path, pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {e}")

    background_tasks.add_task(os.remove, docx_path)
    background_tasks.add_task(os.remove, pdf_path)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="converted.pdf"
    )
