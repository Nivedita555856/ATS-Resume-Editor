'use client';

import { ResumeData } from '@/types/resume';

interface Props {
  resumeData: ResumeData | null;
  title?: string;
}

export default function LivePreview({ resumeData, title = 'Live Preview' }: Props) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <h3 className="mb-3 font-semibold text-slate-700">{title}</h3>
      {!resumeData ? (
        <p className="text-sm text-slate-500">No resume data available yet.</p>
      ) : (
        <div className="space-y-3 text-sm text-slate-700">
          <section>
            <h4 className="font-semibold">{resumeData.personal_info.full_name}</h4>
            <p>{resumeData.personal_info.email}</p>
            <p>{resumeData.personal_info.summary}</p>
          </section>
          <section>
            <h5 className="font-medium">Skills</h5>
            <p>{resumeData.skills.join(', ')}</p>
          </section>
          <section>
            <h5 className="font-medium">Experience</h5>
            <ul className="list-disc pl-5">
              {resumeData.experience.map((exp, idx) => (
                <li key={`${exp.company}-${idx}`}>
                  {exp.title} at {exp.company}
                </li>
              ))}
            </ul>
          </section>
        </div>
      )}
    </div>
  );
}
