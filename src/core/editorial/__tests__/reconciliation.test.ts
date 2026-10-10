import { describe, it, expect } from 'vitest';
import { reconcileBeat, reconcileInventory, type ObservationWithSource } from '../reconciliation';
import { DEFAULT_STORY_INVENTORY, WALK_STORY_BEATS, JOE_STORY_BEATS } from '../storyInventory';

let n = 0;
function obs(sourceFileId: string, text: string, type = 'TRANSCRIPT_SEGMENT', t = 0): ObservationWithSource {
  return {
    id: `o${n++}`, type, text, startTime: t, endTime: t + 3,
    origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED',
    tool: 'faster-whisper', toolVersion: '1.2.1', sourceFileId,
  };
}

const beatOf = (id: string) => DEFAULT_STORY_INVENTORY.find((b) => b.id === id)!;

describe('Reconciliation — remembered material never becomes footage', () => {
  it('reports MISSING_SOURCE_MEDIA when nothing has been ingested', () => {
    const r = reconcileInventory([]);
    expect(r.observationCount).toBe(0);
    for (const b of r.beats) {
      expect(b.state).toBe('MISSING_SOURCE_MEDIA');
      expect(b.confidence).toBe(0);
      expect(b.evidence).toEqual([]);
    }
    // "We have no footage" is not "this never happened".
    expect(r.beats[0].rationale).toMatch(/cannot be looked for/i);
    expect(r.actionable).toEqual([]);
  });

  it('a beat with no matching evidence is NOT_FOUND with zero confidence', () => {
    const observations = [obs('clip1', 'we are just walking down the street here')];
    const r = reconcileBeat(beatOf('joe.tic_tacs'), observations);

    expect(r.state).toBe('NOT_FOUND');
    expect(r.confidence).toBe(0);
    expect(r.evidence).toEqual([]);
    // The wording must not overclaim.
    expect(r.rationale).toMatch(/not proof the event did not happen/i);
  });

  it('never fabricates evidence for an unmatched beat', () => {
    const r = reconcileInventory([obs('clip1', 'nothing relevant at all')]);
    for (const b of r.beats) {
      for (const e of b.evidence) {
        // Every piece of evidence must point at a real observation we supplied.
        expect(e.observationId).toBeTruthy();
        expect(e.sourceFileId).toBe('clip1');
      }
    }
  });
});

describe('Reconciliation — the motel clerk (partially mentioned)', () => {
  const clerk = beatOf('walk.motel_clerk');

  it('is seeded as a PARTIAL mention, not an explicit one', () => {
    expect(clerk.mentionStrength).toBe('PARTIAL');
    expect(clerk.evidenceClass).toBe('HUMAN_DIRECTION');
  });

  it('caps at PARTIALLY_FOUND even when several cues match', () => {
    const observations = [
      obs('clip3', 'go up to the front desk and ask the clerk for the room key', 'TRANSCRIPT_SEGMENT', 12),
      obs('clip3', 'the clerk said checkout is at eleven', 'TRANSCRIPT_SEGMENT', 30),
      obs('clip3', 'OFFICE', 'ON_SCREEN_TEXT', 5),
    ];
    const r = reconcileBeat(clerk, observations);

    // Multiple strong cues, but a vague memory cannot be confirmed by keywords.
    expect(r.state).toBe('PARTIALLY_FOUND');
    expect(r.state).not.toBe('FOUND');
    expect(r.confidence).toBeLessThanOrEqual(0.6);
    expect(r.evidence.length).toBeGreaterThan(0);
    expect(r.candidateSourceFileIds).toContain('clip3');
    expect(r.rationale).toMatch(/only partially described|human confirmation/i);
  });

  it('stays NOT_FOUND when the footage simply does not contain it', () => {
    const observations = [
      obs('clip1', 'we are walking to get cigars right now'),
      obs('clip2', 'give me my bag back'),
    ];
    const r = reconcileBeat(clerk, observations);

    expect(r.state).toBe('NOT_FOUND');
    expect(r.evidence).toEqual([]);
    // The gap is visible: every cue that found nothing is listed.
    expect(r.unmatchedCues.length).toBeGreaterThan(0);
  });

  it('is never actionable for autonomous assembly on its own', () => {
    const observations = [obs('clip3', 'the clerk at the front desk gave us the room key')];
    const r = reconcileInventory(observations);
    const clerkResult = r.beats.find((b) => b.beatId === 'walk.motel_clerk')!;

    expect(r.actionable.map((a) => a.beatId)).not.toContain('walk.motel_clerk');
    expect(r.blocked.map((a) => a.beatId)).toContain('walk.motel_clerk');
    expect(clerkResult.state).not.toBe('FOUND');
  });
});

