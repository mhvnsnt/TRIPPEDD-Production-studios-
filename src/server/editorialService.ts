/**
 * Editorial orchestration.
 *
 * Holds the one live editorial state for the app: observations gathered from
 * completed ingest jobs, the reconciliation of the creator's remembered material
 * against that evidence, the assembled scene candidates, and the approval store.
 *
 * Rebuilding is deliberately non-destructive: locked and rejected scenes are
 * carried through untouched, because a later autonomous pass must never rewrite
 * a decision the creator already made.
 */
import path from 'path';
import { reconcileInventory, type ObservationWithSource, type ReconciliationReport } from '../core/editorial/reconciliation';
import { DEFAULT_STORY_INVENTORY } from '../core/editorial/storyInventory';
import { assembleScenes } from '../core/editorial/assembler';
import { SceneApprovalStore } from '../core/editorial/approval';
import { exportOTIO, exportKdenlive, type ExportResult, MissingMediaError } from '../core/editorial/projectExport';
import { renderScene, MissingRenderMediaError, type RenderResult } from '../core/editorial/render/SceneRenderer';
import { parseInstruction, applyInstruction, type EditIntent } from '../core/editorial/naturalEdit';
import { explainScene, type SceneExplanation } from '../core/editorial/explain';
import { nameClips, type ClipName } from '../core/editorial/naming';
import { checkCanonCompliance, summariseCanonFailure, type CanonComplianceReport } from '../core/canon/canonCompliance';
import { runnerRoot } from '../core/tools/execution/runnerRoot';
import { executeTool } from '../core/tools/execution/executor';
import type { EditorialSceneCandidate, StoryBeat } from '../core/editorial/types';
import type { MediaJob } from '../core/types';

/**
 * A render either happened or was refused by the canon gate. The report rides
 * along either way, so a refusal is readable without a second request.
 */
export type EpisodeRenderResult = RenderResult & {
  sceneCount: number;
  sceneOrder: string[];
  canonStatus?: 'CANON_COMPLIANT' | 'CANON_COMPLIANCE_FAILED';
  canon?: CanonComplianceReport;
};

export interface EditorialBuildResult {
  reconciliation: ReconciliationReport;
  scenes: EditorialSceneCandidate[];
  preserved: number;
  observationCount: number;
  sourceFileCount: number;
  builtAt: string;
}

export class EditorialService {
  private store = new SceneApprovalStore();
  private observations: ObservationWithSource[] = [];
  private lastReconciliation?: ReconciliationReport;
  private lastBuiltAt?: string;
  private beats: StoryBeat[] = DEFAULT_STORY_INVENTORY;
  private narrativeOrder?: string[];
  /** sourceFileId -> local media path, for export. */
  private mediaPaths = new Map<string, string>();
  /** sourceFileId -> analyzers that were resource-blocked during its ingest. */
  private blockedTools: Record<string, string[]> = {};
  /** sceneId -> rendered preview on disk. */
  private renders = new Map<string, { path: string; durationSec: number; renderedAt: string; version: number }>();
  private ffmpegPath = '/usr/bin/ffmpeg';
  /** sourceFileId -> original filename, kept for the life of the project. */
  private originalNames: Record<string, string> = {};
  private durations: Record<string, number> = {};
  private clipNames: ClipName[] = [];

  getClipNames(): ClipName[] { return this.clipNames; }

  setFfmpegPath(p: string): void { this.ffmpegPath = p; }
  getRender(sceneId: string) { return this.renders.get(sceneId); }

  getStore(): SceneApprovalStore { return this.store; }
  getBeats(): StoryBeat[] { return this.beats; }
  getObservations(): ObservationWithSource[] { return this.observations; }
  getReconciliation(): ReconciliationReport | undefined { return this.lastReconciliation; }
  getLastBuiltAt(): string | undefined { return this.lastBuiltAt; }

  setNarrativeOrder(order: string[] | undefined): void { this.narrativeOrder = order; }
  registerMedia(sourceFileId: string, localPath: string): void { this.mediaPaths.set(sourceFileId, localPath); }
  getMediaPath(id: string): string | undefined { return this.mediaPaths.get(id); }
  getMediaMap(): Record<string, string> { return Object.fromEntries(this.mediaPaths); }

