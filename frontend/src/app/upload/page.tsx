'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { toast } from 'react-hot-toast';
import FileUploader from '@/components/FileUploader';
import { useResume } from '@/context/ResumeContext';
import { uploadResume } from '@/lib/api';

export default function UploadPage() {
  const router = useRouter();
  const { setResumeData, setEnhancedResumeData, setOriginalScore, setEnhancedScore } = useResume();
  const [loading, setLoading] = useState(false);

  const handleFile = async (file: File) => {
    try {
      setLoading(true);
      const response = await uploadResume(file);
      setResumeData(response.resume_data);
      setEnhancedResumeData(null);
      setOriginalScore(null);
      setEnhancedScore(null);
      toast.success('Resume parsed successfully.');
      router.push('/enhance');
    } catch (error) {
      toast.error('Upload failed. Please try another file.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mx-auto max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-slate-800">Upload Your Resume</h1>
      <p className="text-slate-600">Drag and drop your resume to parse content instantly.</p>
      <FileUploader onFileSelected={handleFile} loading={loading} />
    </section>
  );
}
