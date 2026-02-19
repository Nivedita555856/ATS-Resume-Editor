'use client';

interface FormStepperProps {
  currentStep: number;
  steps: string[];
  onBack: () => void;
  onNext: () => void;
  isFirst: boolean;
  isLast: boolean;
}

export default function FormStepper({
  currentStep,
  steps,
  onBack,
  onNext,
  isFirst,
  isLast
}: FormStepperProps) {
  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-2">
        {steps.map((step, index) => {
          const active = index === currentStep;
          const done = index < currentStep;
          return (
            <div
              key={step}
              className={`rounded-full px-3 py-1 text-sm ${
                active
                  ? 'bg-indigo-600 text-white'
                  : done
                    ? 'bg-indigo-100 text-indigo-700'
                    : 'bg-slate-100 text-slate-500'
              }`}
            >
              {index + 1}. {step}
            </div>
          );
        })}
      </div>
      <div className="flex justify-between">
        <button
          onClick={onBack}
          disabled={isFirst}
          className="rounded-lg border border-slate-300 px-4 py-2 text-slate-700 disabled:opacity-50"
        >
          Back
        </button>
        <button onClick={onNext} className="rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700">
          {isLast ? 'Submit' : 'Next'}
        </button>
      </div>
    </div>
  );
}
