'use client';

import { DragEvent, useRef, useState } from 'react';

interface FileUploaderProps {
  onFileSelected: (file: File) => Promise<void>;
  loading?: boolean;
}

const acceptedTypes = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
];

export default function FileUploader({ onFileSelected, loading = false }: FileUploaderProps) {
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [error, setError] = useState('');

  const validateAndUpload = async (file: File) => {
    if (!acceptedTypes.includes(file.type)) {
      setError('Only PDF and DOCX files are supported.');
      return;
    }
    setError('');
    await onFileSelected(file);
  };

  const handleDrop = async (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragActive(false);
    const file = event.dataTransfer.files?.[0];
    if (file) {
      await validateAndUpload(file);
    }
  };

  return (
    <div className="space-y-3">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`rounded-xl border-2 border-dashed p-8 text-center transition ${
          dragActive ? 'border-indigo-500 bg-indigo-50' : 'border-slate-300 bg-white'
        }`}
      >
        <p className="mb-2 text-lg font-semibold text-slate-700">Drop your resume here</p>
        <p className="mb-5 text-sm text-slate-500">Supports PDF and DOCX formats</p>
        <button
          type="button"
          disabled={loading}
          onClick={() => inputRef.current?.click()}
          className="rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-indigo-300"
        >
          {loading ? 'Uploading...' : 'Choose File'}
        </button>
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept=".pdf,.docx"
          onChange={async (e) => {
            const file = e.target.files?.[0];
            if (file) {
              await validateAndUpload(file);
            }
          }}
        />
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
