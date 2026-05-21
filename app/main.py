from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from pdfminer.high_level import extract_text
from docx import Document
from pydantic import BaseModel

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

class ResumeResponse(BaseModel):
    filename: str
    extracted_text: str
    message: str

@app.post("/upload-resume", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".docx"]

    if not any(file.filename.endswith(ext)
               for ext in allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files allowed"
        )

    content = await file.read()

    max_size = 5 * 1024 * 1024  # 5MB

    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size: 5MB"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    text = extract_resume_text(file_path)

    return ResumeResponse(
        filename=file.filename,
        extracted_text=text[:1000],
        message="Resume processed successfully"
    )