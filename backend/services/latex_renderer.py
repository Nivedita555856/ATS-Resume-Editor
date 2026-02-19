from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from backend.models.schemas import ResumeData

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "generated"


class LatexRendererService:
    def __init__(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            autoescape=select_autoescape(enabled_extensions=()),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def render_template(self, template_name: str, resume: ResumeData) -> str:
        template_file = f"{template_name}.tex.j2"
        try:
            template = self.env.get_template(template_file)
            return template.render(resume=resume.model_dump())
        except Exception as exc:
            raise ValueError(f"Failed to render template '{template_file}': {exc}") from exc

    def compile_pdf(self, latex_content: str, output_basename: str) -> Path:
        if not shutil.which("pdflatex"):
            raise RuntimeError("pdflatex is not installed or not available in PATH.")

        tex_path = OUTPUT_DIR / f"{output_basename}.tex"
        pdf_path = OUTPUT_DIR / f"{output_basename}.pdf"
        tex_path.write_text(latex_content, encoding="utf-8")

        cmd = [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={OUTPUT_DIR}",
            str(tex_path),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            if not pdf_path.exists():
                raise RuntimeError("PDF compilation completed without generating a PDF file.")
            return pdf_path
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"pdflatex compilation failed: {exc.stderr}") from exc


latex_renderer_service = LatexRendererService()
