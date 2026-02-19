'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const links = [
  { href: '/', label: 'Home' },
  { href: '/upload', label: 'Upload' },
  { href: '/manual', label: 'Manual Entry' },
  { href: '/enhance', label: 'Enhance' },
  { href: '/result', label: 'Result' }
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="border-b border-indigo-100 bg-white/90 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-lg font-bold text-indigo-700">
          ATS Resume Builder
        </Link>
        <div className="flex flex-wrap gap-2 text-sm">
          {links.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`rounded-full px-3 py-1.5 transition ${
                  active
                    ? 'bg-indigo-600 text-white'
                    : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      </nav>
    </header>
  );
}