  /** Pull observations off every job that actually produced evidence. */
  ingestFromJobs(jobs: MediaJob[]): number {
    const seen = new Set(this.observations.map((o) => o.id));
    let added = 0;
    for (const job of jobs) {
      const obs = (job as any).observations as ObservationWithSource[] | undefined;
      if (!obs?.length) continue;
      for (const o of obs) {
        if (seen.has(o.id)) continue;
        seen.add(o.id);
        this.observations.push({ ...o, sourceFileId: o.sourceFileId ?? job.fileId });
        added++;
      }
      // The original filename is never lost, whatever we end up calling it.
      this.originalNames[job.fileId] = job.originalName || job.fileId;
      const probe = (job.tools as any)?.ffprobe?.data;
      const dur = Number(probe?.format?.duration);
      if (Number.isFinite(dur)) this.durations[job.fileId] = dur;

      const local = (job as any).localMediaPath;
      if (local) this.mediaPaths.set(job.fileId, local);
      const blocked = (job as any).resourceBlockedTools as string[] | undefined;
      if (blocked?.length) this.blockedTools[job.fileId] = blocked;
    }
    return added;
  }

  /**
   * Re-reconcile and re-assemble from current evidence. Scenes the creator has
   * LOCKED or REJECTED survive verbatim; only mutable ones are replaced.
   */
  build(): EditorialBuildResult {
    const reconciliation = reconcileInventory(this.observations, this.beats);

    const fresh = assembleScenes({
      productionUnitId: 'walk_ep1',
      observations: this.observations,
      reconciled: reconciliation.beats,
      beats: this.beats,
      narrativeOrder: this.narrativeOrder,
      blockedTools: this.blockedTools,
    });

    // Preserve creator decisions across rebuilds.
    const settled = this.store.all().filter(
      (s) => s.humanReviewState === 'LOCKED' || s.humanReviewState === 'REJECTED'
    );
    const settledBeats = new Set(settled.flatMap((s) => s.storyBeatIds));

    const next = new SceneApprovalStore();
    next.addAll(settled);
    for (const s of fresh) {
      // A beat already settled by the creator is not re-proposed.
      if (s.storyBeatIds.some((b) => settledBeats.has(b))) continue;
      next.add(s);
    }
    // Carry feedback history forward.
    for (const f of this.store.getFeedback()) (next as any).feedback?.push?.(f);

    // Give every clip a human name once the evidence is in.
    this.clipNames = nameClips({
      files: this.originalNames,
      durations: this.durations,
      observations: this.observations,
      reconciled: reconciliation.beats,
      beats: this.beats,
    });

    this.store = next;
    this.lastReconciliation = reconciliation;
    this.lastBuiltAt = new Date().toISOString();

    return {
      reconciliation,
      scenes: this.store.all(),
      preserved: settled.length,
      observationCount: this.observations.length,
      sourceFileCount: new Set(this.observations.map((o) => o.sourceFileId)).size,
      builtAt: this.lastBuiltAt,
    };
  }

  /** Scenes ready to show the creator, in editorial order. */
  reviewQueue(): EditorialSceneCandidate[] {
    return this.store.all().filter(
      (s) => s.humanReviewState !== 'LOCKED' && s.humanReviewState !== 'REJECTED'
    );
  }

  /** The next scene awaiting a decision — the scene-by-scene workflow. */
  nextForReview(): EditorialSceneCandidate | undefined {
    return this.reviewQueue()[0];
  }

  /** Transcript lines that fall inside a scene's ranges, for the review panel. */
  transcriptFor(scene: EditorialSceneCandidate) {
    const out: { start: number; end: number; text: string; included: boolean; sourceFileId: string }[] = [];
    for (const o of this.observations) {
      if (o.type !== 'TRANSCRIPT_SEGMENT' || !o.text) continue;
      if (!scene.sourceClipIds.includes(o.sourceFileId)) continue;
      const s = o.startTime ?? 0, e = o.endTime ?? s;

      const inCut = scene.ranges.some(
        (r) => r.sourceFileId === o.sourceFileId && e > r.startTime && s < r.endTime
      );
      const inExcluded = scene.excludedMaterial.some(
        (x) => x.range.sourceFileId === o.sourceFileId && e > x.range.startTime && s < x.range.endTime
      );
      if (inCut || inExcluded) {
        out.push({ start: s, end: e, text: o.text, included: inCut, sourceFileId: o.sourceFileId });
      }
    }
    return out.sort((a, b) => a.start - b.start);
  }

