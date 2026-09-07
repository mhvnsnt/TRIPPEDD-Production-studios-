import { describe, it, expect } from 'vitest';
import { assembleScenes } from '../assembler';
import { classifyAll, classifySegment } from '../classification';
import { reconcileInventory, type ObservationWithSource } from '../reconciliation';
import { DEFAULT_STORY_INVENTORY } from '../storyInventory';

let n = 0;
function o(sourceFileId: string, text: string, start: number, end: number, type = 'TRANSCRIPT_SEGMENT'): ObservationWithSource {
  return {
    id: `ob${n++}`, type, text, startTime: start, endTime: end,
    origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED',
    tool: 'faster-whisper', toolVersion: '1.2.1', sourceFileId,
  };
}

/** A realistic raw clip: camera chatter, then the actual beat. */
function bagClip(): ObservationWithSource[] {
  return [
    o('c1', "the camera's rolling now", 2.5, 4),
    o('c1', 'hey that is my bag give it back', 4.2, 7),
    o('c1', 'you took my bag man', 7.2, 9),
    o('c1', 'my bag is right there', 9.2, 11),
    o('c1', 'cut', 12, 12.6),
  ];
}

function build(observations: ObservationWithSource[], narrativeOrder?: string[]) {
  const rec = reconcileInventory(observations, DEFAULT_STORY_INVENTORY);
  return assembleScenes({
    productionUnitId: 'unit1', observations, reconciled: rec.beats,
    beats: DEFAULT_STORY_INVENTORY, narrativeOrder,
  });
}

describe('Assembly — every range is real', () => {
  it('uses actual observation timestamps, never invented ones', () => {
    const obsv = bagClip();
    const scenes = build(obsv);
    expect(scenes.length).toBeGreaterThan(0);

    const known = obsv.map((x) => ({ s: x.startTime!, e: x.endTime! }));
    for (const sc of scenes) {
      for (const r of sc.ranges) {
        expect(r.endTime).toBeGreaterThan(r.startTime);
        // A range must sit inside the span of real observations for that file.
        const min = Math.min(...known.map((k) => k.s));
        const max = Math.max(...known.map((k) => k.e));
        expect(r.startTime).toBeGreaterThanOrEqual(min - 2);
        expect(r.endTime).toBeLessThanOrEqual(max + 2);
        // And must name the observations that justify it.
        expect(r.derivedFromObservationIds.length).toBeGreaterThan(0);
      }
    }
  });

  it('every scene traces back to evidence and a story beat', () => {
    const scenes = build(bagClip());
    for (const s of scenes) {
      expect(s.sourceEvidenceIds.length).toBeGreaterThan(0);
      expect(s.storyBeatIds.length).toBeGreaterThan(0);
      expect(s.sourceClipIds.length).toBeGreaterThan(0);
      expect(s.editorialRationale).toBeTruthy();
      expect(s.humanReviewState).toBe('PROPOSED');
    }
  });

  it('never assembles a scene from a beat that was not FOUND', () => {
    // Only clerk-adjacent chatter: the beat is PARTIAL and cannot be FOUND.
    const obsv = [o('c5', 'the clerk at the front desk gave us the room key', 3, 6)];
    const rec = reconcileInventory(obsv, DEFAULT_STORY_INVENTORY);
    const scenes = assembleScenes({
      productionUnitId: 'u', observations: obsv, reconciled: rec.beats, beats: DEFAULT_STORY_INVENTORY,
    });
    expect(scenes.some((s) => s.storyBeatIds.includes('walk.motel_clerk'))).toBe(false);
  });

  it('produces nothing at all when no media has been ingested', () => {
    expect(build([])).toEqual([]);
  });
});

