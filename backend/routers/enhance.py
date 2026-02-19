from fastapi import APIRouter, HTTPException

from backend.models.schemas import EnhancedResume, EnhanceRequest
from backend.services.gemini_service import gemini_enhancement_service
from backend.services.openai_service import openai_enhancement_service
from backend.services.scorer import ats_scorer_service

router = APIRouter()


def _changes(original: dict, enhanced: dict, prefix: str = "") -> list[str]:
    changes: list[str] = []
    for key, original_value in original.items():
        current_key = f"{prefix}.{key}" if prefix else key
        enhanced_value = enhanced.get(key)
        if isinstance(original_value, dict) and isinstance(enhanced_value, dict):
            changes.extend(_changes(original_value, enhanced_value, current_key))
        elif original_value != enhanced_value:
            changes.append(f"Updated {current_key}")
    return changes


@router.post("/enhance", response_model=EnhancedResume)
async def enhance_resume(payload: EnhanceRequest) -> EnhancedResume:
    try:
        original_ats = ats_scorer_service.score_resume(payload.resume, payload.job_description)
        openai_enhanced = await openai_enhancement_service.enhance_resume(
            payload.resume, payload.target_role, payload.job_description
        )
        polished = await gemini_enhancement_service.polish_resume(
            openai_enhanced, payload.target_role, payload.job_description
        )
        enhanced_ats = ats_scorer_service.score_resume(polished, payload.job_description)

        return EnhancedResume(
            original=payload.resume,
            enhanced=polished,
            original_ats_score=original_ats,
            enhanced_ats_score=enhanced_ats,
            changes_made=_changes(payload.resume.model_dump(), polished.model_dump()),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Enhancement pipeline failed: {exc}") from exc
