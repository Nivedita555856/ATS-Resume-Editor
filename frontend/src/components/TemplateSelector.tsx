'use client';

import { TemplateOption } from '@/types/resume';

interface Props {
  templates: TemplateOption[];
  selected: string;
  onSelect: (id: string) => void;
}

export default function TemplateSelector({ templates, selected, onSelect }: Props) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {templates.map((template) => {
        const isActive = selected === template.id;
        return (
          <button
            key={template.id}
            onClick={() => onSelect(template.id)}
            type="button"
            className={`rounded-xl border p-3 text-left transition ${
              isActive ? 'border-indigo-500 bg-indigo-50' : 'border-slate-200 bg-white hover:border-indigo-200'
            }`}
          >
            <img
              src={template.previewImage}
              alt={template.name}
              className="mb-3 h-36 w-full rounded-lg object-cover"
            />
            <h4 className="font-semibold text-slate-800">{template.name}</h4>
            <p className="text-sm text-slate-500">{template.description}</p>
          </button>
        );
      })}
    </div>
  );
}
