'use client';

import { Experience } from '@/types/resume';

interface Props {
  value: Experience[];
  onChange: (next: Experience[]) => void;
}

const emptyExperience: Experience = {
  company: '',
  title: '',
  start_date: '',
  end_date: '',
  location: '',
  responsibilities: ['']
};

export default function ExperienceForm({ value, onChange }: Props) {
  const items = value.length ? value : [emptyExperience];

  return (
    <div className="space-y-4">
      {items.map((item, index) => (
        <div key={index} className="space-y-3 rounded-lg border border-slate-200 p-4">
          {['company', 'title', 'start_date', 'end_date', 'location'].map((key) => (
            <input
              key={key}
              placeholder={key.replace('_', ' ')}
              value={(item as Record<string, string>)[key] || ''}
              onChange={(e) => {
                const next = [...items];
                (next[index] as Record<string, string>)[key] = e.target.value;
                onChange(next);
              }}
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
            />
          ))}
          <textarea
            placeholder="Responsibilities (one per line)"
            value={item.responsibilities.join('\n')}
            onChange={(e) => {
              const next = [...items];
              next[index].responsibilities = e.target.value.split('\n').filter(Boolean);
              onChange(next);
            }}
            className="min-h-24 w-full rounded-lg border border-slate-300 px-3 py-2"
          />
        </div>
      ))}
      <button
        type="button"
        onClick={() => onChange([...items, { ...emptyExperience }])}
        className="rounded-lg border border-indigo-300 px-3 py-2 text-indigo-700"
      >
        + Add Experience
      </button>
    </div>
  );
}
