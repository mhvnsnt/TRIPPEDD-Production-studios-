import { describe, it, expect } from 'vitest';
import { EditorialService } from '../editorialService';
import type { MediaJob } from '../../core/types';

let n = 0;
function obs(sourceFileId: string, text: string, start: number, end: number, type = 'TRANSCRIPT_SEGMENT') {
  return {
    id: `eo${n++}`, type, text, startTime: start, endTime: end,
    origin: 'MACHINE_GENERATED' as const, reviewState: 'UNREVIEWED' as const,
    tool: 'faster-whisper', toolVersion: '1.2.1', sourceFileId,
  };
}

function job(fileId: string, observations: any[], localMediaPath?: string): MediaJob {
  const j: any = {
    id: `J_${fileId}`, fileId, originalName: `${fileId}.mp4`, mimeType: 'video/mp4',
    state: 'NEEDS_REVIEW', progress: 100, logs: [], createdAt: '', updatedAt: '',
    tools: {}, evidenceRefs: observations.map((o) => o.id),
  };
  j.observations = observations;
  if (localMediaPath) j.localMediaPath = localMediaPath;
  return j;
}

const bagJob = () => job('c1', [
  obs('c1', "the camera's rolling now", 2.5, 4),
  obs('c1', 'hey that is my bag give it back', 4.2, 7),
  obs('c1', 'you took my bag man', 7.2, 9),
  obs('c1', 'my bag is right there', 9.2, 11),
], '/media/c1.mp4');

describe('EditorialService — evidence intake', () => {
  it('collects observations from finished jobs and dedupes across rebuilds', () => {
    const svc = new EditorialService();
    const j = bagJob();
    expect(svc.ingestFromJobs([j])).toBe(4);
    // Ingesting the same job again adds nothing.
    expect(svc.ingestFromJobs([j])).toBe(0);
    expect(svc.getObservations().length).toBe(4);
  });

  it('records the retained media path so an export can reference it', () => {
    const svc = new EditorialService();
    svc.ingestFromJobs([bagJob()]);
    expect(svc.getMediaPath('c1')).toBe('/media/c1.mp4');
  });

  it('ignores jobs that produced no evidence', () => {
    const svc = new EditorialService();
    expect(svc.ingestFromJobs([job('empty', [])])).toBe(0);
    expect(svc.build().scenes).toEqual([]);
  });
});

describe('EditorialService — build preserves creator decisions', () => {
  it('a locked scene survives a rebuild untouched', () => {
    const svc = new EditorialService();
    svc.ingestFromJobs([bagJob()]);
    const first = svc.build();
    expect(first.scenes.length).toBeGreaterThan(0);

    const id = first.scenes[0].id;
    const originalEnd = first.scenes[0].ranges[0].endTime;
    svc.getStore().lock(id, 'approved');

    const second = svc.build();
    const kept = second.scenes.find((s) => s.id === id)!;

    expect(second.preserved).toBe(1);
    expect(kept.humanReviewState).toBe('LOCKED');
    expect(kept.ranges[0].endTime).toBe(originalEnd);
  });

  it('a rejected scene is not re-proposed on rebuild', () => {
    const svc = new EditorialService();
    svc.ingestFromJobs([bagJob()]);
    const first = svc.build();
    const id = first.scenes[0].id;
    const beats = first.scenes[0].storyBeatIds;
    svc.getStore().reject(id, 'not working');

    const second = svc.build();
    const proposedBeats = second.scenes
      .filter((s) => s.humanReviewState === 'PROPOSED')
      .flatMap((s) => s.storyBeatIds);
    for (const b of beats) expect(proposedBeats).not.toContain(b);
  });

  it('new evidence produces new scenes without disturbing locked ones', () => {
    const svc = new EditorialService();
    svc.ingestFromJobs([bagJob()]);
    const first = svc.build();
    svc.getStore().lock(first.scenes[0].id);

    svc.ingestFromJobs([job('c2', [
      obs('c2', 'my name is joe nice to meet you', 1, 4),
      obs('c2', 'call me joe', 4.2, 5.5),
    ], '/media/c2.mp4')]);
    const second = svc.build();

    expect(second.preserved).toBe(1);
    expect(second.scenes.length).toBeGreaterThan(first.scenes.length - 1);
    expect(second.scenes.find((s) => s.id === first.scenes[0].id)!.humanReviewState).toBe('LOCKED');
  });
});

describe('EditorialService — review queue', () => {
  it('hands back scenes one at a time and skips settled ones', () => {
    const svc = new EditorialService();
    svc.ingestFromJobs([bagJob(), job('c2', [
      obs('c2', 'my name is joe nice to meet you', 1, 4),
      obs('c2', 'call me joe', 4.2, 5.5),
    ])]);
    svc.build();

    const first = svc.nextForReview()!;
    expect(first).toBeTruthy();
    svc.getStore().lock(first.id);

    const next = svc.nextForReview();
    expect(next?.id).not.toBe(first.id);
    expect(svc.reviewQueue().map((s) => s.id)).not.toContain(first.id);
  });

  it('reports done when every scene is settled', () => {
    const svc = new EditorialService();
    svc.ingestFromJobs([bagJob()]);
    svc.build();
    for (const s of svc.reviewQueue()) svc.getStore().lock(s.id);
    expect(svc.nextForReview()).toBeUndefined();
  });
});

describe('EditorialService — transcript panel', () => {
  it('marks which lines are in the cut and which were removed', () => {
    const svc = new EditorialService();
    svc.ingestFromJobs([bagJob()]);
    const scene = svc.build().scenes[0];
    const lines = svc.transcriptFor(scene);

    expect(lines.length).toBeGreaterThan(0);
    // The camera cue is present but flagged as not included.
    const cue = lines.find((l) => /rolling/i.test(l.text));
    expect(cue, 'the excluded camera cue should still be shown').toBeTruthy();
    expect(cue!.included).toBe(false);
    // Real dialogue is included.
    expect(lines.some((l) => l.included && /bag/i.test(l.text))).toBe(true);
    // Ordered by time.
    expect(lines.map((l) => l.start)).toEqual([...lines.map((l) => l.start)].sort((a, b) => a - b));
  });
});

describe('EditorialService — export guards', () => {
  it('refuses to export when there are no scenes', async () => {
    const svc = new EditorialService();
    await expect(svc.exportProject('kdenlive')).rejects.toThrow(/no scenes/i);
  });

  it('refuses to export media it does not have', async () => {
    const svc = new EditorialService();
    // Job with evidence but no retained media path.
    svc.ingestFromJobs([job('c1', [
      obs('c1', 'hey that is my bag give it back', 4.2, 7),
      obs('c1', 'you took my bag man', 7.2, 9),
      obs('c1', 'my bag is right there', 9.2, 11),
    ])]);
    svc.build();
    await expect(svc.exportProject('kdenlive')).rejects.toThrow(/no local media resolved/i);
  });
});
