import React from 'react';
import { StoryboardComparisonResult } from '../../core/types';
import { LayoutList, CheckCircle, AlertTriangle, HelpCircle, XCircle } from 'lucide-react';

interface StoryboardComparisonProps {
  results: StoryboardComparisonResult[];
}

export function StoryboardComparison({ results }: StoryboardComparisonProps) {
  const renderIcon = (status: string) => {
    switch (status) {
      case 'MATCH': return <CheckCircle className="text-green-500" size={16} />;
      case 'CHRONOLOGY_DISCREPANCY': return <AlertTriangle className="text-yellow-500" size={16} />;
      case 'EXPECTED_BUT_MISSING': return <XCircle className="text-red-500" size={16} />;
      case 'UNEXPECTED_PHYSICAL_MATERIAL': return <HelpCircle className="text-purple-500" size={16} />;
      default: return <HelpCircle className="text-neutral-500" size={16} />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-sm font-bold text-neutral-500 uppercase tracking-widest flex items-center">
          <LayoutList size={16} className="mr-2" /> Storyboard vs Physical Discrepancy Report
        </h2>
      </div>
      
      {results.length === 0 ? (
        <div className="p-8 text-center border border-dashed border-neutral-800 rounded-lg text-neutral-500 font-mono text-sm">
          No events mapped to storyboard expectations yet.
        </div>
      ) : (
        <div className="space-y-3">
          {results.map((res, i) => (
            <div key={i} className="flex flex-col md:flex-row md:items-center p-4 bg-neutral-900 border border-neutral-800 rounded-lg gap-4">
              <div className="shrink-0 pt-1 md:pt-0">
                {renderIcon(res.status)}
              </div>
              <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest mb-1">Storyboard Expects</div>
                  <div className="text-sm font-mono text-neutral-300">
                    {res.expectedEvent || <span className="text-neutral-600 italic">None</span>}
                  </div>
                </div>
                <div>
                  <div className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest mb-1">Physical Reality</div>
                  <div className="text-sm font-mono text-neutral-300">
                    {res.detectedEvent || <span className="text-neutral-600 italic">None</span>}
                  </div>
                </div>
              </div>
              <div className="shrink-0 flex items-center">
                <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
                  res.status === 'MATCH' ? 'bg-green-950 text-green-400' :
                  res.status === 'EXPECTED_BUT_MISSING' ? 'bg-red-950 text-red-400' :
                  res.status === 'CHRONOLOGY_DISCREPANCY' ? 'bg-yellow-950 text-yellow-400' :
                  'bg-purple-950 text-purple-400'
                }`}>
                  {res.status.replace(/_/g, ' ')}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