describe('Reconciliation — explicitly mentioned material', () => {
  it('an explicit beat with concentrated evidence reaches FOUND', () => {
    const observations = [
      obs('clip2', 'hey that is my bag, give it back', 'TRANSCRIPT_SEGMENT', 8),
      obs('clip2', 'you took my bag man', 'TRANSCRIPT_SEGMENT', 14),
      obs('clip2', 'my bag is right there', 'TRANSCRIPT_SEGMENT', 22),
    ];
    const r = reconcileBeat(beatOf('walk.bag_interruption'), observations);

    expect(r.state).toBe('FOUND');
    expect(r.confidence).toBeGreaterThan(0.3);
    expect(r.candidateSourceFileIds[0]).toBe('clip2');
    expect(r.evidence.every((e) => e.startTime !== undefined)).toBe(true);
  });

  it('scattered weak evidence is AMBIGUOUS_MATCH rather than a hit', () => {
    // One cue, once each, across four unrelated clips.
    const observations = [
      obs('c1', 'pass me a cigar'), obs('c2', 'cigar'),
      obs('c3', 'cigar maybe'), obs('c4', 'a cigar somewhere'),
    ];
    const r = reconcileBeat(beatOf('walk.cigar_trip'), observations);

    expect(r.state).toBe('AMBIGUOUS_MATCH');
    expect(r.rationale).toMatch(/without a clear concentration|human/i);
  });

  it('records the exact cue and timestamp behind each match', () => {
    const observations = [obs('c9', 'lord we thank you, amen', 'TRANSCRIPT_SEGMENT', 41.5)];
    const r = reconcileBeat(beatOf('joe.prayer'), observations);

    expect(r.evidence.length).toBeGreaterThan(0);
    const e = r.evidence[0];
    expect(e.startTime).toBe(41.5);
    expect(e.tool).toBe('faster-whisper');
    expect(['lord', 'amen', 'pray', 'prayer', 'god', 'bless']).toContain(e.matchedCue);
    expect(e.excerpt).toContain('amen');
  });

  it('matches whole tokens, so "pack" does not fire on "backpack"', () => {
    const r = reconcileBeat(beatOf('walk.shumafied_pack'), [obs('c1', 'he had a backpack on')]);
    expect(r.state).toBe('NOT_FOUND');
  });
});

describe('Reconciliation — inventory shape', () => {
  it('covers every beat the creator described', () => {
    expect(WALK_STORY_BEATS.length).toBeGreaterThanOrEqual(11);
    expect(JOE_STORY_BEATS.length).toBeGreaterThanOrEqual(5);
    const r = reconcileInventory([obs('c1', 'anything')]);
    expect(r.beats.length).toBe(DEFAULT_STORY_INVENTORY.length);
    expect(Object.values(r.summary).reduce((a, b) => a + b, 0)).toBe(r.beats.length);
  });

  it('every seeded beat is HUMAN_DIRECTION, never an observation', () => {
    for (const b of DEFAULT_STORY_INVENTORY) {
      expect(b.evidenceClass).toBe('HUMAN_DIRECTION');
    }
  });
});
