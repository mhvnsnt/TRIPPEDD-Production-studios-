import React, { useState } from 'react';
import { EpisodeRegistry } from '../core/pipeline/episodes';
import { Film, FileVideo, ShieldAlert, Cpu, Frame } from 'lucide-react';
import { Episode, Segment } from '../core/types';

export function EpisodeWorkspace() {
  const episodes = EpisodeRegistry.getAllEpisodes();
  const [selectedEpisodeId, setSelectedEpisodeId] = useState<string | null>(episodes[0]?.id || null);

  const selectedEpisode = episodes.find(e => e.id === selectedEpisodeId);

  return (
    <div className="h-full flex flex-col bg-black text-white">
      <header className="px-6 py-4 border-b border-neutral-800 bg-black/50 backdrop-blur-md flex items-center justify-between shrink-0">
        <div>
          <h1 className="text-xl font-bold uppercase tracking-widest text-white flex items-center">
            <Film className="mr-3 text-purple-500" size={20} />
            Episode Pipeline
          </h1>
          <p className="text-neutral-400 text-sm mt-1">Orchestrating multi-format TRIPPEDD segments and tracking full provenance.</p>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Episodes Sidebar */}
        <div className="w-80 border-r border-neutral-800 bg-neutral-900/50 flex flex-col p-4 space-y-2 overflow-y-auto custom-scrollbar">
          <div className="text-[10px] font-bold text-neutral-600 mb-2 tracking-widest uppercase">Episodes</div>
          {episodes.map(ep => (
            <button
              key={ep.id}
              onClick={() => setSelectedEpisodeId(ep.id)}
              className={`w-full text-left p-3 rounded border transition-colors ${selectedEpisodeId === ep.id ? 'bg-purple-900/20 border-purple-500/50' : 'bg-neutral-800/50 border-neutral-800 hover:border-neutral-700'}`}
            >
              <div className="flex items-center text-sm font-bold text-white mb-1">
                <span className="text-purple-400 mr-2">{ep.id}</span>
                {ep.name}
              </div>
              <div className="text-xs text-neutral-500 truncate">{ep.description}</div>
              <div className="mt-2 inline-block px-2 py-0.5 bg-neutral-800 text-[10px] font-bold rounded uppercase">
                {ep.status}
              </div>
            </button>
          ))}
        </div>

        {/* Segments View */}
        <div className="flex-1 p-6 overflow-y-auto custom-scrollbar">
          {selectedEpisode && (
            <div className="max-w-4xl mx-auto">
              <div className="mb-8">
                <h2 className="text-2xl font-black uppercase tracking-tight mb-2">EPISODE {selectedEpisode.number}: {selectedEpisode.name}</h2>
                <p className="text-neutral-400">{selectedEpisode.description}</p>
              </div>

              <div className="space-y-6">
                {selectedEpisode.segments.map((segment, idx) => (
                  <SegmentCard key={segment.id} segment={segment} index={idx} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function SegmentCard({ segment, index }: { segment: Segment, index: number, key?: string | number }) {
  const getBadgeColor = (status: string) => {
    switch (status) {
      case 'FACTUAL': return 'text-green-400 bg-green-950/50 border-green-900/50';
      case 'FICTIONAL': return 'text-purple-400 bg-purple-950/50 border-purple-900/50';
      case 'RECONSTRUCTED': return 'text-yellow-400 bg-yellow-950/50 border-yellow-900/50';
      case 'PURE_ANIMATION': return 'text-pink-400 bg-pink-950/50 border-pink-900/50';
      case 'PURE_LIVE_ACTION': return 'text-green-400 bg-green-950/50 border-green-900/50';
      default: return 'text-neutral-400 bg-neutral-900 border-neutral-800';
    }
  };

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-5">
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="flex items-center text-neutral-500 font-bold text-xs mb-1">
            <span className="mr-2">SEGMENT {index + 1}</span>
            <span className="text-neutral-600">•</span>
            <span className="ml-2 font-mono text-blue-400">{segment.id}</span>
          </div>
          <h3 className="text-lg font-bold text-white uppercase">{segment.name}</h3>
        </div>
        <div className="flex space-x-2">
          {segment.formatId && (
            <span className="px-2 py-1 bg-neutral-800 border border-neutral-700 rounded text-[10px] font-bold text-neutral-300">
              {segment.formatId}
            </span>
          )}
          {segment.locationId && (
            <span className="px-2 py-1 bg-blue-950/30 border border-blue-900/50 rounded text-[10px] font-bold text-blue-300">
              LOC: {segment.locationId}
            </span>
          )}
        </div>
      </div>
      
      <p className="text-sm text-neutral-400 mb-6">{segment.description}</p>

      {/* Ontology tags */}
      <div className="flex flex-wrap gap-2 mb-6">
        <div className={`px-2 py-1 border rounded text-[10px] font-bold ${getBadgeColor(segment.provenance.realityStatus)}`}>
          REALITY: {segment.provenance.realityStatus}
        </div>
        <div className={`px-2 py-1 border rounded text-[10px] font-bold ${getBadgeColor(segment.provenance.assemblyMode)}`}>
          ASSEMBLY: {segment.provenance.assemblyMode}
        </div>
        <div className={`px-2 py-1 border rounded text-[10px] font-bold ${segment.provenance.aiContributions.includes('NONE') ? 'text-neutral-400 bg-neutral-800 border-neutral-700' : 'text-blue-400 bg-blue-950 border-blue-900'}`}>
          AI: {segment.provenance.aiContributions.join(', ')}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {segment.sourceClips.length > 0 && (
          <div className="bg-black/50 rounded p-3 border border-neutral-800/50">
            <h4 className="text-xs font-bold text-neutral-500 uppercase flex items-center mb-2">
              <FileVideo size={12} className="mr-1.5" /> Source Material
            </h4>
            {segment.sourceClips.map(clip => (
              <div key={clip.id} className="text-xs text-neutral-300 font-mono">
                {clip.id} <span className="text-neutral-600">({clip.startTimecode} - {clip.endTimecode})</span>
              </div>
            ))}
          </div>
        )}
        
        {segment.performances.length > 0 && (
          <div className="bg-black/50 rounded p-3 border border-neutral-800/50">
            <h4 className="text-xs font-bold text-neutral-500 uppercase flex items-center mb-2">
              <Frame size={12} className="mr-1.5" /> Captured Performances
            </h4>
            {segment.performances.map(perf => (
              <div key={perf.id} className="text-xs text-neutral-300">
                <span className="font-bold text-white">{perf.personId}</span> as <span className="text-blue-400">{perf.characterId}</span>
              </div>
            ))}
          </div>
        )}

        {segment.gags.length > 0 && (
          <div className="col-span-full bg-black/50 rounded p-3 border border-neutral-800/50">
            <h4 className="text-xs font-bold text-neutral-500 uppercase flex items-center mb-2">
              <ShieldAlert size={12} className="mr-1.5 text-yellow-500" /> Embedded Gags
            </h4>
            {segment.gags.map(gag => (
              <div key={gag.id} className="text-xs text-neutral-300">
                <span className="font-bold text-white mr-2">{gag.name}</span>
                <span className="px-1.5 py-0.5 bg-neutral-800 rounded text-[9px] text-neutral-400">{gag.type}</span>
                {gag.sourceMaterial && gag.sourceMaterial.length > 0 && (
                   <div className="mt-1 ml-4 text-[10px] text-green-400/80 border-l border-green-900 pl-2 py-0.5">
                     Ingesting Factual Clip: {gag.sourceMaterial[0].id}
                   </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
