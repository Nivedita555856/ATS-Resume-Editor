from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import ats, chat, enhance, generate, manual, upload

app = FastAPI(
    title="AI Resume Builder & ATS Optimization API",
    version="1.0.0",
    description="Upload, optimize, score, and generate ATS-friendly resumes.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(manual.router, prefix="/api", tags=["manual"])
app.include_router(ats.router, prefix="/api", tags=["ats"])
app.include_router(enhance.router, prefix="/api", tags=["enhance"])
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
