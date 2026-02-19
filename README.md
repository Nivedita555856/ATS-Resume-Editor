# AI-Powered Resume Builder & ATS Optimization Agent (Backend)

This repository contains a complete FastAPI backend for:
- Uploading and parsing resumes (PDF/DOCX)
- Manual resume JSON intake
- ATS scoring with detailed breakdown
- Resume enhancement using OpenAI (GPT-4o-mini) + Gemini (1.5 Flash)
- Resume generation as PDF (LaTeX + pdflatex) and DOCX
- Chat endpoint for personalized resume suggestions

## Project Structure

```text
backend/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── models/
│   └── schemas.py
├── routers/
│   ├── upload.py
│   ├── manual.py
│   ├── ats.py
│   ├── enhance.py
│   ├── generate.py
│   └── chat.py
├── services/
│   ├── parser.py
│   ├── scorer.py
│   ├── openai_service.py
│   ├── gemini_service.py
│   ├── latex_renderer.py
│   └── docx_generator.py
├── templates/
│   ├── classic.tex.j2
│   ├── modern.tex.j2
│   └── professional.tex.j2
└── tests/
    └── example_resume.json
```

## Prerequisites

- Python 3.11+
- `pdflatex` available on `PATH`
- OpenAI API key
- Gemini API key

## Setup

1. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp backend/.env.example .env
   ```

   `.env` format:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   GEMINI_MODEL=gemini-1.5-flash
   ```

4. **Run FastAPI server**
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

## API Endpoints

### 1) Upload Resume
`POST /api/upload`
- Accepts `.pdf` or `.docx`
- Parses and returns `ResumeData`

Example:
```bash
curl -X POST "http://127.0.0.1:8000/api/upload" \
  -F "file=@sample_resume.pdf"
```

### 2) Manual Resume Input
`POST /api/manual`
- Validates and echoes `ResumeData`

Example:
```bash
curl -X POST "http://127.0.0.1:8000/api/manual" \
  -H "Content-Type: application/json" \
  -d @backend/tests/example_resume.json
```

### 3) ATS Scoring
`POST /api/ats/score`
- Scores resume 0-100 using keyword match, section completeness, formatting, readability

Example:
```bash
curl -X POST "http://127.0.0.1:8000/api/ats/score" \
  -H "Content-Type: application/json" \
  -d '{
    "resume": '"$(cat backend/tests/example_resume.json)"',
    "job_description": "Looking for Python backend engineer with FastAPI, Docker, AWS, SQL experience"
  }'
```

### 4) Enhance Resume
`POST /api/enhance`
- OpenAI pass for quantified impact/action verbs/summary
- Gemini pass for grammar, tone, additional keyword quality
- Returns original + enhanced + ATS deltas

Example:
```bash
python - <<'PY'
import json, requests
resume = json.load(open('backend/tests/example_resume.json'))
payload = {
  "resume": resume,
  "target_role": "Senior Backend Engineer",
  "job_description": "Need FastAPI, AWS, Docker, SQL, CI/CD experience"
}
resp = requests.post("http://127.0.0.1:8000/api/enhance", json=payload, timeout=120)
print(resp.status_code)
print(resp.json())
PY
```

### 5) Generate PDF + DOCX
`POST /api/generate`
- Renders LaTeX template and compiles PDF
- Generates DOCX using `python-docx`

Example:
```bash
python - <<'PY'
import json, requests
resume = json.load(open('backend/tests/example_resume.json'))
payload = {
  "resume": resume,
  "template_name": "professional",
  "output_basename": "alex_johnson_resume"
}
resp = requests.post("http://127.0.0.1:8000/api/generate", json=payload, timeout=120)
print(resp.status_code)
print(resp.json())
PY
```

### 6) Resume Chat Assistant
`POST /api/chat`
- Accepts current user message + optional resume context + chat history

Example:
```bash
python - <<'PY'
import json, requests
resume = json.load(open('backend/tests/example_resume.json'))
payload = {
  "message": "How can I improve my experience bullets for ATS?",
  "resume": resume,
  "history": [
    {"role": "user", "content": "I am applying to backend roles."},
    {"role": "assistant", "content": "Great, let's focus on impact metrics and keywords."}
  ]
}
resp = requests.post("http://127.0.0.1:8000/api/chat", json=payload, timeout=120)
print(resp.status_code)
print(resp.json())
PY
```

## Notes

- PDF generation requires `pdflatex` to be installed locally.
- AI enhancement and chat endpoints require valid API keys.
- LaTeX templates are ATS-friendly, single-column, and complete.
- Generated files are saved in `backend/generated/`.
