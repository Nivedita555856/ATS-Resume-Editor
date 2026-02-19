from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="ATS Resume Editor API", version="1.0.0")


class Experience(BaseModel):
    title: str
    company: str
    description: str


class Education(BaseModel):
    degree: str
    institution: str
    year: str


class ResumeData(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)


class ATSScoreRequest(BaseModel):
    resume: ResumeData
    job_description: str


class EnhanceRequest(BaseModel):
    resume: ResumeData
    job_description: str


class GenerateRequest(BaseModel):
    resume: ResumeData
    template: str = "classic"


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/ats-score")
def ats_score(payload: ATSScoreRequest) -> dict:
    jd_words = {word.lower().strip(".,") for word in payload.job_description.split() if word}
    resume_words = {word.lower().strip(".,") for word in (payload.resume.summary + " " + " ".join(payload.resume.skills)).split() if word}
    matched = sorted(jd_words.intersection(resume_words))
    score = int(min(100, (len(matched) / max(1, len(jd_words))) * 100))

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": sorted(jd_words.difference(resume_words))[:20],
        "suggestions": [
            "Add more measurable achievements to your experience section.",
            "Prioritize keywords from the job description in your summary.",
        ],
    }


@app.post("/api/enhance")
def enhance_resume(payload: EnhanceRequest) -> dict:
    enhanced_summary = (
        f"Results-driven professional aligned with this role: {payload.job_description[:120]}... "
        "Known for delivering measurable impact, cross-functional collaboration, and strong execution."
    )

    enhanced_skills = sorted(set(payload.resume.skills + ["Problem Solving", "Communication", "Leadership"]))

    return {
        "enhanced_resume": {
            **payload.resume.model_dump(),
            "summary": enhanced_summary,
            "skills": enhanced_skills,
        },
        "improvements": [
            "Optimized summary with role-specific language.",
            "Expanded core skills with ATS-friendly terms.",
        ],
    }


@app.post("/api/generate")
def generate_resume(payload: GenerateRequest) -> dict:
    # Placeholder for a real PDF generation flow (e.g., LaTeX templating).
    return {
        "message": "Resume generation job accepted.",
        "template": payload.template,
        "download_url": "https://example.com/generated/resume.pdf",
    }
