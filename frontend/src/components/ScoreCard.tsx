'use client';

interface ScoreCardProps {
  title: string;
  score: number;
}

export default function ScoreCard({ title, score }: ScoreCardProps) {
  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.max(0, Math.min(100, score)) / 100) * circumference;

  return (
    <div className="rounded-xl border border-indigo-100 bg-white p-5 shadow-sm">
      <h3 className="mb-3 font-semibold text-slate-700">{title}</h3>
      <div className="flex items-center justify-center">
        <svg width="140" height="140" viewBox="0 0 140 140" className="-rotate-90">
          <circle cx="70" cy="70" r={radius} stroke="#e2e8f0" strokeWidth="12" fill="none" />
          <circle
            cx="70"
            cy="70"
            r={radius}
            stroke="#4f46e5"
            strokeWidth="12"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute text-center">
          <p className="text-3xl font-bold text-indigo-700">{score}</p>
          <p className="text-sm text-slate-500">/ 100</p>
        </div>
      </div>
    </div>
  );
}
