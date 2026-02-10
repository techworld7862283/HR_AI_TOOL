from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
import uuid, os
from backend.services.extract_text_from_file import extract_text_from_file
from backend.services.parser import parse_resume

router = APIRouter()
UPLOAD_DIR = "backend/storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/parse")
async def parse_resume_api(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(400, "Only PDF or DOCX allowed")
    uid = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{uid}_{file.filename}")
    with open(path, "wb") as f:
        f.write(await file.read())
    text = extract_text_from_file(file)
    data = parse_resume(text)
    if background_tasks:
        background_tasks.add_task(os.remove, path)
    return {"filename": file.filename, "parsed_data": data}
