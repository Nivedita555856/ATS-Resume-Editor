import json

from fastapi import APIRouter, HTTPException
from openai import OpenAI

from backend.config import get_settings
from backend.models.schemas import ChatRequest

router = APIRouter()
settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


@router.post("/chat")
async def resume_chat(payload: ChatRequest) -> dict:
    if not client:
        raise HTTPException(status_code=500, detail="OpenAI API key is not configured.")

    try:
        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are a senior resume coach. Provide practical, concise, personalized guidance "
                    "for ATS and recruiter impact."
                ),
            }
        ]

        if payload.resume:
            messages.append(
                {
                    "role": "system",
                    "content": f"Resume context JSON:\n{json.dumps(payload.resume.model_dump())}",
                }
            )

        for msg in payload.history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": payload.message})

        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.5,
        )
        answer = response.choices[0].message.content or "I can help refine your resume further."
        return {"reply": answer, "history": messages + [{"role": "assistant", "content": answer}]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chat request failed: {exc}") from exc