  /** Cuts the scene together into an actual watchable file. */
  async renderScene(sceneId: string): Promise<RenderResult & { version?: number }> {
    const scene = this.store.get(sceneId);
    if (!scene) throw new Error(`unknown scene ${sceneId}`);

    const outDir = path.join(runnerRoot(), '.trippedd_tools', 'previews');
    const prior = this.renders.get(sceneId);
    const version = (prior?.version ?? 0) + 1;

    const res = await renderScene({
      // Version the filename so the browser cannot serve a stale cut from cache
      // after the creator has asked for a change.
      sceneId: `${sceneId}_v${version}`,
      ranges: scene.ranges,
      resolveMedia: (id) => this.mediaPaths.get(id),
      outDir,
      ffmpegPath: this.ffmpegPath,
    });

    if (res.ok && res.outputPath) {
      this.renders.set(sceneId, {
        path: res.outputPath, durationSec: res.durationSec ?? 0,
        renderedAt: new Date().toISOString(), version,
      });
      // Transcode a VP9/WebM companion in the background. H.264 plays in every
      // normal browser, but not in builds shipped without proprietary codecs,
      // and a creator should never meet "no supported source" because of that.
      void this.makeWebm(res.outputPath);
    }
    return { ...res, version };
  }

  /** WebM companion so playback never depends on H.264 being available. */
  private async makeWebm(mp4Path: string): Promise<void> {
    const webm = mp4Path.replace(/\.mp4$/, '.webm');
    try {
      const { existsSync } = await import('fs');
      if (existsSync(webm)) return;
      await executeTool({
        tool: 'ffmpeg', version: 'preview-webm', executablePath: this.ffmpegPath,
        args: ['-y', '-v', 'error', '-i', mp4Path,
               '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34', '-deadline', 'realtime', '-cpu-used', '5',
               '-c:a', 'libopus', '-b:a', '96k', webm],
        sourceFileId: 'preview-webm', timeoutMs: 900_000,
      });
    } catch { /* the mp4 remains the primary; a missing companion is not fatal */ }
  }

  explain(sceneId: string): SceneExplanation | undefined {
    const scene = this.store.get(sceneId);
    if (!scene) return undefined;
    return explainScene(scene, this.observations);
  }

  /**
   * The creator types what they want; the cut changes and is re-rendered.
   * A locked scene refuses, and an instruction that was not understood changes
   * nothing and says so.
   */
  async instruct(sceneId: string, text: string): Promise<{
    intent: EditIntent;
    changed: boolean;
    summary: string;
    problem?: string;
    render?: RenderResult & { version?: number };
    scene?: EditorialSceneCandidate;
    reorderedTo?: number;
  }> {
    const scene = this.store.get(sceneId);
    if (!scene) throw new Error(`unknown scene ${sceneId}`);

    const intent = parseInstruction(text);

    if (intent.kind === 'APPROVE') {
      const locked = this.store.lock(sceneId, text);
      return { intent, changed: true, summary: 'Locked. Moving to the next scene.', scene: locked };
    }
    if (intent.kind === 'REJECT') {
      const rejected = this.store.reject(sceneId, text);
      return { intent, changed: true, summary: 'Dropped this version. Your footage is untouched.', scene: rejected };
    }
    if (intent.kind === 'REORDER') {
      const moved = this.reorderScene(scene, intent);
      return { intent, changed: moved !== undefined, summary: moved !== undefined
        ? `Moved "${scene.proposedTitle}" to position ${moved + 1} in the episode.`
        : 'I could not work out where to move it.', scene, reorderedTo: moved };
    }

    const outcome = applyInstruction(scene, intent, {
      observations: this.observations,
      excluded: scene.excludedMaterial,
    });

    if (!outcome.changed) {
      return { intent, changed: false, summary: outcome.summary, problem: outcome.problem };
    }

    // Record the change against the scene, keeping the previous cut in history.
    this.store.applyMachineEdit(sceneId, (s) => {
      s.ranges = outcome.ranges;
      s.excludedMaterial = outcome.excluded;
      s.proposedDuration = Number(outcome.ranges.reduce((a, r) => a + (r.endTime - r.startTime), 0).toFixed(3));
    }, `creator: "${text}"`);

    const render = await this.renderScene(sceneId);
    return { intent, changed: true, summary: outcome.summary, render, scene: this.store.get(sceneId) };
  }

  /** Moves a scene in the episode running order. */
  private reorderScene(scene: EditorialSceneCandidate, intent: EditIntent): number | undefined {
    const all = this.store.all();
    let target: number | undefined;

    if (intent.targetScene) {
      const want = intent.targetScene.toLowerCase();
      const match = all.find((s) => s.id !== scene.id && s.proposedTitle.toLowerCase().includes(want));
      if (match) target = intent.where === 'before' ? match.proposedOrder : match.proposedOrder + 1;
    } else if (intent.where === 'before') target = 0;
    else if (intent.where === 'after') target = all.length - 1;

    if (target === undefined) return undefined;

    const others = all.filter((s) => s.id !== scene.id).sort((a, b) => a.proposedOrder - b.proposedOrder);
    const clamped = Math.max(0, Math.min(others.length, target));
    others.splice(clamped, 0, scene);
    others.forEach((s, i) => { s.proposedOrder = i; s.updatedAt = new Date().toISOString(); });
    return clamped;
  }

