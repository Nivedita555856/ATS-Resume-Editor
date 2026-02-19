import json
import requests

BASE_URL = "http://localhost:8000"

sample_resume = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-555-0100",
    "summary": "Software engineer focused on Python, FastAPI, cloud deployment, and scalable APIs.",
    "skills": ["Python", "FastAPI", "Docker", "AWS", "REST APIs"],
    "experience": [
        {
            "title": "Backend Engineer",
            "company": "Tech Corp",
            "description": "Built and deployed API services with FastAPI and Docker.",
        }
    ],
    "education": [
        {
            "degree": "B.Sc. Computer Science",
            "institution": "Example University",
            "year": "2022",
        }
    ],
}

job_description = (
    "We are looking for a Python backend engineer with FastAPI, Docker, cloud, and API design experience."
)


def post(path: str, payload: dict):
    response = requests.post(f"{BASE_URL}{path}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    print("\n== Testing ATS scoring endpoint ==")
    ats_result = post("/api/ats-score", {"resume": sample_resume, "job_description": job_description})
    print(json.dumps(ats_result, indent=2))

    print("\n== Testing enhancement endpoint ==")
    enhance_result = post("/api/enhance", {"resume": sample_resume, "job_description": job_description})
    print(json.dumps(enhance_result, indent=2))

    print("\n== Testing generation endpoint ==")
    generate_result = post("/api/generate", {"resume": sample_resume, "template": "modern"})
    print(json.dumps(generate_result, indent=2))


if __name__ == "__main__":
    main()
