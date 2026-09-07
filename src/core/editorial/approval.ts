/**
 * The human gate.
 *
 * Autonomous does not mean final. The editor may analyse, select, cut and build
 * a real timeline, but a scene only becomes LOCKED when the creator says so —
 * and once locked, no later autonomous pass may rewrite it. That guarantee is
 * enforced here rather than left to the discipline of every future caller.
 */
import type {
  EditorialSceneCandidate, SceneReviewState, SceneRevision, EditorialFeedback,
} from './types';

const ALLOWED: Record<SceneReviewState, SceneReviewState[]> = {
  PROPOSED: ['UNDER_REVIEW', 'APPROVED', 'REVISION_REQUESTED', 'REJECTED'],
  UNDER_REVIEW: ['APPROVED', 'REVISION_REQUESTED', 'REJECTED'],
  REVISION_REQUESTED: ['REVISED', 'REJECTED'],
  REVISED: ['UNDER_REVIEW', 'APPROVED', 'REVISION_REQUESTED', 'REJECTED'],
  APPROVED: ['LOCKED', 'REVISION_REQUESTED'],
  // Terminal. Nothing may leave these states automatically.
  LOCKED: [],
  REJECTED: [],
};

export class LockedSceneError extends Error {
  constructor(sceneId: string, attempted: string) {
    super(`scene ${sceneId} is LOCKED — ${attempted} refused. A locked scene records an approved creative decision and can only be reopened deliberately by the creator.`);
    this.name = 'LockedSceneError';
  }
}

export class InvalidTransitionError extends Error {
  constructor(from: SceneReviewState, to: SceneReviewState) {
    super(`invalid review transition ${from} -> ${to}`);
    this.name = 'InvalidTransitionError';
  }
}

export interface TransitionOptions {
  actor: 'MACHINE' | 'CREATOR';
  note?: string;
}

function revision(
  scene: EditorialSceneCandidate, to: SceneReviewState, o: TransitionOptions
): SceneRevision {
  return {
    at: new Date().toISOString(),
    from: scene.humanReviewState,
    to,
    actor: o.actor,
    note: o.note,
    // Snapshot the cut at each transition so history is a record, not a claim.
    rangesSnapshot: scene.ranges.map((r) => ({ ...r, derivedFromObservationIds: [...r.derivedFromObservationIds] })),
  };
}

export class SceneApprovalStore {
  private scenes = new Map<string, EditorialSceneCandidate>();
  private feedback: EditorialFeedback[] = [];

  add(scene: EditorialSceneCandidate): void {
    this.scenes.set(scene.id, scene);
  }
  addAll(scenes: EditorialSceneCandidate[]): void {
    for (const s of scenes) this.add(s);
  }
  get(id: string): EditorialSceneCandidate | undefined {
    return this.scenes.get(id);
  }
  all(): EditorialSceneCandidate[] {
    return [...this.scenes.values()].sort((a, b) => a.proposedOrder - b.proposedOrder);
  }
  getFeedback(): EditorialFeedback[] {
    return [...this.feedback];
  }

  /** Scenes an autonomous pass is still allowed to touch. */
  mutable(): EditorialSceneCandidate[] {
    return this.all().filter((s) => s.humanReviewState !== 'LOCKED' && s.humanReviewState !== 'REJECTED');
  }

  isLocked(id: string): boolean {
    return this.scenes.get(id)?.humanReviewState === 'LOCKED';
  }

  transition(id: string, to: SceneReviewState, o: TransitionOptions): EditorialSceneCandidate {
    const scene = this.scenes.get(id);
    if (!scene) throw new Error(`unknown scene ${id}`);

    if (scene.humanReviewState === 'LOCKED') {
      // Only the creator may reopen a locked scene, and only explicitly.
      if (!(o.actor === 'CREATOR' && to === 'REVISION_REQUESTED')) {
        throw new LockedSceneError(id, `transition to ${to}`);
      }
    } else if (!ALLOWED[scene.humanReviewState].includes(to)) {
      throw new InvalidTransitionError(scene.humanReviewState, to);
    }

    scene.revisionHistory.push(revision(scene, to, o));
    scene.humanReviewState = to;
    scene.updatedAt = new Date().toISOString();
    return scene;
  }

