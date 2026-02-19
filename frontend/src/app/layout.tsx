import type { Metadata } from 'next';
import { Toaster } from 'react-hot-toast';
import Navbar from '@/components/Navbar';
import { ResumeProvider } from '@/context/ResumeContext';
import './globals.css';

export const metadata: Metadata = {
  title: 'ATS Resume Builder',
  description: 'Create and optimize resumes with AI and ATS scoring.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ResumeProvider>
          <Navbar />
          <main className="mx-auto min-h-[calc(100vh-73px)] max-w-6xl px-4 py-8">{children}</main>
          <Toaster position="top-right" />
        </ResumeProvider>
      </body>
    </html>
  );
}
