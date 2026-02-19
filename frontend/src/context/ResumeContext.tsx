'use client';

import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useMemo,
  useState
} from 'react';
import { ATSScoreResponse, ResumeData } from '@/types/resume';

interface ResumeContextState {
  resumeData: ResumeData | null;
  enhancedResumeData: ResumeData | null;
  originalScore: ATSScoreResponse | null;
  enhancedScore: ATSScoreResponse | null;
  selectedTemplate: string;
  jobDescription: string;
  setResumeData: (data: ResumeData | null) => void;
  setEnhancedResumeData: (data: ResumeData | null) => void;
  setOriginalScore: (score: ATSScoreResponse | null) => void;
  setEnhancedScore: (score: ATSScoreResponse | null) => void;
  setSelectedTemplate: (template: string) => void;
  setJobDescription: (description: string) => void;
  resetAll: () => void;
}

const ResumeContext = createContext<ResumeContextState | undefined>(undefined);

const storageKey = 'ats-resume-state';

export const ResumeProvider = ({ children }: { children: ReactNode }) => {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [enhancedResumeData, setEnhancedResumeData] = useState<ResumeData | null>(null);
  const [originalScore, setOriginalScore] = useState<ATSScoreResponse | null>(null);
  const [enhancedScore, setEnhancedScore] = useState<ATSScoreResponse | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<string>('classic');
  const [jobDescription, setJobDescription] = useState<string>('');

  useEffect(() => {
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      const parsed = JSON.parse(stored) as Omit<ResumeContextState, 'resetAll'>;
      setResumeData(parsed.resumeData);
      setEnhancedResumeData(parsed.enhancedResumeData);
      setOriginalScore(parsed.originalScore);
      setEnhancedScore(parsed.enhancedScore);
      setSelectedTemplate(parsed.selectedTemplate || 'classic');
      setJobDescription(parsed.jobDescription || '');
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(
      storageKey,
      JSON.stringify({
        resumeData,
        enhancedResumeData,
        originalScore,
        enhancedScore,
        selectedTemplate,
        jobDescription
      })
    );
  }, [resumeData, enhancedResumeData, originalScore, enhancedScore, selectedTemplate, jobDescription]);

  const value = useMemo(
    () => ({
      resumeData,
      enhancedResumeData,
      originalScore,
      enhancedScore,
      selectedTemplate,
      jobDescription,
      setResumeData,
      setEnhancedResumeData,
      setOriginalScore,
      setEnhancedScore,
      setSelectedTemplate,
      setJobDescription,
      resetAll: () => {
        setResumeData(null);
        setEnhancedResumeData(null);
        setOriginalScore(null);
        setEnhancedScore(null);
        setSelectedTemplate('classic');
        setJobDescription('');
      }
    }),
    [resumeData, enhancedResumeData, originalScore, enhancedScore, selectedTemplate, jobDescription]
  );

  return <ResumeContext.Provider value={value}>{children}</ResumeContext.Provider>;
};

export const useResume = () => {
  const context = useContext(ResumeContext);
  if (!context) {
    throw new Error('useResume must be used within a ResumeProvider');
  }
  return context;
};
