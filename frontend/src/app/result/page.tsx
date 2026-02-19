'use client';

import { useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import ChatWidget from '@/components/ChatWidget';
import ComparisonView from '@/components/ComparisonView';
import DownloadButtons from '@/components/DownloadButtons';
import LivePreview from '@/components/LivePreview';
import ScoreCard from '@/components/ScoreCard';
import ScoreTracker from '@/components/ScoreTracker';
import { useResume } from '@/context/ResumeContext';

const prettyStringify = (input: unknown) => JSON.stringify(input, null, 2);

export default function ResultPage() {
  const router = useRouter();
  const { resumeData, enhancedResumeData, originalScore, enhancedScore } = useResume();
  const [splitView, setSplitView] = useState(true);

  const originalText = useMemo(() => prettyStringify(resumeData), [resumeData]);
  const enhancedText = useMemo(() => prettyStringify(enhancedResumeData), [enhancedResumeData]);

  if (!resumeData || !enhancedResumeData || !originalScore || !enhancedScore) {
    return (
      <section className="space-y-4">
        <h1 className="text-2xl font-bold">No enhanced resume available</h1>
        <p className="text-slate-600">Upload or create a resume and run enhancement first.</p>
        <button
          onClick={() => router.push('/')}
          className="rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white"
        >
          Go to Home
        </button>
      </section>
    );
  }

  return (
    <section className="space-y-6 pb-24">
      <h1 className="text-2xl font-bold text-slate-800">Your Enhanced Resume</h1>

      <div className="grid gap-4 md:grid-cols-2">
        <ScoreCard title="Original ATS Score" score={originalScore.score} />
        <ScoreCard title="Enhanced ATS Score" score={enhancedScore.score} />
      </div>

      <ScoreTracker original={originalScore.score} enhanced={enhancedScore.score} />

      <div className="rounded-xl border border-slate-200 bg-white p-5">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="font-semibold">Resume Comparison</h2>
          <button
            onClick={() => setSplitView((prev) => !prev)}
            className="rounded-lg border border-indigo-300 px-3 py-2 text-sm text-indigo-700"
          >
            Toggle {splitView ? 'Inline View' : 'Side-by-Side View'}
          </button>
        </div>
        <ComparisonView original={originalText} enhanced={enhancedText} splitView={splitView} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <LivePreview resumeData={resumeData} title="Original Preview" />
        <LivePreview resumeData={enhancedResumeData} title="Enhanced Preview" />
      </div>

      <DownloadButtons resumeData={enhancedResumeData} />
      <ChatWidget />
    </section>
  );
}