describe('Assembly — production artifacts are excluded, not deleted', () => {
  it('keeps camera chatter out of the cut while preserving it in source', () => {
    const scenes = build(bagClip());
    const s = scenes[0];

    const excl = s.excludedMaterial.find((e) => e.classification === 'CAMERA_DIRECTION');
    expect(excl, 'camera-direction chatter should be excluded').toBeTruthy();
    // The exclusion is explicit that source evidence survives.
    expect(excl!.preservedInPhysicalTimeline).toBe(true);
    expect(excl!.excerpt).toMatch(/rolling/i);

    // And the excluded stretch is genuinely absent from the cut.
    for (const r of s.ranges) {
      const overlaps = r.startTime < excl!.range.endTime && r.endTime > excl!.range.startTime;
      expect(overlaps).toBe(false);
    }
  });

  it('classifies unambiguous camera cues but flags ambiguous ones as UNCERTAIN', () => {
    const rolling = classifySegment(o('c1', "the camera's rolling now", 0, 2))!;
    expect(rolling.classification).toBe('CAMERA_DIRECTION');
    expect(rolling.ambiguous).toBe(false);

    // "let's go" is a camera cue in one clip and real dialogue in another.
    const letsGo = classifySegment(o('c1', "alright let's go", 0, 2))!;
    expect(letsGo.classification).toBe('UNCERTAIN');
    expect(letsGo.ambiguous).toBe(true);
  });

  it('an UNCERTAIN segment is kept in the cut and raised as an assumption', () => {
    const obsv = [
      o('c1', 'hey that is my bag give it back', 4, 7),
      o('c1', "well let's go", 7.2, 8),
      o('c1', 'you took my bag man', 8.2, 10),
      o('c1', 'my bag is right there', 10.2, 12),
    ];
    const s = build(obsv)[0];
    // Never silently cut on a guess.
    expect(s.chronologyAssumptions.some((a) => /camera cue/i.test(a.statement))).toBe(true);
    expect(s.excludedMaterial.some((e) => /let's go/i.test(e.excerpt ?? ''))).toBe(false);
  });

  it('surfaces long silences as dead-air candidates', () => {
    const segs = classifyAll([o('c1', 'first line', 0, 2), o('c1', 'second line', 20, 22)]);
    const dead = segs.find((s) => s.classification === 'DEAD_AIR');
    expect(dead).toBeTruthy();
    expect(dead!.startTime).toBe(2);
    expect(dead!.endTime).toBe(20);
  });
});

describe('Assembly — editorial order is independent of physical chronology', () => {
  const twoClips = () => [
    ...bagClip(),
    o('c2', 'lord we thank you for this day amen', 0, 3),
    o('c2', 'my name is joe nice to meet you', 3.5, 6),
    o('c2', 'you want a tic tac', 6.5, 8),
  ];

  it('reorders for narrative while retaining the physical position', () => {
    const scenes = build(twoClips(), ['joe.names_intros', 'walk.bag_interruption']);
    expect(scenes.length).toBeGreaterThanOrEqual(2);

    const joe = scenes.find((s) => s.storyBeatIds.includes('joe.names_intros'))!;
    const bag = scenes.find((s) => s.storyBeatIds.includes('walk.bag_interruption'))!;

    // Editorially Joe comes first...
    expect(joe.proposedOrder).toBeLessThan(bag.proposedOrder);
    // ...while the physical record still says the bag material came first.
    expect(bag.physicalOrder).toBeLessThan(joe.physicalOrder);
    // And the difference is stated, not hidden.
    expect(joe.reorderReason).toMatch(/physical chronology is unchanged/i);
  });

  it('falls back to physical order when no narrative order is given', () => {
    const scenes = build(twoClips());
    for (const s of scenes) {
      expect(s.proposedOrder).toBe(s.physicalOrder);
      expect(s.reorderReason).toBeUndefined();
    }
  });

  it('merges two beats that resolve to the same footage instead of duplicating it', () => {
    // "bag interruption" and "bag-return argument" both match the same argument.
    const scenes = build(bagClip());
    const bagScenes = scenes.filter((s) => s.sourceClipIds.includes('c1'));
    expect(bagScenes.length).toBe(1);
    expect(bagScenes[0].storyBeatIds.length).toBeGreaterThan(1);
    expect(bagScenes[0].editorialRationale).toMatch(/appears once/i);
  });

  it('assembles multiple scenes across multiple clips autonomously', () => {
    const scenes = build(twoClips());
    expect(scenes.length).toBeGreaterThanOrEqual(2);
    expect(new Set(scenes.flatMap((s) => s.sourceClipIds)).size).toBeGreaterThanOrEqual(2);
    // Orders are a dense sequence, not arbitrary numbers.
    expect(scenes.map((s) => s.proposedOrder).sort((a, b) => a - b)).toEqual(scenes.map((_, i) => i));
  });
});

describe('Assembly — beat map and gaps', () => {
  it('marks opening/payoff/exit against real ranges', () => {
    const s = build(bagClip())[0];
    const roles = s.beatMap.map((b) => b.role);
    expect(roles).toContain('OPENING');
    expect(roles).toContain('PAYOFF');
    expect(roles).toContain('EXIT');
    for (const b of s.beatMap) {
      expect(s.ranges.some((r) => r.startTime === b.range.startTime && r.sourceFileId === b.range.sourceFileId)).toBe(true);
    }
  });

  it('records cues that found no evidence as missing rather than ignoring them', () => {
    const s = build(bagClip())[0];
    expect(Array.isArray(s.missingEvidence)).toBe(true);
    expect(s.generatedAssetIds).toEqual([]);
  });
});