  /**
   * Joins the approved scenes into a full episode the creator can watch.
   * Only locked/approved scenes go in — a draft nobody signed off is not the
   * episode.
   */
  async renderEpisode(): Promise<EpisodeRenderResult> {
    const approved = this.store.all()
      .filter((s) => s.humanReviewState === 'LOCKED' || s.humanReviewState === 'APPROVED')
      .sort((a, b) => a.proposedOrder - b.proposedOrder);

    if (!approved.length) {
      return {
        ok: false, segmentCount: 0, warnings: [], provenance: [],
        error: 'no approved scenes yet — approve at least one scene first',
        sceneCount: 0, sceneOrder: [],
      };
    }

    // The canon gate. A cut that breaks a locked decision does not get rendered
    // and does not get quietly repaired — the creator has had to restate the
    // EP01 order more than once, and a checker that fixes the order behind his
    // back is how it goes wrong again without anyone noticing.
    const canon = checkCanonCompliance(approved);
    if (!canon.ok) {
      return {
        ok: false, segmentCount: 0, warnings: [], provenance: [],
        error: summariseCanonFailure(canon),
        canonStatus: 'CANON_COMPLIANCE_FAILED',
        canon,
        sceneCount: approved.length,
        sceneOrder: approved.map((s) => s.proposedTitle),
      };
    }

    const ranges = approved.flatMap((s) => s.ranges);
    const res = await renderScene({
      sceneId: `episode_${Date.now().toString(36)}`,
      ranges,
      resolveMedia: (id) => this.mediaPaths.get(id),
      outDir: path.join(runnerRoot(), '.trippedd_tools', 'previews'),
      ffmpegPath: this.ffmpegPath,
    });

    return {
      ...res,
      canonStatus: 'CANON_COMPLIANT',
      canon,
      sceneCount: approved.length,
      sceneOrder: approved.map((s) => s.proposedTitle),
    };
  }

  /** The canon gate on its own, so the creator can see it before rendering. */
  canonCheck(): CanonComplianceReport {
    return checkCanonCompliance(
      this.store.all().filter((s) => s.humanReviewState !== 'REJECTED')
        .sort((a, b) => a.proposedOrder - b.proposedOrder)
    );
  }

  /** How the episode reads right now: what is locked, what is still open. */
  episodeStatus() {
    const all = this.store.all();
    const approved = all.filter((s) => s.humanReviewState === 'LOCKED' || s.humanReviewState === 'APPROVED')
      .sort((a, b) => a.proposedOrder - b.proposedOrder);
    return {
      totalScenes: all.length,
      approved: approved.length,
      waitingOnYou: all.filter((s) => s.humanReviewState === 'PROPOSED' || s.humanReviewState === 'REVISION_REQUESTED').length,
      rejected: all.filter((s) => s.humanReviewState === 'REJECTED').length,
      runningTimeSec: Number(approved.reduce((a, s) => a + s.proposedDuration, 0).toFixed(1)),
      order: approved.map((s, i) => ({ position: i + 1, title: s.proposedTitle, seconds: s.proposedDuration })),
    };
  }

  async exportProject(
    format: 'otio' | 'kdenlive',
    opts: { onlyApproved?: boolean; name?: string; outDir?: string } = {}
  ): Promise<ExportResult> {
    const all = this.store.all();
    const scenes = opts.onlyApproved
      ? all.filter((s) => s.humanReviewState === 'LOCKED' || s.humanReviewState === 'APPROVED')
      : all.filter((s) => s.humanReviewState !== 'REJECTED');

    if (!scenes.length) throw new Error('no scenes to export');

    const outDir = opts.outDir ?? path.join(runnerRoot(), '.trippedd_tools', 'edits');
    const resolve = (id: string) => this.mediaPaths.get(id);
    const name = opts.name ?? (opts.onlyApproved ? 'approved_cut' : 'working_cut');

    if (format === 'otio') {
      const py = path.join(runnerRoot(), '.trippedd_venv', 'bin', 'python');
      return exportOTIO(scenes, resolve, outDir, { name, pythonPath: py });
    }
    return exportKdenlive(scenes, resolve, outDir, { name });
  }
}

export { MissingMediaError };
export const editorialService = new EditorialService();
