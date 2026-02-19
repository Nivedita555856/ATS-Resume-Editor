'use client';

import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import LivePreview from '@/components/LivePreview';
import ScoreCard from '@/components/ScoreCard';
import TemplateSelector from '@/components/TemplateSelector';
import { useResume } from '@/context/ResumeContext';
import { enhanceResume, getATSScore } from '@/lib/api';
import { TemplateOption } from '@/types/resume';

const templates: TemplateOption[] = [
  {
    id: 'classic',
    name: 'Classic Pro',
    description: 'Traditional single-column layout with strong ATS structure.',
    previewImage:
      'https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=900&q=80'
  },
  {
    id: 'modern',
    name: 'Modern Edge',
    description: 'Balanced spacing and modern typography for clarity.',
    previewImage:
      'https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=900&q=80'
  },
  {
    id: 'minimal',
    name: 'Minimal Focus',
    description: 'Minimal aesthetic emphasizing content over design.',
    previewImage:
      'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=900&q=80'
  }
];

export default function EnhancePage() {
  const router = useRouter();
  const {
    resumeData,
    enhancedResumeData,
    originalScore,
    enhancedScore,
    selectedTemplate,
    jobDescription,
    setOriginalScore,
    setEnhancedScore,
    setEnhancedResumeData,
    setSelectedTemplate,
    setJobDescription
  } = useResume();

  const [loadingScore, setLoadingScore] = useState(false);
  const [enhancing, setEnhancing] = useState(false);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!resumeData) {
      router.replace('/');
      return;
    }
    if (!originalScore) {
      setLoadingScore(true);
      getATSScore(resumeData)
        .then((score) => setOriginalScore(score))
        .catch(() => toast.error('Could not load ATS score.'))
        .finally(() => setLoadingScore(false));
    }
  }, [resumeData, originalScore, router, setOriginalScore]);

  const progressLabel = useMemo(() => {
    if (progress < 30) return 'Analyzing resume structure...';
    if (progress < 65) return 'Optimizing ATS keyword relevance...';
    if (progress < 90) return 'Generating enhanced resume draft...';
    return 'Finalizing and scoring...';
  }, [progress]);

  const handleEnhance = async () => {
    if (!resumeData) return;
    setEnhancing(true);
    setProgress(10);
    const timer = setInterval(() => {
      setProgress((prev) => (prev >= 90 ? prev : prev + 10));
    }, 500);

    try {
      const response = await enhanceResume({
        resume_data: resumeData,
        job_description: jobDescription,
        template: selectedTemplate
      });

      setEnhancedResumeData(response.enhanced_resume_data);
      setEnhancedScore(response.score);
      setProgress(100);
      toast.success('Resume enhanced successfully!');
      router.push('/result');
    } catch (error) {
      toast.error('Enhancement failed. Please try again.');
    } finally {
      clearInterval(timer);
      setEnhancing(false);
    }
  };

  if (!resumeData) return null;

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-800">Enhance Your Resume</h1>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="mb-2 font-semibold">Original ATS Score</h2>
          {loadingScore ? (
            <div className="flex items-center gap-3 text-slate-600">
              <div className="spinner" /> Calculating score...
            </div>
          ) : originalScore ? (
            <ScoreCard title="Current Score" score={originalScore.score} />
          ) : (
            <p className="text-sm text-slate-500">Score unavailable.</p>
          )}
        </div>
        <LivePreview resumeData={enhancedResumeData ?? resumeData} />
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5">
        <label className="text-sm">
          <span className="mb-2 block font-medium text-slate-700">Job Description (optional)</span>
          <textarea
            className="min-h-32 w-full rounded-lg border border-slate-300 px-3 py-2"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the target job description to improve matching..."
          />
        </label>
      </div>

      <div className="space-y-3 rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="font-semibold">Choose a Resume Template</h2>
        <TemplateSelector templates={templates} selected={selectedTemplate} onSelect={setSelectedTemplate} />
      </div>

      {enhancing && (
        <div className="space-y-2 rounded-xl border border-indigo-100 bg-indigo-50 p-4">
          <div className="h-2 w-full rounded-full bg-indigo-100">
            <div className="h-2 rounded-full bg-indigo-600" style={{ width: `${progress}%` }} />
          </div>
          <p className="text-sm text-indigo-700">{progressLabel}</p>
        </div>
      )}

      <button
        onClick={handleEnhance}
        disabled={enhancing || loadingScore}
        className="rounded-lg bg-indigo-600 px-5 py-3 font-semibold text-white disabled:bg-indigo-300"
      >
        {enhancing ? 'Enhancing...' : 'Enhance & Generate'}
      </button>
    </section>
  );
}
