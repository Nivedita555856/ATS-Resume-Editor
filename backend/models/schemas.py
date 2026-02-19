from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    linkedin: str | None = None
    github: str | None = None
    location: str | None = None


class Education(BaseModel):
    degree: str
    institution: str
    year: str
    gpa: str | None = None
    relevant_courses: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str
    bullets: list[str]


class Project(BaseModel):
    name: str
    description: str
    tech_stack: list[str] = Field(default_factory=list)
    link: str | None = None


class ResumeData(BaseModel):
    personal_info: PersonalInfo
    summary: str | None = None
    education: list[Education]
    skills: list[str]
    certifications: list[str] = Field(default_factory=list)
    experience: list[Experience]
    projects: list[Project] = Field(default_factory=list)


class ATSResult(BaseModel):
    overall_score: int
    keyword_score: int
    section_score: int
    formatting_score: int
    readability_score: int
    missing_keywords: list[str]
    suggestions: list[str]


class EnhancedResume(BaseModel):
    original: ResumeData
    enhanced: ResumeData
    original_ats_score: ATSResult
    enhanced_ats_score: ATSResult
    changes_made: list[str]


class ATSScoreRequest(BaseModel):
    resume: ResumeData
    job_description: str | None = None


class EnhanceRequest(BaseModel):
    resume: ResumeData
    target_role: str | None = None
    job_description: str | None = None


class GenerateRequest(BaseModel):
    resume: ResumeData
    template_name: Literal["classic", "modern", "professional"] = "classic"
    output_basename: str = "resume"


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    resume: ResumeData | None = None
    history: list[ChatMessage] = Field(default_factory=list)
