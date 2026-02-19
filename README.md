# ATS Resume Editor

ATS Resume Editor is a full-stack application designed to help job seekers optimize resumes for Applicant Tracking Systems (ATS), improve wording with AI-ready workflows, and generate polished output documents.

## Features

- ATS score analysis against a target job description.
- Resume enhancement endpoint to improve summary and skill alignment.
- Resume generation endpoint for template-based export workflows.
- FastAPI backend ready for Render deployment via Docker.
- Next.js frontend configuration ready for Vercel deployment.
- API proxy rewrites from frontend (`/api/*`) to backend base URL.

## Screenshots

> Add screenshots after deployment or local run.

### Dashboard

![Dashboard Placeholder](docs/screenshots/dashboard-placeholder.png)

### ATS Score Results

![ATS Results Placeholder](docs/screenshots/ats-results-placeholder.png)

### Resume Preview

![Resume Preview Placeholder](docs/screenshots/resume-preview-placeholder.png)

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- Docker (Render)
- TeX Live (for LaTeX/PDF workflows)

### Frontend
- Next.js
- Node.js
- Vercel

## Folder Structure

```text
ATS-Resume-Editor/
├── backend/
│   ├── .env.example
│   ├── .gitignore
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── test_backend.py
├── frontend/
│   ├── .env.example
│   ├── .gitignore
│   └── next.config.js
├── render.yaml
└── README.md
```

## Local Setup (Step by Step)

### 1) Clone repository

```bash
git clone <your-repo-url>
cd ATS-Resume-Editor
```

### 2) Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 3) Run backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at `http://localhost:8000`.

### 4) Test backend APIs

In another terminal:

```bash
cd backend
python test_backend.py
```

### 5) Frontend setup

```bash
cd ../frontend
cp .env.example .env.local
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`.

## Deployment Instructions

## Deploy Backend on Render

1. Push your repository to GitHub.
2. In Render, create a **New Web Service** from your repo.
3. Render detects `render.yaml` and provisions the Docker web service.
4. Set environment variables in Render dashboard:
   - `OPENAI_API_KEY`
   - Any additional backend secrets
5. Deploy and verify health endpoint:
   - `GET https://<your-render-url>/health`

## Deploy Frontend on Vercel

1. Import the repository in Vercel.
2. Set project root to `frontend`.
3. Add environment variables in Vercel settings:
   - `NEXT_PUBLIC_API_URL=https://<your-render-url>`
   - `NEXT_PUBLIC_APP_ENV=production`
   - `NEXT_PUBLIC_SITE_URL=https://<your-vercel-url>`
4. Deploy and verify API rewrite by calling frontend `/api/...` routes.

## API Documentation

Base URL (local): `http://localhost:8000`

### Health Check

- **GET** `/health`

Response:

```json
{
  "status": "ok"
}
```

### ATS Scoring

- **POST** `/api/ats-score`

Request:

```json
{
  "resume": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0100",
    "summary": "Software engineer focused on Python and FastAPI.",
    "skills": ["Python", "FastAPI", "Docker"],
    "experience": [
      {
        "title": "Backend Engineer",
        "company": "Tech Corp",
        "description": "Built API services."
      }
    ],
    "education": [
      {
        "degree": "B.Sc. Computer Science",
        "institution": "Example University",
        "year": "2022"
      }
    ]
  },
  "job_description": "Looking for Python FastAPI Docker experience."
}
```

Response:

```json
{
  "score": 67,
  "matched_keywords": ["docker", "fastapi", "python"],
  "missing_keywords": ["experience", "looking", "for"],
  "suggestions": [
    "Add more measurable achievements to your experience section.",
    "Prioritize keywords from the job description in your summary."
  ]
}
```

### Resume Enhancement

- **POST** `/api/enhance`

Request:

```json
{
  "resume": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0100",
    "summary": "Software engineer focused on Python and FastAPI.",
    "skills": ["Python", "FastAPI", "Docker"],
    "experience": [],
    "education": []
  },
  "job_description": "Looking for strong communication and cloud deployment experience."
}
```

Response:

```json
{
  "enhanced_resume": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0100",
    "summary": "Results-driven professional aligned with this role...",
    "skills": ["Communication", "Docker", "FastAPI", "Leadership", "Problem Solving", "Python"],
    "experience": [],
    "education": []
  },
  "improvements": [
    "Optimized summary with role-specific language.",
    "Expanded core skills with ATS-friendly terms."
  ]
}
```

### Resume Generation

- **POST** `/api/generate`

Request:

```json
{
  "resume": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0100",
    "summary": "Software engineer",
    "skills": ["Python"],
    "experience": [],
    "education": []
  },
  "template": "modern"
}
```

Response:

```json
{
  "message": "Resume generation job accepted.",
  "template": "modern",
  "download_url": "https://example.com/generated/resume.pdf"
}
```

## Environment Variables

### Backend (`backend/.env`)

- `APP_ENV`: development | production
- `HOST`: backend bind host
- `PORT`: backend port
- `OPENAI_API_KEY`: API key for LLM features
- `LOG_LEVEL`: logging level

### Frontend (`frontend/.env.local`)

- `NEXT_PUBLIC_APP_ENV`: development | production
- `NEXT_PUBLIC_API_URL`: backend base URL
- `NEXT_PUBLIC_SITE_URL`: public frontend URL
