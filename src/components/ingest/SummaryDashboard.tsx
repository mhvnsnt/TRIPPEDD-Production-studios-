import React from 'react';
import { Database, FileVideo, Activity, Hash, Layers, List } from 'lucide-react';
import { PhysicalSourceTimeline } from '../../core/types';

interface SummaryDashboardProps {
  timeline: PhysicalSourceTimeline;
  totalDriveFiles: number;
}

export function SummaryDashboard({ timeline, totalDriveFiles }: SummaryDashboardProps) {
  const observations = Object.values(timeline.observations);
  const shots = observations.filter(o => o.type === 'SHOT');
  const transcripts = observations.filter(o => o.type === 'TRANSCRIPT');
  const events = observations.filter(o => o.type === 'EVENT');
  
  const confirmed = observations.filter(o => o.reviewState === 'CONFIRMED').length;
  const unreviewed = observations.filter(o => o.reviewState === 'UNREVIEWED').length;
  const rejected = observations.filter(o => o.reviewState === 'REJECTED').length;
  const corrected = observations.filter(o => o.reviewState === 'CORRECTED').length;

  const StatBox = ({ label, value, icon: Icon, colorClass = "text-blue-500" }: any) => (
    <div className="bg-black border border-neutral-800 rounded-lg p-4 flex items-center justify-between">
      <div>
        <div className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest mb-1">{label}</div>
        <div className="text-xl font-mono text-white">{value}</div>
      </div>
      <Icon size={24} className={colorClass} />
    </div>
  );

  return (
    <div className="space-y-6">
      <h2 className="text-sm font-bold text-neutral-500 uppercase tracking-widest flex items-center">
        <Database size={16} className="mr-2" /> Ingestion Telemetry
      </h2>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatBox label="Source Files" value={totalDriveFiles} icon={FileVideo} />
        <StatBox label="Analyzed & Hashed" value={timeline.clips.length} icon={Hash} colorClass="text-green-500" />
        <StatBox label="Detected Shots" value={shots.length} icon={Layers} colorClass="text-purple-500" />
        <StatBox label="Transcript Segs" value={transcripts.length} icon={List} colorClass="text-yellow-500" />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
        <StatBox label="Physical Events" value={events.length} icon={Activity} colorClass="text-orange-500" />
        <StatBox label="Human Confirmed" value={confirmed} icon={Database} colorClass="text-green-400" />
        <StatBox label="Human Corrected" value={corrected} icon={Database} colorClass="text-blue-400" />
        <StatBox label="Unreviewed" value={unreviewed} icon={Database} colorClass="text-neutral-400" />
      </div>
    </div>
  );
}
