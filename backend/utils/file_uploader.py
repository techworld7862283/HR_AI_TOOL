from pdfminer.high_level import extract_text
from docx import Document
import pandas as pd
import tempfile
import os

def extract_text_from_file(file):
    suffix = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        temp_path = tmp.name

    try:
        if suffix == ".pdf":
            return extract_text(temp_path)

        elif suffix == ".docx":
            doc = Document(temp_path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif suffix == ".csv":
            df = pd.read_csv(temp_path)
            return df.to_string(index=False)

        else:
            raise ValueError("Unsupported file format")

    finally:
        os.remove(temp_path)
