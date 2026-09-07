import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Play, Send, Check, X, RotateCcw, Loader2, Film, AlertTriangle,
  Sparkles, ListVideo, ChevronRight, Clapperboard, Upload, FileVideo,
} from 'lucide-react';

/**
 * The creator's screen.
 *
 * Watch the scene TRIPPEDD cut. Tell it what to change in plain words. Watch it
 * again. Approve. Next scene. No timelines, no codecs, no jargon — those live
 * underneath and stay there.
 */

interface Shot { label: string; seconds: number; from: string; line?: string }
interface Explanation { headline: string; did: string[]; unsure: string[]; shots: Shot[] }
interface Scene {
  id: string; proposedTitle: string; proposedDuration: number;
  humanReviewState: string; proposedOrder: number;
  ranges: { sourceFileId: string; startTime: number; endTime: number }[];
}
interface EpisodeStatus {
  totalScenes: number; approved: number; waitingOnYou: number; rejected: number;
  runningTimeSec: number; order: { position: number; title: string; seconds: number }[];
}
interface Turn { you: string; trippedd: string; problem?: string; at: number }

const QUICK = [
  'Cut that camera shit',
  'Make it shorter',
  'Hold on the ending longer',
  'Show me another version',
];

export function MakeTheShowWorkspace() {
  const [scene, setScene] = useState<Scene | null>(null);
  const [explain, setExplain] = useState<Explanation | null>(null);
  const [episode, setEpisode] = useState<EpisodeStatus | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [say, setSay] = useState('');
  const [turns, setTurns] = useState<Turn[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [remaining, setRemaining] = useState(0);
  const [episodeUrl, setEpisodeUrl] = useState<string | null>(null);
  const [footage, setFootage] = useState<{ name: string; bytes: number }[]>([]);
  const [uploading, setUploading] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const fileInput = useRef<HTMLInputElement | null>(null);

  const loadFootage = useCallback(async () => {
    try {
      const f = await (await fetch('/api/footage')).json();
      setFootage(f.files ?? []);
    } catch { /* surfaced by the error banner if it matters */ }
  }, []);

  /** Send the actual bytes; no base64, so a large clip does not balloon. */
  const upload = useCallback(async (files: FileList | File[]) => {
    const list = Array.from(files).filter((f) => /\.(mp4|mov|m4v|mkv|avi|webm)$/i.test(f.name));
    if (!list.length) { setErr('Those did not look like video files.'); return; }
    for (const f of list) {
      setUploading(f.name);
      try {
        const r = await fetch(`/api/footage/upload?name=${encodeURIComponent(f.name)}`, {
          method: 'POST', body: f,
        });
        if (!r.ok) throw new Error((await r.json()).error);
      } catch (e: any) { setErr(`${f.name}: ${e.message}`); }
    }
    setUploading(null);
    await loadFootage();
  }, [loadFootage]);

  /** Analyse the footage folder, then cut scenes from whatever it found. */
  const processFootage = useCallback(async () => {
    setBusy('thinking');
    setErr(null);
    try {
      await fetch('/api/footage/process', { method: 'POST' });
      // Analysis runs in the background; poll until the queue settles.
      for (let i = 0; i < 600; i++) {
        await new Promise((r) => setTimeout(r, 2000));
        const jobs = await (await fetch('/api/queue')).json();
        const busyStates = ['QUEUED', 'PROBING', 'ANALYZING', 'DOWNLOADING/STREAMING', 'RESOURCE_WAIT'];
        if (!jobs.some((j: any) => busyStates.includes(j.state))) break;
      }
      const r = await fetch('/api/editorial/build', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}',
      });
      if (!r.ok) throw new Error((await r.json()).error);
      await loadNextRef.current?.();
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  }, []);

  const loadNextRef = useRef<(() => Promise<void>) | null>(null);

  /** Pull the real footage from the configured Drive folder. */
  const getFromDrive = useCallback(async () => {
    setBusy('drive');
    setErr(null);
    try {
      const r = await fetch('/api/footage/from-drive', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}',
      });
      const d = await r.json();
      if (!d.ok) {
        // The real reason, not a shrug — and never a generated stand-in.
        setErr(`${d.blocker}${d.howToFix ? `\n\n${d.howToFix}` : ''}`);
        return;
      }
      await loadFootage();
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  }, [loadFootage]);

  const loadEpisode = useCallback(async () => {
    try { setEpisode(await (await fetch('/api/editorial/episode')).json()); } catch { /* shown elsewhere */ }
  }, []);

  /** Pull the next scene awaiting the creator, render it, and explain it. */
  const loadNext = useCallback(async (render = true) => {
    setBusy('loading');
    setErr(null);
    setTurns([]);
    try {
      const n = await (await fetch('/api/editorial/scenes/next')).json();
      setRemaining(n.remaining ?? 0);
      if (!n.scene) { setScene(null); setExplain(null); setVideoUrl(null); await loadEpisode(); return; }
      setScene(n.scene);

      if (render) {
        setBusy('rendering');
        const r = await (await fetch(`/api/editorial/scenes/${n.scene.id}/render`, { method: 'POST' })).json();
        // A version query defeats the browser cache after a re-cut.
        setVideoUrl(r.ok ? `/api/preview/${n.scene.id}?v=${r.version ?? 1}` : null);
        if (!r.ok) setErr(r.error ?? 'could not render this scene');
      }
      setExplain(await (await fetch(`/api/editorial/scenes/${n.scene.id}/explain`)).json());
      await loadEpisode();
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  }, [loadEpisode]);

  useEffect(() => { loadNextRef.current = () => loadNext(); }, [loadNext]);
  useEffect(() => { loadNext(); loadFootage(); }, [loadNext, loadFootage]);

  const makeScenes = async () => {
    setBusy('thinking');
    try {
      const r = await fetch('/api/editorial/build', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}',
      });
      if (!r.ok) throw new Error((await r.json()).error);
      await loadNext();
    } catch (e: any) { setErr(e.message); setBusy(null); }
  };

  const tell = async (text: string) => {
    if (!scene || !text.trim()) return;
    setBusy('working');
    setSay('');
    try {
      const out = await (await fetch(`/api/editorial/scenes/${scene.id}/instruct`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })).json();

      setTurns((t) => [...t, { you: text, trippedd: out.summary, problem: out.problem, at: Date.now() }]);

      if (out.scene?.humanReviewState === 'LOCKED' || out.scene?.humanReviewState === 'REJECTED') {
        await loadNext();
        return;
      }
      if (out.render?.ok) setVideoUrl(`/api/preview/${scene.id}?v=${out.render.version}`);
      setExplain(await (await fetch(`/api/editorial/scenes/${scene.id}/explain`)).json());
      const s = await (await fetch(`/api/editorial/scenes/${scene.id}`)).json();
      setScene(s.scene);
      await loadEpisode();
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  };

  const watchEpisode = async () => {
    setBusy('episode');
    try {
      const r = await (await fetch('/api/editorial/episode/render', { method: 'POST' })).json();
      if (!r.ok) throw new Error(r.error);
      // The episode renders under its own id; play it from the same route.
      setEpisodeUrl(`/api/preview/${r.outputPath.split('/').pop()?.replace('.mp4', '')}`);
      await loadEpisode();
    } catch (e: any) { setErr(e.message); } finally { setBusy(null); }
  };

  return (
    <div className="p-6 max-w-[1500px] mx-auto text-neutral-200">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <Clapperboard size={20} className="text-neutral-300" />
          <h1 className="text-lg font-bold tracking-tight">MAKE THE SHOW</h1>
          {episode && (
            <span className="text-xs text-neutral-500">
              {episode.approved} scene{episode.approved === 1 ? '' : 's'} done
              {episode.runningTimeSec ? ` · ${Math.round(episode.runningTimeSec)}s` : ''}
              {episode.waitingOnYou ? ` · ${episode.waitingOnYou} waiting on you` : ''}
            </span>
          )}
        </div>
        <div className="flex gap-2">
          <button onClick={getFromDrive} disabled={!!busy || !!uploading}
            className="flex items-center gap-2 text-sm px-4 py-2 rounded-lg border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40">
            {busy === 'drive' ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
            {busy === 'drive' ? 'Getting your footage…' : 'Get my footage from Drive'}
          </button>
          <button onClick={() => fileInput.current?.click()} disabled={!!busy || !!uploading}
            className="flex items-center gap-2 text-sm px-4 py-2 rounded-lg border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40">
            <Upload size={15} />Add footage
          </button>
          <input ref={fileInput} type="file" accept="video/*" multiple hidden
            onChange={(e) => e.target.files && upload(e.target.files)} />
          <button onClick={makeScenes} disabled={!!busy}
            className="flex items-center gap-2 text-sm px-4 py-2 rounded-lg bg-neutral-100 text-neutral-900 font-semibold hover:bg-white disabled:opacity-40">
            {busy === 'thinking' ? <Loader2 size={15} className="animate-spin" /> : <Sparkles size={15} />}
            {busy === 'thinking' ? 'Watching your footage…' : 'Make the scenes'}
          </button>
          {!!episode?.approved && (
            <button onClick={watchEpisode} disabled={!!busy}
              className="flex items-center gap-2 text-sm px-4 py-2 rounded-lg border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40">
              <ListVideo size={15} />Watch the episode
            </button>
          )}
        </div>
      </div>

      {err && (
        <div className="mb-4 border border-red-500/25 bg-red-500/5 rounded-lg p-3 text-sm text-red-400 flex gap-2">
          <AlertTriangle size={15} className="mt-0.5 shrink-0" />{err}
        </div>
      )}

      {episodeUrl && (
        <div className="mb-5 border border-neutral-800 rounded-xl overflow-hidden bg-neutral-950">
          <div className="px-4 py-2.5 border-b border-neutral-800 text-sm font-bold">YOUR EPISODE</div>
          <video src={episodeUrl} controls autoPlay className="w-full bg-black max-h-[60vh]" />
        </div>
      )}

      {/* Drop footage in */}
      {!scene && !busy && (
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => { e.preventDefault(); setDragOver(false); upload(e.dataTransfer.files); }}
          className={`mb-5 border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
            dragOver ? 'border-neutral-400 bg-neutral-900' : 'border-neutral-800 bg-neutral-950'}`}
        >
          <Upload size={26} className="mx-auto text-neutral-600 mb-3" />
          <div className="font-bold text-sm">
            {uploading ? `Uploading ${uploading}…` : 'Drop your footage here'}
          </div>
          <div className="text-xs text-neutral-500 mt-1">
            or press <b>Add footage</b> above. mp4, mov, mkv, avi, webm.
          </div>

          {footage.length > 0 && (
            <div className="mt-5 text-left max-w-lg mx-auto space-y-1">
              <div className="text-[10px] uppercase tracking-wider text-neutral-500 mb-1.5">
                {footage.length} clip{footage.length === 1 ? '' : 's'} ready
              </div>
              {footage.slice(0, 8).map((f) => (
                <div key={f.name} className="flex items-center justify-between text-xs text-neutral-400">
                  <span className="flex items-center gap-1.5 truncate">
                    <FileVideo size={12} className="shrink-0 text-neutral-600" />{f.name}
                  </span>
                  <span className="text-neutral-600 tabular-nums shrink-0 ml-3">
                    {(f.bytes / 1048576).toFixed(1)} MB
                  </span>
                </div>
              ))}
              {footage.length > 8 && <div className="text-xs text-neutral-600">+{footage.length - 8} more</div>}

              <button onClick={processFootage} disabled={!!busy || !!uploading}
                className="mt-4 w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-neutral-100 text-neutral-900 font-bold hover:bg-white disabled:opacity-40">
                <Sparkles size={16} />
                Watch my footage and cut the scenes
              </button>
            </div>
          )}
        </div>
      )}

      {/* Nothing to review */}
      {!scene && !busy && footage.length === 0 && (
        <div className="border border-neutral-800 rounded-xl bg-neutral-950 p-12 text-center">
          <Film size={30} className="mx-auto text-neutral-600 mb-4" />
          {episode?.approved ? (
            <>
              <div className="font-bold">Every scene is approved.</div>
              <div className="text-sm text-neutral-500 mt-1">
                {episode.approved} scenes, {Math.round(episode.runningTimeSec)}s. Watch the episode above.
              </div>
            </>
          ) : (
            <>
              <div className="font-bold">No scenes yet.</div>
              <div className="text-sm text-neutral-500 mt-1">
                Add footage, then press <b>Make the scenes</b> and I'll watch it and cut something together.
              </div>
            </>
          )}
        </div>
      )}

      {scene && (
        <div className="grid grid-cols-5 gap-5">
          {/* ---------------- WATCH + TALK ---------------- */}
          <div className="col-span-3 space-y-4">
            <div className="border border-neutral-800 rounded-xl overflow-hidden bg-neutral-950">
              <div className="px-4 py-3 border-b border-neutral-800 flex items-center justify-between">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-[11px] px-2 py-0.5 rounded bg-neutral-800 text-neutral-300 shrink-0">
                    Scene {scene.proposedOrder + 1}
                  </span>
                  <h2 className="font-bold truncate">{scene.proposedTitle}</h2>
                </div>
                <span className="text-xs text-neutral-500 shrink-0">
                  {scene.proposedDuration.toFixed(1)}s{remaining > 1 ? ` · ${remaining - 1} more after this` : ''}
                </span>
              </div>

              <div className="bg-black aspect-video relative">
                {busy === 'rendering' || busy === 'working' ? (
                  <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 text-neutral-400">
                    <Loader2 size={26} className="animate-spin" />
                    <span className="text-sm">{busy === 'working' ? 'Re-cutting it…' : 'Cutting the scene together…'}</span>
                  </div>
                ) : videoUrl ? (
                  // Two sources: the browser plays whichever codec it supports.
                  <video ref={videoRef} key={videoUrl} controls className="w-full h-full">
                    <source src={videoUrl} type="video/mp4" />
                    <source src={`${videoUrl}${videoUrl.includes('?') ? '&' : '?'}f=webm`} type="video/webm" />
                  </video>
                ) : (
                  <div className="absolute inset-0 flex items-center justify-center text-neutral-600 text-sm px-8 text-center">
                    Couldn't cut this one together. The footage may not be on this machine.
                  </div>
                )}
              </div>

              {/* Talk to it */}
              <div className="p-3 border-t border-neutral-800 space-y-2">
                <div className="flex gap-2">
                  <input
                    value={say} onChange={(e) => setSay(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter' && !busy) tell(say); }}
                    placeholder="Tell me what to change — “cut that camera shit”, “hold on her longer”, “start with the argument”"
                    disabled={!!busy}
                    className="flex-1 bg-neutral-900 border border-neutral-700 rounded-lg px-3 py-2.5 text-sm placeholder:text-neutral-600 focus:outline-none focus:border-neutral-500 disabled:opacity-50"
                  />
                  <button onClick={() => tell(say)} disabled={!!busy || !say.trim()}
                    className="px-4 rounded-lg bg-neutral-100 text-neutral-900 font-semibold disabled:opacity-30">
                    {busy === 'working' ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
                  </button>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {QUICK.map((q) => (
                    <button key={q} onClick={() => tell(q)} disabled={!!busy}
                      className="text-[11px] px-2.5 py-1 rounded-full border border-neutral-700 text-neutral-400 hover:bg-neutral-900 hover:text-neutral-200 disabled:opacity-40">
                      {q}
                    </button>
                  ))}
                </div>
              </div>

              {/* Decisions */}
              <div className="p-3 border-t border-neutral-800 flex gap-2">
                <button onClick={() => tell("That's good.")} disabled={!!busy}
                  className="flex-1 flex items-center justify-center gap-2 py-3 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 font-bold hover:bg-emerald-500/25 disabled:opacity-40">
                  <Check size={16} /> That's good — next scene
                </button>
                <button onClick={() => tell('Show me another version')} disabled={!!busy}
                  className="flex items-center gap-2 px-4 rounded-lg border border-neutral-700 hover:bg-neutral-900 text-sm disabled:opacity-40">
                  <RotateCcw size={14} /> Another version
                </button>
                <button onClick={() => tell('Reject this')} disabled={!!busy}
                  className="flex items-center gap-2 px-4 rounded-lg border border-neutral-800 text-neutral-400 hover:bg-neutral-900 text-sm disabled:opacity-40">
                  <X size={14} /> Drop it
                </button>
              </div>
            </div>

            {/* Conversation */}
            {turns.length > 0 && (
              <div className="border border-neutral-800 rounded-xl bg-neutral-950 p-4 space-y-3">
                {turns.map((t) => (
                  <div key={t.at} className="space-y-1">
                    <div className="text-sm text-neutral-300">
                      <span className="text-neutral-500 text-xs mr-2">YOU</span>{t.you}
                    </div>
                    <div className={`text-sm ${t.problem ? 'text-amber-400' : 'text-emerald-300'}`}>
                      <span className="text-neutral-500 text-xs mr-2">TRIPPEDD</span>
                      {t.problem ?? t.trippedd}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* ---------------- WHAT IT DID ---------------- */}
          <div className="col-span-2 space-y-4">
            {explain && (
              <>
                <div className="border border-neutral-800 rounded-xl bg-neutral-950 p-4 space-y-3">
                  <div className="text-[10px] uppercase tracking-wider text-neutral-500">What I did</div>
                  <p className="text-sm text-neutral-400">{explain.headline}</p>
                  <ul className="space-y-2">
                    {explain.did.map((d, i) => (
                      <li key={i} className="text-sm text-neutral-300 flex gap-2">
                        <ChevronRight size={14} className="mt-0.5 shrink-0 text-neutral-600" />{d}
                      </li>
                    ))}
                  </ul>
                </div>

                {explain.unsure.length > 0 && (
                  <div className="border border-amber-500/25 bg-amber-500/5 rounded-xl p-4 space-y-2">
                    <div className="text-[10px] uppercase tracking-wider text-amber-400">What I'm not sure about</div>
                    {/* Stated up front so approval is never a blind bet. */}
                    {explain.unsure.map((u, i) => (
                      <div key={i} className="text-sm text-neutral-300">{u}</div>
                    ))}
                  </div>
                )}

                <div className="border border-neutral-800 rounded-xl bg-neutral-950 p-4 space-y-2">
                  <div className="text-[10px] uppercase tracking-wider text-neutral-500">The cut</div>
                  {explain.shots.map((s, i) => (
                    <div key={i} className="text-xs border-t border-neutral-900 pt-2 first:border-0 first:pt-0">
                      <div className="flex justify-between text-neutral-400">
                        <span className="font-semibold text-neutral-300">{s.label}</span>
                        <span className="tabular-nums">{s.seconds}s</span>
                      </div>
                      {s.line && <div className="text-neutral-500 italic mt-0.5">"{s.line}"</div>}
                    </div>
                  ))}
                </div>
              </>
            )}

            {episode && episode.order.length > 0 && (
              <div className="border border-neutral-800 rounded-xl bg-neutral-950 p-4 space-y-1.5">
                <div className="text-[10px] uppercase tracking-wider text-neutral-500">Episode so far</div>
                {episode.order.map((o) => (
                  <div key={o.position} className="flex justify-between text-xs text-neutral-400">
                    <span>{o.position}. {o.title}</span>
                    <span className="tabular-nums text-neutral-600">{o.seconds.toFixed(1)}s</span>
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
