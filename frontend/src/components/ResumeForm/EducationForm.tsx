'use client';

import { Education } from '@/types/resume';

interface Props {
  value: Education[];
  onChange: (next: Education[]) => void;
}

const emptyEducation: Education = {
  institution: '',
  degree: '',
  field_of_study: '',
  start_date: '',
  end_date: '',
  grade: '',
  description: ''
};

export default function EducationForm({ value, onChange }: Props) {
  const items = value.length ? value : [emptyEducation];
  return (
    <div className="space-y-4">
      {items.map((item, index) => (
        <div key={index} className="rounded-lg border border-slate-200 p-4">
          <div className="grid gap-3 md:grid-cols-2">
            {Object.keys(emptyEducation).map((key) => (
              <input
                key={key}
                placeholder={key.replaceAll('_', ' ')}
                value={(item as Record<string, string>)[key] || ''}
                onChange={(e) => {
                  const next = [...items];
                  (next[index] as Record<string, string>)[key] = e.target.value;
                  onChange(next);
                }}
                className="rounded-lg border border-slate-300 px-3 py-2"
              />
            ))}
          </div>
        </div>
      ))}
      <button
        type="button"
        onClick={() => onChange([...items, { ...emptyEducation }])}
        className="rounded-lg border border-indigo-300 px-3 py-2 text-indigo-700"
      >
        + Add Education
      </button>
    </div>
  );
}
