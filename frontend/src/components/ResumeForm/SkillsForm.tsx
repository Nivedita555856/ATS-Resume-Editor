'use client';

interface Props {
  value: string[];
  onChange: (next: string[]) => void;
}

export default function SkillsForm({ value, onChange }: Props) {
  const text = value.join(', ');
  return (
    <div>
      <label className="text-sm">
        <span className="mb-1 block font-medium text-slate-700">Skills (comma separated)</span>
        <textarea
          className="min-h-32 w-full rounded-lg border border-slate-300 px-3 py-2"
          value={text}
          onChange={(e) =>
            onChange(
              e.target.value
                .split(',')
                .map((item) => item.trim())
                .filter(Boolean)
            )
          }
        />
      </label>
    </div>
  );
}
