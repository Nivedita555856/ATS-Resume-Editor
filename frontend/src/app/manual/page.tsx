'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { toast } from 'react-hot-toast';
import EducationForm from '@/components/ResumeForm/EducationForm';
import ExperienceForm from '@/components/ResumeForm/ExperienceForm';
import FormStepper from '@/components/ResumeForm/FormStepper';
import PersonalInfoForm from '@/components/ResumeForm/PersonalInfoForm';
import ProjectsForm from '@/components/ResumeForm/ProjectsForm';
import SkillsForm from '@/components/ResumeForm/SkillsForm';
import { useResume } from '@/context/ResumeContext';
import { ResumeData } from '@/types/resume';

const steps = ['Personal Info', 'Education', 'Skills', 'Experience', 'Projects'];

const initialResumeData: ResumeData = {
  personal_info: {
    full_name: '',
    email: '',
    phone: '',
    location: '',
    linkedin: '',
    github: '',
    website: '',
    summary: ''
  },
  skills: [],
  education: [],
  experience: [],
  projects: []
};

export default function ManualPage() {
  const router = useRouter();
  const { setResumeData, resumeData } = useResume();
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<ResumeData>(resumeData ?? initialResumeData);

  const validateStep = () => {
    if (currentStep === 0) {
      const { full_name, email, phone, location } = formData.personal_info;
      return full_name && email && phone && location;
    }
    return true;
  };

  const handleNext = () => {
    if (!validateStep()) {
      toast.error('Please complete required fields before continuing.');
      return;
    }
    if (currentStep === steps.length - 1) {
      setResumeData(formData);
      toast.success('Resume details saved.');
      router.push('/enhance');
      return;
    }
    setCurrentStep((prev) => prev + 1);
  };

  return (
    <section className="mx-auto max-w-4xl space-y-6">
      <h1 className="text-2xl font-bold text-slate-800">Enter Resume Manually</h1>
      <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
        {currentStep === 0 && (
          <PersonalInfoForm
            value={formData.personal_info}
            onChange={(next) => setFormData((prev) => ({ ...prev, personal_info: next }))}
          />
        )}
        {currentStep === 1 && (
          <EducationForm
            value={formData.education}
            onChange={(next) => setFormData((prev) => ({ ...prev, education: next }))}
          />
        )}
        {currentStep === 2 && (
          <SkillsForm
            value={formData.skills}
            onChange={(next) => setFormData((prev) => ({ ...prev, skills: next }))}
          />
        )}
        {currentStep === 3 && (
          <ExperienceForm
            value={formData.experience}
            onChange={(next) => setFormData((prev) => ({ ...prev, experience: next }))}
          />
        )}
        {currentStep === 4 && (
          <ProjectsForm
            value={formData.projects}
            onChange={(next) => setFormData((prev) => ({ ...prev, projects: next }))}
          />
        )}
      </div>
      <FormStepper
        currentStep={currentStep}
        steps={steps}
        onBack={() => setCurrentStep((prev) => Math.max(0, prev - 1))}
        onNext={handleNext}
        isFirst={currentStep === 0}
        isLast={currentStep === steps.length - 1}
      />
    </section>
  );
}
