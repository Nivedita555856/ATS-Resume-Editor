from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from backend.config import get_settings
from backend.models.schemas import ResumeData

settings = get_settings()


class OpenAIEnhancementService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def enhance_resume(
        self,
        resume: ResumeData,
        target_role: str | None = None,
        job_description: str | None = None,
    ) -> ResumeData:
        if not self.client:
            raise ValueError("OpenAI API key is not configured.")

        instructions = (
            "You are an expert resume editor. Rewrite experience bullets with strong action verbs, "
            "add measurable impact where possible, optimize skills for ATS keywords, and improve or generate "
            "a concise professional summary. Keep data truthful and do not invent companies or dates. "
            "Return JSON only matching the same schema as input."
        )

        payload = {
            "target_role": target_role,
            "job_description": job_description,
            "resume": resume.model_dump(),
        }

        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                response_format={"type": "json_object"},
                temperature=0.4,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": json.dumps(payload)},
                ],
            )
            content = response.choices[0].message.content or "{}"
            data: dict[str, Any] = json.loads(content)
            return ResumeData.model_validate(data)
        except Exception as exc:
            raise ValueError(f"OpenAI enhancement failed: {exc}") from exc


openai_enhancement_service = OpenAIEnhancementService()
