import { CheckSquare, Square, Video, Plus, Wand2, ShieldAlert, ShieldCheck } from 'lucide-react';
import { useState } from 'react';
import { useProduction } from '../context';

export function ActiveProduction() {
  const [activeShot, setActiveShot] = useState<string | null>(null);
  const { records } = useProduction();

  const shots = records.filter(r => r.type === 'SHOT');
  const activeRecord = shots.find(s => s.id === activeShot);
  const verifiedCount = shots.filter(s => s.verified && s.status === 'COMPLETED').length;

  return (
    <div className="p-8 max-w-6xl mx-auto w-full space-y-8">
      <header className="border-b border-neutral-800 pb-6 flex justify-between items-end">
        <div>
          <div className="text-sm font-bold text-neutral-500 tracking-widest mb-2">PRODUCTION TERMINAL</div>
          <h2 className="text-4xl font-black tracking-tight text-white">EPISODE 01 — THE WALK</h2>
        </div>
        <button className="bg-neutral-800 hover:bg-neutral-700 text-white px-4 py-2 rounded font-bold text-sm transition-colors flex items-center gap-2 border border-neutral-700">
          <Wand2 size={16} />
          GENERATE TRIPPEDD TIMELINE
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Shot List */}
        <div className="lg:col-span-1 space-y-4">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center justify-between">
            SHOT LIST
            <span className="text-xs font-mono text-neutral-500">{verifiedCount}/{shots.length} VERIFIED</span>
          </h3>
          
          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-2">
            {shots.map((shot) => {
              const isVerified = shot.verified === true && shot.status === 'COMPLETED';
              const isFiction = shot.verified === 'not_applicable';
              return (
                <button 
                  key={shot.id}
                  onClick={() => setActiveShot(shot.id)}
                  className={`w-full flex items-center justify-between p-3 rounded border text-left transition-colors ${
                    activeShot === shot.id 
                      ? 'bg-neutral-800 border-neutral-600' 
                      : 'bg-neutral-900 border-neutral-800 hover:border-neutral-700'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    {isVerified ? (
                      <ShieldCheck size={18} className="text-emerald-500 mt-0.5 shrink-0" />
                    ) : isFiction ? (
                      <Wand2 size={18} className="text-fuchsia-500 mt-0.5 shrink-0" />
                    ) : (
                      <ShieldAlert size={18} className="text-amber-500 mt-0.5 shrink-0" />
                    )}
                    <div>
                      <div className="text-xs font-mono text-neutral-500 mb-0.5 flex items-center gap-2">
                        {shot.id.toUpperCase()} 
                        <span className="text-[9px] bg-neutral-950 px-1.5 py-0.5 rounded border border-neutral-800">
                          {shot.status}
                        </span>
                      </div>
                      <div className={`text-sm font-medium ${isVerified ? 'text-neutral-300' : 'text-white'}`}>
                        {shot.title}
                      </div>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Shot Terminal */}
        <div className="lg:col-span-2">
          {activeRecord ? (
            <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 h-full flex flex-col">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <div className="text-xs font-mono text-blue-500 mb-1 flex items-center gap-2">
                    TERMINAL: {activeRecord.id.toUpperCase()}
                    <span className="text-neutral-500">|</span>
                    <span className="text-neutral-400">PROVENANCE: {activeRecord.provenance}</span>
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-2">{activeRecord.title}</h3>
                  {activeRecord.description && (
                    <p className="text-sm text-neutral-400 mb-2">{activeRecord.description}</p>
                  )}
                </div>
                
                {activeRecord.verified === true && activeRecord.status === 'COMPLETED' ? (
                  <span className="bg-emerald-500/10 text-emerald-500 px-3 py-1 rounded-full text-xs font-bold tracking-wider flex items-center gap-1 border border-emerald-500/20">
                    <ShieldCheck size={14} /> VERIFIED
                  </span>
                ) : activeRecord.verified === 'not_applicable' ? (
                  <span className="bg-fuchsia-500/10 text-fuchsia-500 px-3 py-1 rounded-full text-xs font-bold tracking-wider flex items-center gap-1 border border-fuchsia-500/20">
                    <Wand2 size={14} /> GENERATED FICTION
                  </span>
                ) : (
                  <span className="bg-amber-500/10 text-amber-500 px-3 py-1 rounded-full text-xs font-bold tracking-wider flex items-center gap-1 border border-amber-500/20">
                    <ShieldAlert size={14} /> UNVERIFIED / {activeRecord.status}
                  </span>
                )}
              </div>

              <div className="flex-1 bg-black rounded-lg border border-neutral-800 flex items-center justify-center relative overflow-hidden min-h-[300px]">
                {activeRecord.verified === true && activeRecord.status === 'COMPLETED' ? (
                  <div className="absolute inset-0 bg-neutral-800 flex items-center justify-center">
                    <Video size={48} className="text-neutral-600" />
                    <div className="absolute bottom-4 left-4 text-xs font-mono text-white bg-black/50 px-2 py-1 rounded flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                      VERIFIED EVIDENCE ATTACHED
                    </div>
                  </div>
                ) : activeRecord.verified === 'not_applicable' ? (
                  <div className="absolute inset-0 bg-fuchsia-900/20 flex items-center justify-center border border-fuchsia-500/20 rounded-lg">
                    <Wand2 size={48} className="text-fuchsia-500/50" />
                    <div className="absolute bottom-4 left-4 text-xs font-mono text-fuchsia-400 bg-black/50 px-2 py-1 rounded border border-fuchsia-500/30">
                      FICTIONAL GENERATION
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-neutral-500 flex flex-col items-center">
                    <Video size={32} className="mb-3 opacity-50" />
                    <p className="text-sm font-medium mb-1">No verified footage exists.</p>
                    <p className="text-xs text-neutral-600 max-w-xs">This item was generated from {activeRecord.provenance.toLowerCase().replace('_', ' ')}. Upload footage to mark it as verified.</p>
                  </div>
                )}
              </div>

              <div className="mt-6 flex gap-4">
                <button className="flex-1 bg-blue-600 hover:bg-blue-500 text-white py-3 rounded font-bold text-sm transition-colors flex items-center justify-center gap-2">
                  <Video size={18} />
                  ATTACH EVIDENCE & VERIFY
                </button>
                <button className="flex-1 bg-neutral-800 hover:bg-neutral-700 text-white py-3 rounded font-bold text-sm transition-colors flex items-center justify-center gap-2 border border-neutral-700">
                  <Wand2 size={18} />
                  GENERATE PREVIEW
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 h-full flex items-center justify-center text-neutral-500 flex-col gap-4">
              <ShieldAlert size={48} className="opacity-20" />
              <div className="text-center">
                <p className="font-bold text-neutral-400 mb-1">Select an item to view provenance</p>
                <p className="text-sm">Verify production status or review planned items.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
