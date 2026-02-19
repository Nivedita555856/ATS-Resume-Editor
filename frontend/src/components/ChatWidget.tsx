'use client';

import { FormEvent, useState } from 'react';

interface Message {
  role: 'user' | 'assistant';
  text: string;
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', text: 'Ask me how to further improve your resume for ATS.' }
  ]);
  const [input, setInput] = useState('');

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userText = input.trim();
    setMessages((prev) => [
      ...prev,
      { role: 'user', text: userText },
      {
        role: 'assistant',
        text: 'Great point. Emphasize measurable achievements and tailor keywords to the job description.'
      }
    ]);
    setInput('');
  };

  return (
    <div className="fixed bottom-5 right-5 z-50">
      {open && (
        <div className="mb-3 w-80 rounded-xl border border-slate-200 bg-white shadow-xl">
          <div className="border-b border-slate-100 p-3 font-semibold text-indigo-700">AI Resume Coach</div>
          <div className="max-h-64 space-y-2 overflow-y-auto p-3 text-sm">
            {messages.map((message, idx) => (
              <div
                key={idx}
                className={`rounded-lg p-2 ${
                  message.role === 'assistant' ? 'bg-indigo-50 text-indigo-900' : 'bg-slate-100 text-slate-800'
                }`}
              >
                {message.text}
              </div>
            ))}
          </div>
          <form onSubmit={onSubmit} className="flex gap-2 border-t border-slate-100 p-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 rounded-lg border border-slate-300 px-3 py-2"
              placeholder="Ask for suggestions..."
            />
            <button className="rounded-lg bg-indigo-600 px-3 py-2 text-white">Send</button>
          </form>
        </div>
      )}
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="rounded-full bg-indigo-600 px-4 py-3 font-semibold text-white shadow-lg hover:bg-indigo-700"
      >
        {open ? 'Close Chat' : 'AI Chat'}
      </button>
    </div>
  );
}
