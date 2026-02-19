from fastapi import APIRouter, HTTPException

from backend.models.schemas import GenerateRequest
from backend.services.docx_generator import docx_generator_service
from backend.services.latex_renderer import latex_renderer_service

router = APIRouter()


@router.post("/generate")
async def generate_resume_files(payload: GenerateRequest) -> dict[str, str]:
    try:
        latex = latex_renderer_service.render_template(payload.template_name, payload.resume)
        pdf_path = latex_renderer_service.compile_pdf(latex, payload.output_basename)
        docx_path = docx_generator_service.generate(payload.resume, payload.output_basename)
        return {
            "pdf_path": str(pdf_path),
            "docx_path": str(docx_path),
            "template": payload.template_name,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate resume files: {exc}") from exc