  /**
   * Apply an autonomous edit. Refused outright on a locked scene — this is the
   * guarantee that a later pass cannot silently rewrite approved work.
   */
  applyMachineEdit(
    id: string,
    mutate: (s: EditorialSceneCandidate) => void,
    note = 'autonomous revision'
  ): EditorialSceneCandidate {
    const scene = this.scenes.get(id);
    if (!scene) throw new Error(`unknown scene ${id}`);
    if (scene.humanReviewState === 'LOCKED') throw new LockedSceneError(id, 'autonomous edit');
    if (scene.humanReviewState === 'REJECTED') throw new Error(`scene ${id} was rejected; not eligible for autonomous edits`);

    const before = scene.ranges.map((r) => ({ ...r }));
    mutate(scene);
    scene.updatedAt = new Date().toISOString();
    scene.revisionHistory.push({
      at: new Date().toISOString(),
      from: scene.humanReviewState,
      to: scene.humanReviewState,
      actor: 'MACHINE',
      note,
      rangesSnapshot: before,
    });
    return scene;
  }

  approve(id: string, note?: string): EditorialSceneCandidate {
    return this.transition(id, 'APPROVED', { actor: 'CREATOR', note });
  }

  /** Approve then lock, the normal creator path for a finished scene. */
  lock(id: string, note?: string): EditorialSceneCandidate {
    const s = this.scenes.get(id);
    if (!s) throw new Error(`unknown scene ${id}`);
    if (s.humanReviewState !== 'APPROVED') this.transition(id, 'APPROVED', { actor: 'CREATOR', note });
    const locked = this.transition(id, 'LOCKED', { actor: 'CREATOR', note });
    this.recordFeedback(locked, 'APPROVED', note);
    return locked;
  }

  requestRevision(id: string, note: string): EditorialSceneCandidate {
    const s = this.transition(id, 'REVISION_REQUESTED', { actor: 'CREATOR', note });
    this.recordFeedback(s, 'REVISION_REQUESTED', note);
    return s;
  }

  reject(id: string, note: string): EditorialSceneCandidate {
    const s = this.transition(id, 'REJECTED', { actor: 'CREATOR', note });
    this.recordFeedback(s, 'REJECTED', note);
    return s;
  }

  private recordFeedback(
    scene: EditorialSceneCandidate,
    decision: EditorialFeedback['decision'],
    note?: string
  ): void {
    const first = scene.revisionHistory[0]?.rangesSnapshot;
    const originalDur = first?.reduce((a, r) => a + (r.endTime - r.startTime), 0);
    this.feedback.push({
      sceneId: scene.id,
      at: new Date().toISOString(),
      decision,
      note,
      signals: {
        keptRanges: scene.ranges.length,
        removedRanges: scene.excludedMaterial.length,
        durationDeltaSec:
          originalDur !== undefined
            ? Number((scene.proposedDuration - originalDur).toFixed(3))
            : undefined,
        preferredClassifications: scene.excludedMaterial.map((e) => e.classification),
        rejectedReason: decision === 'REJECTED' ? note : undefined,
      },
    });
  }

  /**
   * What the creator's decisions suggest for FUTURE proposals. Deliberately
   * read-only: learning informs the next scene, it never rewrites past ones.
   */
  learnedPreferences(): {
    approvals: number; rejections: number; revisions: number;
    averageApprovedDuration?: number;
    frequentlyExcluded: { classification: string; count: number }[];
  } {
    const approvals = this.feedback.filter((f) => f.decision === 'APPROVED');
    const counts = new Map<string, number>();
    for (const f of this.feedback) {
      for (const c of f.signals.preferredClassifications ?? []) {
        counts.set(c, (counts.get(c) ?? 0) + 1);
      }
    }
    const approvedScenes = approvals
      .map((f) => this.scenes.get(f.sceneId))
      .filter((s): s is EditorialSceneCandidate => !!s);

    return {
      approvals: approvals.length,
      rejections: this.feedback.filter((f) => f.decision === 'REJECTED').length,
      revisions: this.feedback.filter((f) => f.decision === 'REVISION_REQUESTED').length,
      averageApprovedDuration: approvedScenes.length
        ? Number((approvedScenes.reduce((a, s) => a + s.proposedDuration, 0) / approvedScenes.length).toFixed(2))
        : undefined,
      frequentlyExcluded: [...counts.entries()]
        .map(([classification, count]) => ({ classification, count }))
        .sort((a, b) => b.count - a.count),
    };
  }
}
