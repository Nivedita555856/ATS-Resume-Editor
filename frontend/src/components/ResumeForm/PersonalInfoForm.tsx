'use client';

import { PersonalInfo } from '@/types/resume';

interface Props {
  value: PersonalInfo;
  onChange: (next: PersonalInfo) => void;
}

const fields: Array<{ key: keyof PersonalInfo; label: string; required?: boolean }> = [
  { key: 'full_name', label: 'Full Name', required: true },
  { key: 'email', label: 'Email', required: true },
  { key: 'phone', label: 'Phone', required: true },
  { key: 'location', label: 'Location', required: true },
  { key: 'linkedin', label: 'LinkedIn' },
  { key: 'github', label: 'GitHub' },
  { key: 'website', label: 'Website' },
  { key: 'summary', label: 'Professional Summary' }
];

export default function PersonalInfoForm({ value, onChange }: Props) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {fields.map((field) => (
        <label key={field.key} className={`text-sm ${field.key === 'summary' ? 'md:col-span-2' : ''}`}>
          <span className="mb-1 block font-medium text-slate-700">{field.label}</span>
          {field.key === 'summary' ? (
            <textarea
              required={field.required}
              value={value[field.key] || ''}
              onChange={(e) => onChange({ ...value, [field.key]: e.target.value })}
              className="min-h-24 w-full rounded-lg border border-slate-300 px-3 py-2"
            />
          ) : (
            <input
              required={field.required}
              value={value[field.key] || ''}
              onChange={(e) => onChange({ ...value, [field.key]: e.target.value })}
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
            />
          )}
        </label>
      ))}
    </div>
  );
}
