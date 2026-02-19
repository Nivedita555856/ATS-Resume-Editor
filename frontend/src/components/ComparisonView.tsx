'use client';

import ReactDiffViewer from 'react-diff-viewer-continued';

interface Props {
  original: string;
  enhanced: string;
  splitView?: boolean;
}

export default function ComparisonView({ original, enhanced, splitView = true }: Props) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <ReactDiffViewer
        oldValue={original}
        newValue={enhanced}
        splitView={splitView}
        leftTitle="Original"
        rightTitle="Enhanced"
        hideLineNumbers={false}
      />
    </div>
  );
}
