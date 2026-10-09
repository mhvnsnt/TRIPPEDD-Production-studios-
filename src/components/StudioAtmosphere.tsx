import { useEffect, useState } from 'react';

const signals = [
  'PHYSICAL EVIDENCE',
  'STORY / RHYTHM',
  'MEDIA / IMAGE',
  '3D / MOTION',
  'SOUND / VOICE',
  'COLOR / MATTER',
  'AI / GENERATION',
  'QC / PROVENANCE',
];

export function StudioAtmosphere() {
  const [signal, setSignal] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => setSignal((value) => (value + 1) % signals.length), 2600);
    return () => window.clearInterval(id);
  }, []);

  return (
    <div className="studio-atmosphere" aria-hidden="true">
      <div className="studio-atmosphere__aurora" />
      <div className="studio-atmosphere__grain" />
      <div className="studio-atmosphere__orb studio-atmosphere__orb--a" />
      <div className="studio-atmosphere__orb studio-atmosphere__orb--b" />
      <div className="studio-atmosphere__signal">
        <span className="studio-atmosphere__dot" />
        <span>{signals[signal]}</span>
      </div>
      <div className="studio-atmosphere__axis" />
    </div>
  );
}
