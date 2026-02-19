'use client';

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

interface Props {
  original: number;
  enhanced: number;
}

export default function ScoreTracker({ original, enhanced }: Props) {
  const data = [
    { name: 'Original', score: original },
    { name: 'Enhanced', score: enhanced }
  ];

  return (
    <div className="h-72 rounded-xl border border-indigo-100 bg-white p-4 shadow-sm">
      <h3 className="mb-3 font-semibold text-slate-700">Score Comparison</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Bar dataKey="score" fill="#4f46e5" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
