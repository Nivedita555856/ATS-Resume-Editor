from fastapi import APIRouter

from backend.models.schemas import ResumeData

router = APIRouter()


@router.post("/manual", response_model=ResumeData)
async def manual_resume_input(resume: ResumeData) -> ResumeData:
    return resume
