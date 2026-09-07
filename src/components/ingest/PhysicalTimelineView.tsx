import React from 'react';
import { PhysicalSourceTimeline, Observation, ReviewState } from '../../core/types';
import { Check, X, Edit, Spline, GitMerge, Flag, Tag } from 'lucide-react';

interface PhysicalTimelineViewProps {
  timeline: PhysicalSourceTimeline;
  onConfirm: (id: string) => void;
  onReject: (id: string) => void;
}

export function PhysicalTimelineView({ timeline, onConfirm, onReject }: PhysicalTimelineViewProps) {
  const observations = Object.values(timeline.observations).filter(o => o.reviewState !== 'REJECTED');

  const renderBadge = (state: ReviewState) => {
    switch(state) {
      case 'CONFIRMED': return <span className="px-2 py-0.5 bg-green-950 text-green-400 rounded text-[9px] font-bold uppercase">Confirmed</span>;
      case 'CORRECTED': return <span className="px-2 py-0.5 bg-blue-950 text-blue-400 rounded text-[9px] font-bold uppercase">Corrected</span>;
      case 'UNREVIEWED': return <span className="px-2 py-0.5 bg-neutral-800 text-neutral-400 rounded text-[9px] font-bold uppercase">Unreviewed</span>;
      default: return null;
    }
  };

  const renderOrigin = (origin: string) => {
    if (origin === 'MACHINE_GENERATED') return <span className="text-[10px] text-purple-400 font-mono">MACHINE</span>;
    return <span className="text-[10px] text-blue-400 font-mono">HUMAN</span>;
  };

  return (
    <div className="space-y-6">
      {timeline.clips.length === 0 ? (
        <div className="p-8 text-center border border-dashed border-neutral-800 rounded-lg text-neutral-500">
          No physical sources ingested yet.
        </div>
      ) : (
        <div className="space-y-8">
          {timeline.clips.map(clip => {
            const clipObs = observations.filter(o => o.sourceClipId === clip.id);
            return (
              <div key={clip.id} className="bg-neutral-900 border border-neutral-800 rounded-lg overflow-hidden">
                <div className="px-4 py-3 bg-black border-b border-neutral-800 flex items-center justify-between">
                  <div>
                    <div className="text-sm font-bold text-white font-mono">{clip.assetId}</div>
                    <div className="text-xs text-neutral-500 font-mono mt-1">Drive ID: {clip.id}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-mono text-neutral-400">Duration: {clip.endTimecode || 'Unknown'}</div>
                  </div>
                </div>
                
                <div className="p-4 space-y-4">
                  <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-widest">Physical Observations</h4>
                  
                  {clipObs.length === 0 ? (
                    <div className="text-xs text-neutral-600 font-mono italic">No observations cataloged.</div>
                  ) : (
                    <div className="space-y-2">
                      {clipObs.map(obs => (
                        <div key={obs.id} className="flex flex-col md:flex-row md:items-center justify-between p-3 bg-black border border-neutral-800 rounded">
                          <div className="flex-1 mb-3 md:mb-0">
                            <div className="flex items-center space-x-2 mb-1">
                              {renderOrigin(obs.origin)}
                              <span className="text-[10px] text-neutral-500 font-bold uppercase">{obs.type}</span>
                              {renderBadge(obs.reviewState)}
                            </div>
                            <div className="text-sm text-neutral-300">
                              {obs.type === 'EVENT' ? <span className="text-orange-400 font-bold">{(obs as any).eventLabel}</span> : obs.description}
                            </div>
                            {obs.confidence && (
                              <div className="text-[10px] text-neutral-600 font-mono mt-1">Confidence: {obs.confidence}</div>
                            )}
                          </div>
                          
                          <div className="flex items-center space-x-1 shrink-0">
                            <button onClick={() => onConfirm(obs.id)} className="p-1.5 bg-neutral-800 hover:bg-green-900 text-neutral-400 hover:text-green-400 rounded transition-colors" title="Confirm">
                              <Check size={14} />
                            </button>
                            <button className="p-1.5 bg-neutral-800 hover:bg-blue-900 text-neutral-400 hover:text-blue-400 rounded transition-colors" title="Edit">
                              <Edit size={14} />
                            </button>
                            <button className="p-1.5 bg-neutral-800 hover:bg-neutral-700 text-neutral-400 hover:text-white rounded transition-colors" title="Add Event Tag">
                              <Tag size={14} />
                            </button>
                            <button className="p-1.5 bg-neutral-800 hover:bg-neutral-700 text-neutral-400 hover:text-white rounded transition-colors" title="Split">
                              <Spline size={14} />
                            </button>
                            <button className="p-1.5 bg-neutral-800 hover:bg-neutral-700 text-neutral-400 hover:text-white rounded transition-colors" title="Merge">
                              <GitMerge size={14} />
                            </button>
                            <button className="p-1.5 bg-neutral-800 hover:bg-red-900 text-neutral-400 hover:text-red-400 rounded transition-colors" title="Flag">
                              <Flag size={14} />
                            </button>
                            <button onClick={() => onReject(obs.id)} className="p-1.5 bg-neutral-800 hover:bg-red-900 text-neutral-400 hover:text-red-400 rounded transition-colors" title="Reject">
                              <X size={14} />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
