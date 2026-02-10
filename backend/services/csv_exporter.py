import csv
import io

def resume_result_to_csv(result: dict):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Field", "Value"])
    writer.writerow(["Total Score", result.get("score")])
    writer.writerow(["Experience (Years)", result.get("experience_years")])
    writer.writerow(["Summary", result.get("summary")])
    writer.writerow(["Top Skills", ", ".join(result.get("skills", {}).keys())])
    writer.writerow(["Missing Skills", ", ".join(result.get("missing_skills", []))])
    writer.writerow([])
    writer.writerow(["Skill", "Score"])
    for skill, score in result.get("skills", {}).items():
        writer.writerow([skill, score])
    buffer.seek(0)
    return buffer
