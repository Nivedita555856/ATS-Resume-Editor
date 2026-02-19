import Link from 'next/link';

const features = [
  'Upload PDF/DOCX and auto-parse resume content',
  'Manual resume builder with step-by-step guidance',
  'ATS scoring before and after AI enhancement',
  'Template selection and export in PDF/DOCX'
];

export default function LandingPage() {
  return (
    <section className="space-y-10">
      <div className="rounded-2xl bg-gradient-to-r from-indigo-600 to-blue-500 p-8 text-white md:p-12">
        <h1 className="mb-4 text-3xl font-bold md:text-5xl">Build an ATS-Friendly Resume in Minutes</h1>
        <p className="max-w-2xl text-indigo-50">
          Upload your resume or create one from scratch, get AI-powered enhancements, and improve your ATS score.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link href="/upload" className="rounded-lg bg-white px-5 py-3 font-semibold text-indigo-700">
            Upload Resume
          </Link>
          <Link href="/manual" className="rounded-lg border border-white px-5 py-3 font-semibold text-white">
            Enter Manually
          </Link>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {features.map((feature) => (
          <div key={feature} className="rounded-xl border border-indigo-100 bg-white p-5 shadow-sm">
            <h3 className="font-medium text-slate-700">{feature}</h3>
          </div>
        ))}
      </div>
    </section>
  );
}
