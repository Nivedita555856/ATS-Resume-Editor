from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.models.schemas import ResumeData
from backend.services.parser import resume_parser_service

router = APIRouter()


@router.post("/upload", response_model=ResumeData)
async def upload_resume(file: UploadFile = File(...)) -> ResumeData:
    filename = (file.filename or "").lower()
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    try:
        content = await file.read()
        text = (
            resume_parser_service.extract_text_from_pdf(content)
            if filename.endswith(".pdf")
            else resume_parser_service.extract_text_from_docx(content)
        )
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from uploaded file.")
        return await resume_parser_service.parse_resume_text_to_schema(text)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
