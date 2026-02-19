export interface PersonalInfo {
  full_name: string;
  email: string;
  phone: string;
  location: string;
  linkedin?: string;
  github?: string;
  website?: string;
  summary?: string;
}

export interface Education {
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date: string;
  grade?: string;
  description?: string;
}

export interface Experience {
  company: string;
  title: string;
  start_date: string;
  end_date: string;
  location?: string;
  responsibilities: string[];
}

export interface Project {
  name: string;
  description: string;
  technologies: string[];
  link?: string;
}

export interface ResumeData {
  personal_info: PersonalInfo;
  skills: string[];
  education: Education[];
  experience: Experience[];
  projects: Project[];
}

export interface ATSScoreBreakdown {
  keyword_match: number;
  formatting: number;
  readability: number;
  structure: number;
}

export interface ATSScoreResponse {
  score: number;
  breakdown: ATSScoreBreakdown;
  feedback: string[];
}

export interface EnhanceRequest {
  resume_data: ResumeData;
  job_description?: string;
  template: string;
}

export interface EnhanceResponse {
  enhanced_resume_data: ResumeData;
  latex_content?: string;
  score: ATSScoreResponse;
}

export interface UploadResponse {
  resume_data: ResumeData;
}

export interface DownloadResponse {
  url: string;
}

export type TemplateOption = {
  id: string;
  name: string;
  description: string;
  previewImage: string;
};
