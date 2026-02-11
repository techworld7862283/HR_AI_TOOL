import subprocess
from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, HTTPException
import os, uuid

router = APIRouter()
UPLOAD_DIR = "backend/uploads"
OUTPUT_DIR = "backend/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(400, "Only DOCX allowed")

    uid = str(uuid.uuid4())
    docx_path = os.path.join(UPLOAD_DIR, f"{uid}.docx")
    pdf_path = os.path.join(OUTPUT_DIR, f"{uid}.pdf")

    with open(docx_path, "wb") as f:
        f.write(await file.read())

    try:
        # Convert using LibreOffice headless
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", OUTPUT_DIR],
            check=True
        )
    except Exception as e:
        raise HTTPException(500, f"Conversion failed: {e}")

    return FileResponse(pdf_path, media_type="application/pdf", filename="converted.pdf")
