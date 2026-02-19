from fastapi import APIRouter, HTTPException

from backend.models.schemas import ATSResult, ATSScoreRequest
from backend.services.scorer import ats_scorer_service

router = APIRouter()


@router.post("/ats/score", response_model=ATSResult)
async def score_resume(payload: ATSScoreRequest) -> ATSResult:
    try:
        return ats_scorer_service.score_resume(payload.resume, payload.job_description)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to score resume: {exc}") from exc
