from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import analytics


# Import routers
from backend.api import pdf_tools, word_tools, tts_tools, bulk_rank, export, jd_match, analytics
from backend.routers import resume

app = FastAPI(title="Grand AI + HR Tool")

# CORS (allow frontend fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(pdf_tools.router, prefix="/api/pdf")
app.include_router(word_tools.router, prefix="/api/word")
app.include_router(resume.router)
app.include_router(tts_tools.router, prefix="/api/tts")
app.include_router(bulk_rank.router, prefix="/api/bulk_rank")
app.include_router(export.router, prefix="/api/export")
app.include_router(jd_match.router, prefix="/api/jd_match")
app.include_router(analytics.router, prefix="/api/analytics")
@app.get("/")
def root():
    return {"status": "API is live 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )


