from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import csv, io

router = APIRouter()

@router.post("/csv")
async def export_csv(payload: dict):
    candidates = payload.get("candidates", [])
    if not candidates:
        return {"error": "No candidate data provided"}
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Rank", "Filename", "Match Score", "Verdict", "Matched Skills", "Missing Skills"])
    for c in candidates:
        writer.writerow([
            c.get("rank"),
            c.get("filename"),
            c.get("match_score"),
            c.get("verdict"),
            ", ".join(c.get("matched_skills", [])),
            ", ".join(c.get("missing_skills", []))
        ])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=hr_analysis.csv"})
