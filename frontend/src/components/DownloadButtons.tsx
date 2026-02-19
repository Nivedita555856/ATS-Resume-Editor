'use client';

import { useState } from 'react';
import { toast } from 'react-hot-toast';
import { downloadResume } from '@/lib/api';
import { ResumeData } from '@/types/resume';

interface Props {
  resumeData: ResumeData;
}

export default function DownloadButtons({ resumeData }: Props) {
  const [loadingFormat, setLoadingFormat] = useState<'pdf' | 'docx' | null>(null);

  const handleDownload = async (format: 'pdf' | 'docx') => {
    try {
      setLoadingFormat(format);
      const response = await downloadResume(resumeData, format);
      window.open(response.url, '_blank');
      toast.success(`${format.toUpperCase()} download is ready`);
    } catch (error) {
      toast.error('Failed to generate download file.');
    } finally {
      setLoadingFormat(null);
    }
  };

  return (
    <div className="flex flex-wrap gap-3">
      <button
        onClick={() => handleDownload('pdf')}
        disabled={loadingFormat !== null}
        className="rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white disabled:bg-indigo-300"
      >
        {loadingFormat === 'pdf' ? 'Preparing PDF...' : 'Download PDF'}
      </button>
      <button
        onClick={() => handleDownload('docx')}
        disabled={loadingFormat !== null}
        className="rounded-lg border border-indigo-600 px-4 py-2 font-medium text-indigo-700 disabled:opacity-50"
      >
        {loadingFormat === 'docx' ? 'Preparing DOCX...' : 'Download DOCX'}
      </button>
    </div>
  );
}
