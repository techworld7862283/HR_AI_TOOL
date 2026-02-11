from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from gtts import gTTS
import os
import uuid

router = APIRouter()

OUTPUT_DIR = "backend/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Available voices (Google TTS language variants)
VOICE_OPTIONS = {
    "female_en_us": {"lang": "en", "tld": "com"},
    "male_en_uk": {"lang": "en", "tld": "co.uk"},
    "female_en_au": {"lang": "en", "tld": "com.au"},
    "male_en_in": {"lang": "en", "tld": "co.in"}
}


@router.post("/text_to_speech")
async def text_to_speech(
    text: str = Form(...),
    voice: str = Form("female_en_us")
):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text required")

    if voice not in VOICE_OPTIONS:
        raise HTTPException(status_code=400, detail="Invalid voice option")

    uid = str(uuid.uuid4())
    filename = f"{uid}.mp3"
    mp3_path = os.path.join(OUTPUT_DIR, filename)

    try:
        voice_config = VOICE_OPTIONS[voice]

        tts = gTTS(
            text=text,
            lang=voice_config["lang"],
            tld=voice_config["tld"]
        )

        tts.save(mp3_path)

        return JSONResponse({
            "audio_url": f"/api/tts/play/{filename}",
            "download_url": f"/api/tts/download/{filename}",
            "voice_used": voice
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")


@router.get("/play/{filename}")
async def play_audio(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    from fastapi.responses import FileResponse
    return FileResponse(file_path, media_type="audio/mpeg")


@router.get("/download/{filename}")
async def download_audio(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    from fastapi.responses import FileResponse
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename="tts.mp3"
    )
