import axios from 'axios';
import {
  ATSScoreResponse,
  DownloadResponse,
  EnhanceRequest,
  EnhanceResponse,
  ResumeData,
  UploadResponse
} from '@/types/resume';

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
});

export const uploadResume = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const { data } = await api.post<UploadResponse>('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return data;
};

export const getATSScore = async (resume_data: ResumeData): Promise<ATSScoreResponse> => {
  const { data } = await api.post<ATSScoreResponse>('/ats/score', { resume_data });
  return data;
};

export const enhanceResume = async (payload: EnhanceRequest): Promise<EnhanceResponse> => {
  const { data } = await api.post<EnhanceResponse>('/enhance', payload);
  return data;
};

export const downloadResume = async (
  resume_data: ResumeData,
  format: 'pdf' | 'docx'
): Promise<DownloadResponse> => {
  const { data } = await api.post<DownloadResponse>(`/download/${format}`, { resume_data });
  return data;
};

export default api;
