from fastapi import APIRouter, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from gtts import gTTS
import os, uuid

router = APIRouter()
OUTPUT_DIR = "backend/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/text_to_speech")
async def text_to_speech(text: str = Form(...), background_tasks: BackgroundTasks = None):
    if not text.strip():
        raise HTTPException(400, "Text required")
    uid = str(uuid.uuid4())
    mp3_path = os.path.join(OUTPUT_DIR, f"{uid}.mp3")
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(mp3_path)
        if background_tasks:
            background_tasks.add_task(os.remove, mp3_path)
        return FileResponse(mp3_path, media_type="audio/mpeg", filename="tts.mp3")
    except Exception as e:
        raise HTTPException(500, f"TTS failed: {e}")
