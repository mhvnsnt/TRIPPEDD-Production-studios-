import { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, CheckCircle2, Circle, RefreshCw, Sparkles, Video } from 'lucide-react';
import { createEp01AssemblyPlan } from '../core/editorial/ep01Assembly';
import { createEp01PilotPlan } from '../core/editorial/ep01Pilot';

interface QueueJob {
  id: string;
  fileId?: string;
  originalName?: string;
  state?: string;
  progress?: number;
  evidenceRefs?: string[];
}

interface ProductionStageProgress {
  id: string;
  label: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETE' | 'FAILED';
  completed: number;
  total: number;
  percent: number;
  heartbeatAt: string;
  artifactBytes?: number;
  message?: string;
}

interface ProductionProgressSnapshot {
  schemaVersion: 1;
  episodeId: string;
  runId: string;
  updatedAt: string;
  currentStageId?: string;
  stages: ProductionStageProgress[];
}

const pilot = createEp01PilotPlan();
const assembly = createEp01AssemblyPlan();

const stageNames = [
  'Drive media discovered',
  'Physical source timeline analyzed',
  'Comedy candidates discovered',
  'Story / segment structure approved',
  'Subjective material generated',
  'Editorial assembly built',
  'QC passed',
  'Final greenlight',
];

function formatBytes(bytes?: number) {
  if (!bytes) return '';
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function ActiveProduction() {
  const [jobs, setJobs] = useState<QueueJob[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedBeat, setSelectedBeat] = useState(pilot.beats[0]?.id ?? null);
  const [productionProgress, setProductionProgress] = useState<ProductionProgressSnapshot | null>(null);

  const refresh = async () => {
    setLoading(true);
    try {
      const [queueResponse, progressResponse] = await Promise.all([fetch('/api/queue'), fetch('/api/production/progress/latest')]);
      if (queueResponse.ok) setJobs(await queueResponse.json());
      if (progressResponse.ok) setProductionProgress(await progressResponse.json());
    } catch {
      // The workspace remains useful offline; the Drive ingest workspace owns authentication.
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void refresh();
    const timer = window.setInterval(() => void refresh(), 5000);
    return () => window.clearInterval(timer);
  }, []);

  const analyzed = jobs.filter(job => job.state === 'NEEDS_REVIEW' || job.state === 'COMPLETED').length;
  const selected = useMemo(() => pilot.beats.find(beat => beat.id === selectedBeat), [selectedBeat]);

  return (
    <div className="p-8 max-w-7xl mx-auto w-full space-y-8">
      <header className="border-b border-neutral-800 pb-6 flex flex-col md:flex-row md:items-end md:justify-between gap-4">
        <div>
          <div className="text-sm font-bold text-neutral-500 tracking-widest mb-2">AUTONOMOUS PRODUCTION TERMINAL</div>
          <h2 className="text-4xl font-black tracking-tight text-white">EP01 — THE WALK</h2>
          <p className="text-neutral-400 mt-2 max-w-3xl">The actual pilot run: real source evidence first, comedy discovery second, subjective generation only where the story calls for it.</p>
        </div>
        <button onClick={() => void refresh()} disabled={loading} className="bg-neutral-800 hover:bg-neutral-700 disabled:opacity-50 text-white px-4 py-2 rounded font-bold text-sm flex items-center gap-2 border border-neutral-700">
          <RefreshCw size={16} className={loading ? 'animate-spin' : ''} /> REFRESH PIPELINE
        </button>
      </header>

      <section className="bg-neutral-900 border border-neutral-800 rounded-xl p-5">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-2 mb-5">
          <div>
            <div className="text-xs font-mono text-neutral-500">MEASURED RENDER PROGRESS</div>
            <h3 className="text-xl font-bold text-white">Live stage evidence</h3>
          </div>
          <div className="text-[10px] font-mono text-neutral-600">
            {productionProgress ? `RUN ${productionProgress.runId} · UPDATED ${new Date(productionProgress.updatedAt).toLocaleTimeString()}` : 'WAITING FOR A RENDER LEDGER'}
          </div>
        </div>
        {productionProgress ? (
          <div className="space-y-4">
            {productionProgress.stages.map(stage => (
              <div key={stage.id}>
                <div className="flex items-center gap-3 mb-1.5">
                  {stage.status === 'COMPLETE' ? <CheckCircle2 size={15} className="text-emerald-400 shrink-0" /> : stage.status === 'FAILED' ? <AlertTriangle size={15} className="text-red-400 shrink-0" /> : <Circle size={15} className={stage.status === 'RUNNING' ? 'text-blue-400 shrink-0' : 'text-neutral-700 shrink-0'} />}
                  <span className={`text-sm ${stage.status === 'FAILED' ? 'text-red-300' : stage.status === 'COMPLETE' ? 'text-neutral-300' : stage.status === 'RUNNING' ? 'text-blue-300' : 'text-neutral-500'}`}>{stage.label}</span>
                  <span className="ml-auto text-xs font-mono text-neutral-500">{stage.completed}/{stage.total} · {stage.percent}%</span>
                </div>
                <div className="h-2 bg-neutral-950 border border-neutral-800 rounded-full overflow-hidden">
                  <div className={`h-full transition-all duration-500 ${stage.status === 'FAILED' ? 'bg-red-500' : stage.status === 'COMPLETE' ? 'bg-emerald-500' : 'bg-blue-500'}`} style={{ width: `${stage.percent}%` }} />
                </div>
                {(stage.message || stage.artifactBytes) && <div className="text-[10px] font-mono text-neutral-600 mt-1">{stage.message ?? ''}{stage.artifactBytes ? ` · artifact ${formatBytes(stage.artifactBytes)}` : ''}</div>}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-sm text-neutral-600 font-mono">No measured render ledger has been published yet.</div>
        )}
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-neutral-900 border border-neutral-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-5">
            <div>
              <div className="text-xs font-mono text-neutral-500">EDITORIAL ASSEMBLY</div>
              <h3 className="text-xl font-bold text-white">Source → Subjectivity → Button</h3>
            </div>
            <span className="text-xs font-mono text-neutral-500">{assembly.items.length} planned items</span>
          </div>
          <div className="space-y-2">
            {assembly.items.map((item, index) => (
              <button key={item.id} onClick={() => setSelectedBeat(item.beatId)} className={`w-full text-left p-3 rounded-lg border transition-colors ${selectedBeat === item.beatId ? 'border-neutral-600 bg-neutral-800' : 'border-neutral-800 bg-neutral-950 hover:border-neutral-700'}`}>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-neutral-600 w-5">{String(index + 1).padStart(2, '0')}</span>
                  {item.kind === 'GENERATED' ? <Sparkles size={16} className="text-fuchsia-400 shrink-0" /> : <Video size={16} className="text-emerald-400 shrink-0" />}
                  <div className="min-w-0 flex-1">
                    <div className="text-sm font-semibold text-white">{item.title}</div>
                    <div className="text-[11px] font-mono text-neutral-500 truncate">{item.kind} {item.sourceLabels.length ? `· ${item.sourceLabels.join(' / ')}` : `· ${item.generationPurpose ?? ''}`}</div>
                  </div>
                  {item.terminal && <span className="text-[9px] font-bold text-yellow-400 border border-yellow-500/30 px-2 py-1 rounded">CUT</span>}
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-5 space-y-5">
          <div>
            <div className="text-xs font-mono text-neutral-500">SOURCE INGEST</div>
            <div className="text-3xl font-black text-white mt-1">{jobs.length}</div>
            <div className="text-xs text-neutral-500">Drive files currently visible to the production queue</div>
          </div>
          <div className="border-t border-neutral-800 pt-5">
            <div className="text-xs font-mono text-neutral-500">ANALYZED</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">{analyzed}</div>
            <div className="text-xs text-neutral-500">Analysis complete / awaiting evidence review</div>
          </div>
          <div className="border-t border-neutral-800 pt-5">
            <div className="text-xs font-mono text-neutral-500">TERMINAL BEAT</div>
            <div className="text-lg font-bold text-yellow-400 mt-1">THE LOST ACID</div>
            <div className="text-xs text-neutral-500">No resolution. No post-button scene.</div>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-5">
          <div className="text-xs font-mono text-neutral-500 mb-2">SELECTED BEAT</div>
          <h3 className="text-2xl font-bold text-white">{selected?.title ?? 'Select a beat'}</h3>
          <p className="text-sm text-neutral-400 mt-3">{selected?.purpose}</p>
          <div className="flex gap-2 mt-5 flex-wrap">
            <span className="text-[10px] font-bold border border-neutral-700 rounded px-2 py-1 text-neutral-300">{selected?.kind}</span>
            {selected?.sourceTruthRequired && <span className="text-[10px] font-bold border border-emerald-500/30 rounded px-2 py-1 text-emerald-400">SOURCE TRUTH</span>}
            {selected?.generatedMaterialAllowed && <span className="text-[10px] font-bold border border-fuchsia-500/30 rounded px-2 py-1 text-fuchsia-400">GENERATED ALLOWED</span>}
            {selected?.humanApprovalRequired && <span className="text-[10px] font-bold border border-yellow-500/30 rounded px-2 py-1 text-yellow-400">HUMAN GATE</span>}
          </div>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-5">
          <div className="text-xs font-mono text-neutral-500 mb-4">AUTONOMOUS RUN</div>
          <div className="space-y-3">
            {stageNames.map((name, index) => {
              const complete = index === 0 ? jobs.length > 0 : false;
              const gated = [3, 4, 5, 7].includes(index);
              return (
                <div key={name} className="flex items-center gap-3">
                  {complete ? <CheckCircle2 size={16} className="text-emerald-400" /> : gated ? <AlertTriangle size={16} className="text-yellow-400" /> : <Circle size={16} className="text-neutral-700" />}
                  <span className={`text-sm ${complete ? 'text-neutral-300' : gated ? 'text-yellow-300' : 'text-neutral-500'}`}>{name}</span>
                  {gated && <span className="ml-auto text-[9px] font-mono text-neutral-600">REVIEW</span>}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <div className="text-[11px] font-mono text-neutral-600 border-t border-neutral-900 pt-4">
        PHYSICAL CHRONOLOGY IS AUTHORITATIVE ABOUT WHAT HAPPENED. THIS SCREEN DESCRIBES EDITORIAL ORDER. GENERATED MATERIAL NEVER REPLACES SOURCE EVIDENCE.
      </div>
    </div>
  );
}