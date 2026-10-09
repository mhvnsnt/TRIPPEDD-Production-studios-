import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Film, CheckCircle2, XCircle, RotateCcw, Scissors, ChevronRight, AlertTriangle,
  Play, Pause, Lock, FileWarning, Sparkles, Download, RefreshCw, Layers, Quote,
} from 'lucide-react';

/**
 * Editorial Review — the human gate, one scene at a time.
 *
 * Everything shown here comes from the server's editorial state. The panel
 * never computes an opinion of its own: if the engine did not detect something,
 * this says "not detected", never "nothing happened", and material that is only
 * remembered is labelled as such rather than drawn as evidence.
 */

interface SourceRange { sourceFileId: string; startTime: number; endTime: number; derivedFromObservationIds: string[]; }
interface Exclusion { range: SourceRange; classification: string; reason: string; excerpt?: string; preservedInPhysicalTimeline: boolean; }
interface Scene {
  id: string; proposedTitle: string; purpose: string;
  proposedOrder: number; physicalOrder: number; reorderReason?: string;
  ranges: SourceRange[]; proposedDuration: number;
  beatMap: { role: string; range: SourceRange; rationale: string }[];
  excludedMaterial: Exclusion[];
  confidence: number; editorialRationale: string;
  chronologyAssumptions: { statement: string; confidence: string }[];
  missingEvidence: string[]; sourceClipIds: string[]; storyBeatIds: string[];
  evidenceLimitations: { tool: string; reason: string; effect: string }[];
  sourceEvidenceIds: string[]; humanReviewState: string;
  revisionHistory: { at: string; from: string; to: string; actor: string; note?: string }[];
}
interface TranscriptLine { start: number; end: number; text: string; included: boolean; sourceFileId: string; }
interface NextPayload { scene: Scene | null; done: boolean; transcript?: TranscriptLine[]; remaining?: number; mediaPath?: string | null; }
interface ReconBeat { beatId: string; title: string; state: string; confidence: number; mentionStrength: string; rationale: string; candidateSourceFileIds: string[]; }

const STATE_BADGE: Record<string, string> = {
  PROPOSED: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  UNDER_REVIEW: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  REVISION_REQUESTED: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  REVISED: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  APPROVED: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  LOCKED: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  REJECTED: 'text-red-400 bg-red-500/10 border-red-500/20',
};

const RECON_STYLE: Record<string, { cls: string; label: string }> = {
  FOUND: { cls: 'text-emerald-400', label: 'found in source' },
  PARTIALLY_FOUND: { cls: 'text-amber-400', label: 'partially found' },
  AMBIGUOUS_MATCH: { cls: 'text-amber-400', label: 'ambiguous' },
  NOT_FOUND: { cls: 'text-neutral-500', label: 'not detected in ingested media' },
  MISSING_SOURCE_MEDIA: { cls: 'text-neutral-500', label: 'no source media ingested' },
};

const fmt = (s: number) => {
  const m = Math.floor(s / 60), sec = s % 60;
  return `${String(m).padStart(2, '0')}:${sec.toFixed(2).padStart(5, '0')}`;
};

