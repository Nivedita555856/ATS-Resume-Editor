from __future__ import annotations

import io
import json
from typing import Any

import fitz
from docx import Document
from openai import OpenAI

from backend.config import get_settings
from backend.models.schemas import ResumeData

settings = get_settings()


class ResumeParserService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            pages = [page.get_text("text") for page in doc]
            return "\n".join(pages).strip()
        except Exception as exc:
            raise ValueError(f"Failed to parse PDF: {exc}") from exc

    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        try:
            stream = io.BytesIO(file_bytes)
            document = Document(stream)
            paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)
        except Exception as exc:
            raise ValueError(f"Failed to parse DOCX: {exc}") from exc

    async def parse_resume_text_to_schema(self, raw_text: str) -> ResumeData:
        if not self.client:
            raise ValueError("OpenAI API key not configured.")

        prompt = (
            "Extract resume information into the provided JSON schema exactly. "
            "Infer best-possible structure and preserve important details. "
            "Return valid JSON only."
        )
        schema = {
            "personal_info": {
                "name": "",
                "email": "",
                "phone": "",
                "linkedin": None,
                "github": None,
                "location": None,
            },
            "summary": "",
            "education": [
                {
                    "degree": "",
                    "institution": "",
                    "year": "",
                    "gpa": None,
                    "relevant_courses": [],
                }
            ],
            "skills": [],
            "certifications": [],
            "experience": [
                {
                    "title": "",
                    "company": "",
                    "start_date": "",
                    "end_date": "",
                    "bullets": [],
                }
            ],
            "projects": [
                {
                    "name": "",
                    "description": "",
                    "tech_stack": [],
                    "link": None,
                }
            ],
        }

        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": prompt},
                    {
                        "role": "user",
                        "content": f"Schema example: {json.dumps(schema)}\n\nResume text:\n{raw_text}",
                    },
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content or "{}"
            data: dict[str, Any] = json.loads(content)
            return ResumeData.model_validate(data)
        except Exception as exc:
            raise ValueError(f"Failed to parse resume text with AI: {exc}") from exc


resume_parser_service = ResumeParserService()
