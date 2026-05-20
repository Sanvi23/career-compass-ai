from fastapi import FastAPI, UploadFile, File
import os
from pdfminer.high_level import extract_text
from docx import Document

app = FastAPI(
    title="Career Compass AI",
    description="""
Upload resumes, extract text,
analyze skills and match jobs.
""",
    version="0.1.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_resume_text(file_path: str):
    if file_path.endswith(".pdf"):
        return extract_text(file_path)

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    return "Unsupported file format"


@app.get("/")
def home():
    return {"message": "Career Compass AI running"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_resume_text(file_path)

    return {
        "filename": file.filename,
        "extracted_text": text[:1000]
    }