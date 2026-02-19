'use client';

import { Project } from '@/types/resume';

interface Props {
  value: Project[];
  onChange: (next: Project[]) => void;
}

const emptyProject: Project = {
  name: '',
  description: '',
  technologies: [],
  link: ''
};

export default function ProjectsForm({ value, onChange }: Props) {
  const items = value.length ? value : [emptyProject];

  return (
    <div className="space-y-4">
      {items.map((item, index) => (
        <div key={index} className="space-y-3 rounded-lg border border-slate-200 p-4">
          <input
            placeholder="Project name"
            value={item.name}
            onChange={(e) => {
              const next = [...items];
              next[index].name = e.target.value;
              onChange(next);
            }}
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
          />
          <textarea
            placeholder="Description"
            value={item.description}
            onChange={(e) => {
              const next = [...items];
              next[index].description = e.target.value;
              onChange(next);
            }}
            className="min-h-20 w-full rounded-lg border border-slate-300 px-3 py-2"
          />
          <input
            placeholder="Technologies (comma separated)"
            value={item.technologies.join(', ')}
            onChange={(e) => {
              const next = [...items];
              next[index].technologies = e.target.value.split(',').map((t) => t.trim()).filter(Boolean);
              onChange(next);
            }}
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
          />
          <input
            placeholder="Project link"
            value={item.link || ''}
            onChange={(e) => {
              const next = [...items];
              next[index].link = e.target.value;
              onChange(next);
            }}
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
          />
        </div>
      ))}
      <button
        type="button"
        onClick={() => onChange([...items, { ...emptyProject }])}
        className="rounded-lg border border-indigo-300 px-3 py-2 text-indigo-700"
      >
        + Add Project
      </button>
    </div>
  );
}
