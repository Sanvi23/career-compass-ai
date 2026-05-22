from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from pdfminer.high_level import extract_text
from docx import Document
from pydantic import BaseModel
from app.skill_extractor import extract_skills
from typing import List
from app.job_matcher import calculate_match
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
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
    skills: List[str]
    message: str
class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str


class JobMatchResponse(BaseModel):
    score: int
    matched: list[str]
    missing: list[str]

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
    logger.info("Uploading file: %s", file.filename)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    text = extract_resume_text(file_path)
    skills = extract_skills(text)
    logger.info("Processed file successfully: %s", file.filename)
    return ResumeResponse(
        filename=file.filename,
        extracted_text=text[:1000],
        skills=skills,
        message="Resume processed successfully"
    )
@app.post(
    "/match-job",
    response_model=JobMatchResponse
)
def match_job(
        request: JobMatchRequest):

    result = calculate_match(
        request.resume_text,
        request.job_description
    )

    return JobMatchResponse(
        score=result["score"],
        matched=result["matched"],
        missing=result["missing"]
    )