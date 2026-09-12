import { useEffect, useState } from 'react';
import { Film, RefreshCw, PlayCircle, AlertTriangle, CheckCircle2, Lock, XCircle } from 'lucide-react';
import { createEp01PilotPlan } from '../core/editorial/ep01Pilot';

interface AssemblyManifest { status: string; sourceClipCount: number; selectedClipCount: number; missingBeats: string[]; outputPath?: string; generatedAt: string; }
interface FinalManifest { status: string; finalMasterPath?: string; durationSeconds?: number; blockedReasons: string[]; gates: Record<string, boolean>; generatedAt: string; }

export function PilotBuildWorkspace() {
  const [manifest, setManifest] = useState<AssemblyManifest | null>(null);
  const [finalManifest, setFinalManifest] = useState<FinalManifest | null>(null);
  const [queue, setQueue] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const pilot = createEp01PilotPlan();

  const refresh = async () => {
    setLoading(true);
    try {
      const [queueRes, manifestRes, finalRes] = await Promise.all([
        fetch('/api/queue'),
        fetch('/production/EP01-first-assembly.json', { cache: 'no-store' }),
        fetch('/production/EP01-final.json', { cache: 'no-store' }),
      ]);
      if (queueRes.ok) setQueue(await queueRes.json());
      if (manifestRes.ok) setManifest(await manifestRes.json()); else setManifest(null);
      if (finalRes.ok) setFinalManifest(await finalRes.json()); else setFinalManifest(null);
    } finally { setLoading(false); }
  };

  useEffect(() => { void refresh(); const timer = window.setInterval(() => void refresh(), 5000); return () => window.clearInterval(timer); }, []);

  const analyzed = queue.filter(job => job.state === 'NEEDS_REVIEW' || job.state === 'COMPLETED').length;
  const failed = queue.filter(job => job.state === 'FAILED').length;
  const finalReady = finalManifest?.status === 'FINAL_MASTER_READY' && !!finalManifest.finalMasterPath;

  return (
    <div className="p-8 max-w-7xl mx-auto w-full space-y-8">
      <header className="border-b border-neutral-800 pb-6 flex items-end justify-between gap-4">
        <div><div className="text-xs font-mono tracking-widest text-neutral-500 mb-2">REAL PILOT PRODUCTION</div><h2 className="text-4xl font-black">EP01 — THE WALK</h2><p className="text-neutral-400 mt-2">First assembly and final-master playback. No fake render state.</p></div>
        <button onClick={() => void refresh()} disabled={loading} className="px-4 py-2 rounded bg-neutral-800 border border-neutral-700 text-sm font-bold flex items-center gap-2"><RefreshCw size={15} className={loading ? 'animate-spin' : ''}/> REFRESH</button>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[['SOURCE FILES', queue.length, 'neutral'], ['ANALYZED', analyzed, 'emerald'], ['FAILED', failed, 'red'], ['FIRST ASSEMBLY', manifest?.selectedClipCount ?? 0, manifest ? 'emerald' : 'yellow']].map(([label, value, tone]) => (
          <div key={label as string} className="bg-neutral-900 border border-neutral-800 rounded-xl p-5"><div className="text-[10px] font-mono text-neutral-500">{label}</div><div className={`text-3xl font-black mt-2 ${tone === 'emerald' ? 'text-emerald-400' : tone === 'red' ? 'text-red-400' : tone === 'yellow' ? 'text-yellow-400' : 'text-white'}`}>{value}</div></div>
        ))}
      </section>

      {manifest?.outputPath ? (
        <section className="bg-neutral-900 border border-emerald-500/30 rounded-xl p-5 space-y-4">
          <div className="flex items-center gap-2 text-emerald-400 font-bold"><CheckCircle2 size={18}/> REAL FIRST ASSEMBLY</div>
          <video className="w-full rounded-lg bg-black max-h-[70vh]" controls preload="metadata" src={manifest.outputPath} />
          <div className="text-xs font-mono text-neutral-500">{manifest.selectedClipCount} timed source selects · generated {new Date(manifest.generatedAt).toLocaleString()}</div>
        </section>
      ) : (
        <section className="bg-neutral-900 border border-yellow-500/30 rounded-xl p-6 flex items-start gap-4"><AlertTriangle className="text-yellow-400 shrink-0"/><div><h3 className="font-bold text-yellow-300">Waiting for real source analysis</h3><p className="text-sm text-neutral-400 mt-1">Authenticate Drive and scan the EP01 folder. The renderer will build the first assembly from cached source media and timed evidence.</p></div></section>
      )}

      <section className={`bg-neutral-900 border rounded-xl p-5 space-y-4 ${finalReady ? 'border-emerald-500/40' : 'border-neutral-800'}`}>
        <div className="flex items-center justify-between"><div className="flex items-center gap-2"><Film size={18} className={finalReady ? 'text-emerald-400' : 'text-fuchsia-400'}/><h3 className="font-bold">FULL EPISODE MASTER</h3></div><span className="text-[10px] font-mono px-2 py-1 rounded bg-neutral-950 border border-neutral-800">{finalManifest?.status ?? 'NOT BUILT'}</span></div>
        {finalReady ? (
          <>
            <video className="w-full rounded-lg bg-black max-h-[75vh]" controls preload="metadata" src={finalManifest.finalMasterPath} />
            <div className="text-xs font-mono text-neutral-500">FINAL MASTER · {finalManifest.durationSeconds ? `${Math.round(finalManifest.durationSeconds)}s` : 'duration unavailable'} · {new Date(finalManifest.generatedAt).toLocaleString()}</div>
          </>
        ) : (
          <div className="grid md:grid-cols-5 gap-2">{Object.entries(finalManifest?.gates ?? { sourceAssembly: false, subjectivityAsset: false, editorialLock: false, qc: false, showrunnerGreenlight: false }).map(([gate, passed]) => <div key={gate} className={`p-3 rounded border ${passed ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-neutral-800 bg-neutral-950'}`}><div className="flex items-center gap-2">{passed ? <CheckCircle2 size={14} className="text-emerald-400"/> : <XCircle size={14} className="text-neutral-600"/>}<span className="text-[10px] font-mono uppercase">{gate.replace(/([A-Z])/g, ' $1')}</span></div></div>)}</div>
        )}
        {finalManifest?.blockedReasons?.length ? <div className="text-xs text-neutral-500 space-y-1">{finalManifest.blockedReasons.map(reason => <div key={reason} className="flex gap-2"><Lock size={12} className="shrink-0 mt-0.5"/>{reason}</div>)}</div> : null}
      </section>

      <section className="bg-neutral-900 border border-neutral-800 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-5"><Film size={18} className="text-fuchsia-400"/><h3 className="font-bold">Canonical EP01 Build</h3></div>
        <div className="grid md:grid-cols-2 gap-2">{pilot.beats.map((beat, i) => <div key={beat.id} className="p-3 rounded bg-neutral-950 border border-neutral-800"><div className="text-[10px] font-mono text-neutral-600">{String(i + 1).padStart(2, '0')} · {beat.kind}</div><div className="text-sm font-semibold mt-1">{beat.title}</div>{beat.generatedMaterialAllowed && <div className="text-[10px] text-fuchsia-400 mt-1">GENERATED MATERIAL ALLOWED · HUMAN GATE</div>}</div>)}</div>
        <div className="mt-5 text-[11px] font-mono text-neutral-600">TERMINAL: LOST ACID. THE DISAPPEARANCE IS NOT SOLVED. NOTHING FOLLOWS THE BUTTON.</div>
      </section>

      <section className="bg-neutral-900 border border-neutral-800 rounded-xl p-5">
        <div className="text-xs font-mono text-neutral-500 mb-3">SOURCE QUEUE</div>
        <div className="space-y-2">{queue.map(job => <div key={job.fileId} className="flex items-center gap-3 p-3 bg-neutral-950 rounded border border-neutral-800"><PlayCircle size={15} className="text-neutral-600"/><span className="flex-1 text-sm truncate">{job.originalName || job.fileId}</span><span className="text-[10px] font-mono text-neutral-500">{job.state}</span><span className="text-[10px] font-mono text-neutral-600">{job.progress ?? 0}%</span></div>)}{queue.length === 0 && <div className="text-sm text-neutral-600">No Drive media has entered the production queue yet.</div>}</div>
      </section>
    </div>
  );
}
