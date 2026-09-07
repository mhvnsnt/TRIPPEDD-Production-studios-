import { describe, it, expect } from 'vitest';
import { SceneApprovalStore, LockedSceneError, InvalidTransitionError } from '../approval';
import type { EditorialSceneCandidate } from '../types';

let n = 0;
function scene(over: Partial<EditorialSceneCandidate> = {}): EditorialSceneCandidate {
  return {
    id: `s${n++}`, productionUnitId: 'u1', proposedTitle: 'Scene', purpose: 'p',
    sourceEvidenceIds: ['e1'], sourceClipIds: ['c1'], transcriptSegmentIds: ['t1'],
    visualObservationIds: [], referenceIds: [], storyBeatIds: ['b1'],
    proposedOrder: 0, physicalOrder: 0,
    ranges: [{ sourceFileId: 'c1', startTime: 4, endTime: 11, derivedFromObservationIds: ['t1'] }],
    proposedDuration: 7, beatMap: [], excludedMaterial: [], confidence: 0.7,
    editorialRationale: 'r', chronologyAssumptions: [], missingEvidence: [], evidenceLimitations: [],
    requiredAssets: [], generatedAssetIds: [], humanReviewState: 'PROPOSED',
    revisionHistory: [], createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
    ...over,
  };
}

describe('Approval — the human gate', () => {
  it('a machine-assembled scene starts PROPOSED, never approved', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);
    expect(store.get(s.id)!.humanReviewState).toBe('PROPOSED');
    expect(store.isLocked(s.id)).toBe(false);
  });

  it('approve then lock records the creator decision', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);

    store.lock(s.id, 'looks right');
    expect(store.get(s.id)!.humanReviewState).toBe('LOCKED');
    const hist = store.get(s.id)!.revisionHistory;
    expect(hist.map((h) => h.to)).toEqual(['APPROVED', 'LOCKED']);
    expect(hist.every((h) => h.actor === 'CREATOR')).toBe(true);
    // History carries what the cut actually was at each step.
    expect(hist[0].rangesSnapshot?.[0].endTime).toBe(11);
  });

  it('rejects an invalid transition rather than silently allowing it', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);
    store.reject(s.id, 'not working');
    expect(() => store.transition(s.id, 'APPROVED', { actor: 'CREATOR' })).toThrow(InvalidTransitionError);
  });
});

describe('Approval — a locked scene cannot be silently rewritten', () => {
  it('refuses an autonomous edit to a locked scene', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);
    store.lock(s.id);

    expect(() =>
      store.applyMachineEdit(s.id, (sc) => { sc.ranges[0].endTime = 99; })
    ).toThrow(LockedSceneError);

    // The approved cut is untouched.
    expect(store.get(s.id)!.ranges[0].endTime).toBe(11);
  });

  it('excludes locked scenes from what a later autonomous pass may touch', () => {
    const store = new SceneApprovalStore();
    const a = scene(); const b = scene();
    store.addAll([a, b]);
    store.lock(a.id);

    const mutable = store.mutable().map((m) => m.id);
    expect(mutable).not.toContain(a.id);
    expect(mutable).toContain(b.id);
  });

  it('refuses a machine transition out of LOCKED', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);
    store.lock(s.id);
    expect(() => store.transition(s.id, 'REVISION_REQUESTED', { actor: 'MACHINE' })).toThrow(LockedSceneError);
  });

  it('only the creator may reopen a locked scene, and only deliberately', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);
    store.lock(s.id);

    const reopened = store.transition(s.id, 'REVISION_REQUESTED', { actor: 'CREATOR', note: 'second thoughts' });
    expect(reopened.humanReviewState).toBe('REVISION_REQUESTED');
    // Now editable again.
    store.applyMachineEdit(s.id, (sc) => { sc.proposedDuration = 5; });
    expect(store.get(s.id)!.proposedDuration).toBe(5);
  });

  it('allows autonomous edits before approval and records them as machine revisions', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);
    store.applyMachineEdit(s.id, (sc) => { sc.ranges[0].startTime = 5; }, 'tightened opening');

    expect(store.get(s.id)!.ranges[0].startTime).toBe(5);
    const rev = store.get(s.id)!.revisionHistory.at(-1)!;
    expect(rev.actor).toBe('MACHINE');
    expect(rev.note).toBe('tightened opening');
    // The pre-edit cut is preserved in history, never overwritten.
    expect(rev.rangesSnapshot![0].startTime).toBe(4);
  });
});

describe('Approval — revision and rejection workflows', () => {
  it('revision requested -> revised -> approved -> locked', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);

    store.requestRevision(s.id, 'trim the opening');
    expect(store.get(s.id)!.humanReviewState).toBe('REVISION_REQUESTED');

    store.transition(s.id, 'REVISED', { actor: 'MACHINE', note: 'trimmed' });
    store.lock(s.id, 'better');

    expect(store.get(s.id)!.humanReviewState).toBe('LOCKED');
    expect(store.get(s.id)!.revisionHistory.map((h) => h.to))
      .toEqual(['REVISION_REQUESTED', 'REVISED', 'APPROVED', 'LOCKED']);
  });

  it('a rejected scene is terminal and not eligible for autonomous edits', () => {
    const store = new SceneApprovalStore();
    const s = scene();
    store.add(s);
    store.reject(s.id, 'the joke does not land');

    expect(store.get(s.id)!.humanReviewState).toBe('REJECTED');
    expect(() => store.applyMachineEdit(s.id, () => {})).toThrow(/rejected/i);
    expect(store.mutable().map((m) => m.id)).not.toContain(s.id);
  });
});

describe('Approval — creator feedback persists and informs later work', () => {
  it('records a decision signal for every creator action', () => {
    const store = new SceneApprovalStore();
    const a = scene(); const b = scene(); const c = scene();
    store.addAll([a, b, c]);

    store.lock(a.id, 'good');
    store.requestRevision(b.id, 'too long');
    store.reject(c.id, 'redundant');

    const fb = store.getFeedback();
    expect(fb.map((f) => f.decision).sort()).toEqual(['APPROVED', 'REJECTED', 'REVISION_REQUESTED']);
    expect(fb.find((f) => f.decision === 'REJECTED')!.signals.rejectedReason).toBe('redundant');
  });

  it('summarises preferences without rewriting past decisions', () => {
    const store = new SceneApprovalStore();
    const a = scene({ proposedDuration: 10 });
    const b = scene({ proposedDuration: 20 });
    store.addAll([a, b]);
    store.lock(a.id);
    store.lock(b.id);

    const prefs = store.learnedPreferences();
    expect(prefs.approvals).toBe(2);
    expect(prefs.averageApprovedDuration).toBe(15);

    // Learning is read-only: the locked scenes are unchanged.
    expect(store.get(a.id)!.humanReviewState).toBe('LOCKED');
    expect(store.get(a.id)!.proposedDuration).toBe(10);
  });

  it('feedback survives further scenes being added', () => {
    const store = new SceneApprovalStore();
    const a = scene();
    store.add(a);
    store.lock(a.id, 'first');
    store.add(scene());

    expect(store.getFeedback().length).toBe(1);
    expect(store.getFeedback()[0].sceneId).toBe(a.id);
  });
});