export function EditorialReviewWorkspace() {
  const [next, setNext] = useState<NextPayload | null>(null);
  const [state, setState] = useState<any>(null);
  const [recon, setRecon] = useState<{ built: boolean; beats: ReconBeat[] } | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [note, setNote] = useState('');
  const [noteMode, setNoteMode] = useState<'revise' | 'reject' | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [playing, setPlaying] = useState(false);
  const [activeRange, setActiveRange] = useState(0);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const load = useCallback(async () => {
    try {
      const [n, s, r] = await Promise.all([
        fetch('/api/editorial/scenes/next').then((x) => x.json()),
        fetch('/api/editorial/state').then((x) => x.json()),
        fetch('/api/editorial/reconciliation').then((x) => x.json()),
      ]);
      setNext(n); setState(s); setRecon(r); setErr(null);
      setActiveRange(0);
    } catch (e: any) { setErr(e.message); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const build = async () => {
    setBusy('build');
    try {
      const res = await fetch('/api/editorial/build', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}),
      });
      if (!res.ok) throw new Error((await res.json()).error);
      await load();
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  };

  const decide = async (action: 'approve' | 'revise' | 'reject', text?: string) => {
    if (!next?.scene) return;
    setBusy(action);
    try {
      const res = await fetch(`/api/editorial/scenes/${next.scene.id}/${action}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ note: text }),
      });
      if (!res.ok) throw new Error((await res.json()).error);
      setNote(''); setNoteMode(null);
      await load();
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  };

  const exportProject = async (format: 'kdenlive' | 'otio', onlyApproved: boolean) => {
    setBusy('export');
    try {
      const res = await fetch(`/api/editorial/export/${format}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ onlyApproved }),
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.error);
      setErr(null);
      alert(`${format} written to:\n${j.outputPath}\n\n${j.clipCount} clip(s), ${j.totalDuration.toFixed(2)}s\nverified: ${j.verified}\n${j.verifyDetail ?? ''}`);
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  };

  // Play only the ranges in the cut, in order — a preview of the EDIT, not the raw clip.
  const playCut = () => {
    const v = videoRef.current;
    const scene = next?.scene;
    if (!v || !scene?.ranges.length) return;
    if (playing) { v.pause(); setPlaying(false); return; }
    setActiveRange(0);
    v.currentTime = scene.ranges[0].startTime;
    v.play(); setPlaying(true);
  };

  const onTimeUpdate = () => {
    const v = videoRef.current;
    const scene = next?.scene;
    if (!v || !scene || !playing) return;
    const r = scene.ranges[activeRange];
    if (!r) return;
    if (v.currentTime >= r.endTime) {
      const nextIdx = activeRange + 1;
      if (nextIdx < scene.ranges.length) {
        setActiveRange(nextIdx);
        v.currentTime = scene.ranges[nextIdx].startTime;
      } else { v.pause(); setPlaying(false); }
    }
  };

  const scene = next?.scene;
  const c = state?.counts;

  return (
    <div className="p-6 space-y-4 text-neutral-200">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Film size={18} className="text-neutral-400" />
          <h2 className="font-bold tracking-tight">EDITORIAL REVIEW</h2>
          {c && (
            <span className="text-[11px] text-neutral-500 tabular-nums">
              {c.locked} locked · {c.proposed + c.awaitingRevision} awaiting you · {c.rejected} rejected
            </span>
          )}
        </div>
        <div className="flex gap-2">
          <button onClick={build} disabled={!!busy}
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40">
            <Sparkles size={13} />{busy === 'build' ? 'Assembling…' : 'Assemble scenes'}
          </button>
          <button onClick={() => exportProject('kdenlive', true)} disabled={!!busy || !c?.locked}
            title={!c?.locked ? 'Approve at least one scene first' : 'Export the approved cut'}
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40">
            <Download size={13} />Export approved
          </button>
        </div>
      </div>

      {err && (
        <div className="border border-red-500/20 bg-red-500/5 rounded p-3 text-xs text-red-400 flex gap-2">
          <AlertTriangle size={13} className="mt-px shrink-0" />{err}
        </div>
      )}

      {/* Reconciliation: what was remembered vs what the footage shows */}
      {recon?.built && (
        <details className="border border-neutral-800 rounded-lg bg-neutral-950" open={!scene}>
          <summary className="px-4 py-3 cursor-pointer text-xs font-bold tracking-tight flex items-center gap-2">
            <Layers size={14} className="text-neutral-400" />
            MENTIONED MATERIAL vs ACTUAL FOOTAGE
            <span className="text-neutral-500 font-normal">
              ({recon.beats.filter((b) => b.state === 'FOUND').length} found of {recon.beats.length})
            </span>
          </summary>
          <div className="px-4 pb-3 space-y-1">
            {recon.beats.map((b) => {
              const st = RECON_STYLE[b.state] ?? RECON_STYLE.NOT_FOUND;
              return (
                <div key={b.beatId} className="flex items-start gap-2 text-[11px] py-1 border-t border-neutral-900">
                  <span className={`w-44 shrink-0 ${st.cls}`}>{st.label}</span>
                  <span className="w-52 shrink-0 text-neutral-300">{b.title}</span>
                  {b.mentionStrength === 'PARTIAL' && (
                    <span className="text-[9px] px-1.5 py-0.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-500 shrink-0">
                      only partially described
                    </span>
                  )}
                  <span className="text-neutral-600 flex-1">{b.rationale}</span>
                </div>
              );
            })}
          </div>
        </details>
      )}

      {/* No scenes */}
      {!scene && (
        <div className="border border-neutral-800 rounded-lg bg-neutral-950 p-8 text-center">
          {next?.done && state?.counts?.total > 0 ? (
            <>
              <CheckCircle2 size={28} className="mx-auto text-emerald-400 mb-3" />
              <div className="font-bold text-sm">Every scene has been reviewed.</div>
              <div className="text-xs text-neutral-500 mt-1">
                {c?.locked} locked, {c?.rejected} rejected. Export the approved cut above.
              </div>
            </>
          ) : (
            <>
              <FileWarning size={28} className="mx-auto text-neutral-600 mb-3" />
              <div className="font-bold text-sm">No scenes assembled yet.</div>
              <div className="text-xs text-neutral-500 mt-1">
                Ingest media, then press <b>Assemble scenes</b>. Scenes are only built from beats
                actually found in the footage.
              </div>
            </>
          )}
        </div>
      )}

      {/* The scene */}
      {scene && (
        <div className="grid grid-cols-3 gap-4">
          {/* Left: preview + cut */}
          <div className="col-span-2 space-y-4">
            <div className="border border-neutral-800 rounded-lg bg-neutral-950 overflow-hidden">
              <div className="flex items-center justify-between px-4 py-3 border-b border-neutral-800">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-400 shrink-0">
                    #{scene.proposedOrder + 1}
                  </span>
                  <h3 className="font-bold text-sm truncate">{scene.proposedTitle}</h3>
                  <span className={`text-[10px] px-2 py-0.5 rounded border font-bold shrink-0 ${STATE_BADGE[scene.humanReviewState]}`}>
                    {scene.humanReviewState}
                  </span>
                </div>
                <span className="text-[11px] text-neutral-500 tabular-nums shrink-0">
                  {scene.proposedDuration.toFixed(2)}s · {next?.remaining} left
                </span>
              </div>

              <div className="bg-black aspect-video relative">
                {next?.mediaPath ? (
                  <video
                    ref={videoRef}
                    src={`/api/media/${scene.sourceClipIds[0]}`}
                    className="w-full h-full object-contain"
                    onTimeUpdate={onTimeUpdate}
                    onPause={() => setPlaying(false)}
                    controls
                  />
                ) : (
                  <div className="absolute inset-0 flex items-center justify-center text-neutral-600 text-xs text-center px-6">
                    Source media not retained locally — the cut points below are still exact.
                    Re-run ingest with media retention to preview here.
                  </div>
                )}
              </div>

              <div className="px-4 py-2 border-t border-neutral-800 flex items-center gap-3">
                <button onClick={playCut} disabled={!next?.mediaPath}
                  className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40">
                  {playing ? <Pause size={13} /> : <Play size={13} />}
                  {playing ? 'Pause' : 'Play the cut'}
                </button>
                <span className="text-[10px] text-neutral-500">
                  plays only the selected ranges, in editorial order
                </span>
              </div>
            </div>

            {/* Why this scene exists */}
            <div className="border border-neutral-800 rounded-lg bg-neutral-950 p-4 space-y-2">
              <div className="text-[10px] uppercase tracking-wider text-neutral-500">Why this scene exists</div>
              <p className="text-xs text-neutral-300 leading-relaxed">{scene.purpose}</p>
              <p className="text-[11px] text-neutral-500 leading-relaxed">{scene.editorialRationale}</p>
              {scene.reorderReason && (
                <div className="text-[11px] text-amber-400/90 flex gap-2 pt-1">
                  <RotateCcw size={12} className="mt-px shrink-0" />
                  {scene.reorderReason}
                </div>
              )}
            </div>

            {/* Transcript: what is in the cut and what was taken out */}
            <div className="border border-neutral-800 rounded-lg bg-neutral-950">
              <div className="px-4 py-2.5 border-b border-neutral-800 flex items-center gap-2">
                <Quote size={13} className="text-neutral-400" />
                <span className="text-xs font-bold">TRANSCRIPT</span>
                <span className="text-[10px] text-neutral-500">struck-through lines are excluded from the cut</span>
              </div>
              <div className="max-h-64 overflow-y-auto divide-y divide-neutral-900">
                {(next?.transcript ?? []).length === 0 && (
                  <div className="px-4 py-3 text-[11px] text-neutral-600">
                    No speech detected in this range. That is an absence of detection, not proof of silence.
                  </div>
                )}
                {(next?.transcript ?? []).map((t, i) => (
                  <div key={i} className={`px-4 py-1.5 text-[11px] flex gap-3 ${t.included ? '' : 'opacity-45'}`}>
                    <span className="text-neutral-600 tabular-nums shrink-0">{fmt(t.start)}</span>
                    <span className={t.included ? 'text-neutral-300' : 'text-neutral-500 line-through'}>{t.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right: the reasoning */}
          <div className="space-y-4">
            <div className="border border-neutral-800 rounded-lg bg-neutral-950 p-4 space-y-3">
              <div className="text-[10px] uppercase tracking-wider text-neutral-500">The cut</div>
              {scene.ranges.map((r, i) => (
                <div key={i} className="text-[11px] font-mono flex justify-between text-neutral-300">
                  <span className="text-neutral-500">{r.sourceFileId}</span>
                  <span>{fmt(r.startTime)} → {fmt(r.endTime)}</span>
                </div>
              ))}
              <div className="pt-2 border-t border-neutral-800 flex justify-between text-[11px]">
                <span className="text-neutral-500">editorial confidence</span>
                <span className="tabular-nums">{(scene.confidence * 100).toFixed(0)}%</span>
              </div>
              <div className="flex justify-between text-[11px]">
                <span className="text-neutral-500">physical position</span>
                <span className="tabular-nums">{scene.physicalOrder + 1}</span>
              </div>
              <div className="flex justify-between text-[11px]">
                <span className="text-neutral-500">evidence items</span>
                <span className="tabular-nums">{scene.sourceEvidenceIds.length}</span>
              </div>
            </div>

            {scene.excludedMaterial.length > 0 && (
              <div className="border border-neutral-800 rounded-lg bg-neutral-950 p-4 space-y-2">
                <div className="text-[10px] uppercase tracking-wider text-neutral-500 flex items-center gap-1.5">
                  <Scissors size={11} /> Removed from the cut
                </div>
                {scene.excludedMaterial.map((e, i) => (
                  <div key={i} className="text-[11px] border-t border-neutral-900 pt-1.5">
                    <div className="text-amber-400/90 text-[10px] font-bold">{e.classification}</div>
                    {e.excerpt && <div className="text-neutral-400 italic">"{e.excerpt.slice(0, 90)}"</div>}
                    <div className="text-neutral-600 text-[10px]">
                      {fmt(e.range.startTime)}–{fmt(e.range.endTime)} · kept in the physical timeline
                    </div>
                  </div>
                ))}
              </div>
            )}

            {scene.chronologyAssumptions.length > 0 && (
              <div className="border border-amber-500/20 bg-amber-500/5 rounded-lg p-4 space-y-2">
                <div className="text-[10px] uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
                  <AlertTriangle size={11} /> Assumptions
                </div>
                {scene.chronologyAssumptions.map((a, i) => (
                  <div key={i} className="text-[11px] text-neutral-300 leading-snug">
                    {a.statement}
                    <span className="text-neutral-500"> ({a.confidence})</span>
                  </div>
                ))}
              </div>
            )}

            {scene.evidenceLimitations?.length > 0 && (
              <div className="border border-amber-500/20 bg-amber-500/5 rounded-lg p-4 space-y-2">
                <div className="text-[10px] uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
                  <FileWarning size={11} /> Evidence quality
                </div>
                {/* Approving should never be a guess about what the machine saw. */}
                {scene.evidenceLimitations.map((l, i) => (
                  <div key={i} className="text-[11px] leading-snug">
                    <span className="text-amber-400 font-bold">{l.tool.toUpperCase()}: {l.reason}</span>
                    <div className="text-neutral-400">{l.effect}</div>
                  </div>
                ))}
                <div className="text-[10px] text-neutral-500 pt-1 border-t border-neutral-800">
                  Confidence above is reduced to reflect this.
                </div>
              </div>
            )}

            {scene.missingEvidence.length > 0 && (
              <div className="border border-neutral-800 rounded-lg bg-neutral-950 p-4 space-y-1">
                <div className="text-[10px] uppercase tracking-wider text-neutral-500">Missing material</div>
                {scene.missingEvidence.map((m, i) => (
                  <div key={i} className="text-[11px] text-neutral-500 leading-snug">{m}</div>
                ))}
              </div>
            )}

            {/* Decisions */}
            <div className="border border-neutral-800 rounded-lg bg-neutral-950 p-4 space-y-2">
              {noteMode ? (
                <>
                  <div className="text-[10px] uppercase tracking-wider text-neutral-500">
                    {noteMode === 'revise' ? 'What should change?' : 'Why reject?'}
                  </div>
                  <textarea
                    value={note} onChange={(e) => setNote(e.target.value)} rows={3} autoFocus
                    className="w-full bg-neutral-900 border border-neutral-700 rounded p-2 text-xs text-neutral-200"
                    placeholder={noteMode === 'revise' ? 'trim the opening, hold the reaction longer…' : 'the joke does not land…'}
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => decide(noteMode, note)}
                      disabled={!note.trim() || !!busy}
                      className="flex-1 text-xs px-3 py-2 rounded bg-neutral-800 hover:bg-neutral-700 disabled:opacity-40 font-bold">
                      Submit
                    </button>
                    <button onClick={() => { setNoteMode(null); setNote(''); }}
                      className="text-xs px-3 py-2 rounded border border-neutral-700 hover:bg-neutral-900">
                      Cancel
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <button onClick={() => decide('approve')} disabled={!!busy}
                    className="w-full flex items-center justify-center gap-2 text-xs px-3 py-2.5 rounded bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 hover:bg-emerald-500/20 disabled:opacity-40 font-bold">
                    <Lock size={13} /> Approve &amp; lock scene
                  </button>
                  <button onClick={() => setNoteMode('revise')} disabled={!!busy}
                    className="w-full flex items-center justify-center gap-2 text-xs px-3 py-2 rounded border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40">
                    <RotateCcw size={13} /> Request a revision
                  </button>
                  <button onClick={() => setNoteMode('reject')} disabled={!!busy}
                    className="w-full flex items-center justify-center gap-2 text-xs px-3 py-2 rounded border border-neutral-800 text-neutral-400 hover:bg-neutral-900 disabled:opacity-40">
                    <XCircle size={13} /> Reject scene
                  </button>
                  <div className="text-[10px] text-neutral-600 text-center pt-1">
                    Approving locks the scene. Later autonomous passes cannot change it.
                  </div>
                </>
              )}
            </div>

            {scene.revisionHistory.length > 0 && (
              <div className="border border-neutral-800 rounded-lg bg-neutral-950 p-4 space-y-1">
                <div className="text-[10px] uppercase tracking-wider text-neutral-500">History</div>
                {scene.revisionHistory.map((h, i) => (
                  <div key={i} className="text-[10px] text-neutral-500 flex gap-2">
                    <ChevronRight size={10} className="mt-0.5 shrink-0" />
                    <span>{h.actor.toLowerCase()} · {h.from} → {h.to}{h.note ? ` · "${h.note}"` : ''}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
