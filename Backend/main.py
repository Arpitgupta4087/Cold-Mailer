import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv
from model import Chain
from resume import Resume
from util import clean_text
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

app = FastAPI(title="AI Job Outreach API")
chain = Chain()

class EmailRequest(BaseModel):
    job_description: str
    resume_text: str

class MatchRequest(BaseModel):
    job_url: HttpUrl
    resume_text: str

class JobExtractionResponse(BaseModel):
    role: str | None = None
    experience: str | None = None
    skills: list[str] | None = None
    description: str | None = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Job Outreach API!"}

@app.post("/generate-email/", summary="Generate a cold email")
async def generate_email(request: EmailRequest):
    try:
        email_content = chain.write_mail(request.job_description, request.resume_text)
        return {"email": email_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match-score/", summary="Calculate Resume-to-JD Match Score")
async def get_match_score(request: MatchRequest):
    try:
        score, reason = chain.match_score(str(request.job_url), request.resume_text)
        return {"score": score, "reason": reason}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-jobs-from-url/", summary="Extract job postings from a URL")
async def extract_jobs_from_url(url: HttpUrl):
    try:
        loader = WebBaseLoader([str(url)])
        page_content = loader.load().pop().page_content
        cleaned_text = clean_text(page_content)
        jobs = chain.extract_jobs(cleaned_text)
        return {"jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-resume/", summary="Upload and process a resume")
async def process_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            resume_path = tmp.name

        resume_obj = Resume(resume_path)
        resume_text = resume_obj.get_text()

        os.unlink(resume_path)

        return {"resume_text": resume_text}
    except Exception as e:
        if 'resume_path' in locals() and os.path.exists(resume_path):
            os.unlink(resume_path)
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")
