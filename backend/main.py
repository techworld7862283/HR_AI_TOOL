from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Routers
from backend.api import pdf_tools, word_tools, tts_tools, bulk_rank, export, jd_match, analytics
from backend.api import resume

app = FastAPI(title="Grand AI + HR Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(pdf_tools.router, prefix="/api/pdf")
app.include_router(word_tools.router, prefix="/api/word")
app.include_router(resume.router)
app.include_router(tts_tools.router, prefix="/api/tts")
app.include_router(bulk_rank.router, prefix="/api/bulk_rank")
app.include_router(export.router, prefix="/api/export")
app.include_router(jd_match.router, prefix="/api/jd_match")
app.include_router(analytics.router, prefix="/api/analytics")

# Serve frontend
frontend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
