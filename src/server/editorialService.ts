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
import { runnerRoot } from '../core/tools/execution/runnerRoot';
import type { EditorialSceneCandidate, StoryBeat } from '../core/editorial/types';
import type { MediaJob } from '../core/types';

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
      const local = (job as any).localMediaPath;
      if (local) this.mediaPaths.set(job.fileId, local);
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
