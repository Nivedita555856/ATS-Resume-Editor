from __future__ import annotations

import json
from typing import Any

import google.generativeai as genai

from backend.config import get_settings
from backend.models.schemas import ResumeData

settings = get_settings()


class GeminiEnhancementService:
    def __init__(self) -> None:
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None

    async def polish_resume(
        self,
        resume: ResumeData,
        target_role: str | None = None,
        job_description: str | None = None,
    ) -> ResumeData:
        if not self.model:
            raise ValueError("Gemini API key is not configured.")

        prompt = (
            "Perform grammar and clarity optimization on the resume JSON, improve professional tone, "
            "and suggest ATS-relevant keyword additions naturally in skills/summary/bullets. "
            "Keep factual consistency. Return only valid JSON in the same schema."
        )
        payload = {
            "target_role": target_role,
            "job_description": job_description,
            "resume": resume.model_dump(),
        }

        try:
            response = self.model.generate_content(
                [prompt, json.dumps(payload)],
                generation_config={"response_mime_type": "application/json", "temperature": 0.3},
            )
            text = (response.text or "{}").strip()
            data: dict[str, Any] = json.loads(text)
            return ResumeData.model_validate(data)
        except Exception as exc:
            raise ValueError(f"Gemini enhancement failed: {exc}") from exc


gemini_enhancement_service = GeminiEnhancementService()
