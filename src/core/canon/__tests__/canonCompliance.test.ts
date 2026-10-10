/**
 * The canon gate has to fail for the right reason, and it must not repair.
 * Every test here builds a cut that is wrong in one specific way and asserts
 * the check names that constraint.
 */
import { describe, it, expect } from 'vitest';
import {
  checkCanonCompliance, resolveCanonSegment, summariseCanonFailure,
  type AssemblyScene,
} from '../canonCompliance';
import { EP01_LOCKED_ORDER, EPISODE_01, EP01_UNPLACED_CANON, UNKNOWN_STYLE } from '../episode01';
import { BLUEPRINT_CONSTRAINT_IDS, ASSEMBLY_CONSTRAINT_IDS } from '../canonCompliance';

function scene(id: string, title: string, order: number, extra: Partial<AssemblyScene> = {}): AssemblyScene {
  return { id, proposedTitle: title, proposedOrder: order, physicalOrder: order, ...extra };
}

/** A cut in the locked order, mapped by title. */
function goodCut(): AssemblyScene[] {
  return [
    scene('s1', 'Cold Open', 0),
    scene('s2', 'Motel', 1),
    scene('s3', 'Shumafied', 2),
    scene('s4', 'Shumafied Disappointment + Cigar Setup', 3),
    scene('s5', 'Luck of the Irish', 4),
    scene('s6', 'Cigars / The Walk', 5),
    scene('s7', 'Bag Sequence', 6),
    scene('s8', 'Joe', 7),
    scene('s9', 'TV', 8, { canonSegmentId: 'EP01_TV' }),
    scene('s10', 'Clothed and Confused', 9),
    scene('s11', 'Smoking / Hanging Out', 10),
  ];
}

describe('canon compliance — the blueprint itself', () => {
  it('passes on the canon as committed', () => {
    const r = checkCanonCompliance();
    expect(r.violations).toEqual([]);
    expect(r.status).toBe('CANON_COMPLIANT');
  });

  it('reports the number of constraints it actually evaluated', () => {
    const r = checkCanonCompliance();
    expect(r.constraintsChecked).toBe(BLUEPRINT_CONSTRAINT_IDS.length);
    expect(checkCanonCompliance(goodCut()).constraintsChecked)
      .toBe(BLUEPRINT_CONSTRAINT_IDS.length + ASSEMBLY_CONSTRAINT_IDS.length);
    expect(r.canonDoc).toBe('docs/creative/EP01-THE-WALK-CANON.md');
  });
});

/**
 * A gate that passes on the committed canon proves nothing on its own — it
 * would also pass if it checked nothing. Each test here breaks the blueprint
 * the way a co-developer would, and asserts the specific constraint fires.
 * The blueprint is restored afterwards.
 */
describe('canon compliance — the blueprint checks are not decorative', () => {
  function withSegment<T>(id: string, mutate: (t: any) => void, assertion: () => T): T {
    const s = EPISODE_01.find((x) => x.id === id)!;
    const before = JSON.parse(JSON.stringify(s));
    try { mutate(s); return assertion(); }
    finally { Object.assign(s, before); }
  }
  const ids = () => checkCanonCompliance().violations.map((v) => v.constraintId);

  it('C02/C01 fire when the locked order is edited', () => {
    withSegment('EP01_COLD_OPEN', (s) => { s.position = 99; }, () => {
      const v = ids();
      expect(v).toContain('C01_LOCKED_ORDER_INTACT');
      expect(v).toContain('C02_COLD_OPEN_FIRST');
    });
  });

  it('C03 fires when Luck of the Irish is moved after the cigar trip', () => {
    withSegment('EP01_LUCK_OF_THE_IRISH', (s) => { s.position = 6.5; }, () => {
      expect(ids()).toContain('C03_IRISH_BETWEEN_LETDOWN_AND_CIGARS');
    });
  });

  it('C04 fires when Joe is relabelled as captured footage', () => {
    withSegment('EP01_JOE', (s) => {
      s.treatment.footageExists = true;
      s.treatment.sourceReality = 'REAL_EVENT';
      s.treatment.method = 'LIVE_ACTION';
    }, () => {
      expect(ids()).toContain('C04_JOE_IS_RECONSTRUCTION');
    });
  });

  it('C04 fires when the 2D language is dropped from Joe', () => {
    withSegment('EP01_JOE', (s) => { s.treatment.visualTreatment = 'A reconstruction of the encounter.'; }, () => {
      expect(ids()).toContain('C04_JOE_IS_2D');
    });
  });

  it('C05 fires when Clothed and Confused loses the not-2D/not-3D exclusion', () => {
    withSegment('EP01_CLOTHED_AND_CONFUSED', (s) => {
      s.treatment.visualTreatment = 'Realistic survival-documentary look.';
    }, () => {
      expect(ids()).toContain('C05_CLOTHED_AND_CONFUSED_NOT_2D_OR_3D');
    });
  });

  it('C05 fires when Clothed and Confused is positively classified as animated', () => {
    withSegment('EP01_CLOTHED_AND_CONFUSED', (s) => {
      s.treatment.visualTreatment =
        'Realistic 2D animated survival parody. It is not 2D in the cartoon sense, not a 3D cartoon.';
    }, () => {
      expect(ids()).toContain('C05_CLOTHED_AND_CONFUSED_CLASSIFIED_ANIMATED');
    });
  });

  it('C05 does NOT fire on the committed wording, which is full of the words it rules out', () => {
    // The real treatment says "IT IS NOT 2D. IT IS NOT A BLENDER-LOOKING 3D
    // CARTOON." A naive keyword scan flags exactly that sentence.
    expect(ids()).not.toContain('C05_CLOTHED_AND_CONFUSED_CLASSIFIED_ANIMATED');
    expect(ids()).not.toContain('C05_CLOTHED_AND_CONFUSED_NOT_2D_OR_3D');
  });

  it('C06 fires when McBrain Feed stops being recorded as a separate segment', () => {
    withSegment('EP01_TV', (s) => { s.treatment.visualTreatment = 'Live-action TV watching.'; }, () => {
      expect(ids()).toContain('C06_MCBRAIN_FEED_SEPARATE');
    });
  });

  it('C08 fires when an unrecorded style is marked as locked canon', () => {
    withSegment('EP01_COLD_OPEN', (s) => {
      s.treatment.visualTreatment = UNKNOWN_STYLE;
      s.treatment.visualTreatmentStatus = 'LOCKED_CANON';
    }, () => {
      expect(ids()).toContain('C08_UNRECORDED_STYLE_NEVER_LOCKED');
    });
  });

  it('C09 fires when a segment with no footage is called live action', () => {
    withSegment('EP01_CLOTHED_AND_CONFUSED', (s) => { s.treatment.method = 'LIVE_ACTION'; }, () => {
      expect(ids()).toContain('C09_METHOD_NOT_COLLAPSED');
    });
  });

  it('C07 fires when the Goodville gag family is collapsed to one gag', () => {
    const g = EP01_UNPLACED_CANON.find((u) => u.id === 'GOODVILLE')! as any;
    const before = g.knownMembers;
    try {
      g.knownMembers = ['Goodville Geography (SEG03, DOCUMENTARY_GAG)'];
      expect(ids()).toContain('C07_GOODVILLE_IS_A_GAG_FAMILY');
    } finally { g.knownMembers = before; }
  });
});

describe('canon compliance — the assembled cut', () => {
  it('passes a cut in the locked order', () => {
    const r = checkCanonCompliance(goodCut());
    expect(r.ok).toBe(true);
    expect(r.absentLockedSegments).toEqual([]);
  });

  it('FAILS when Luck of the Irish is moved after the cigar trip', () => {
    const cut = goodCut();
    // swap the gag and the trip — the exact mistake the creator keeps correcting
    cut.find((s) => s.id === 's5')!.proposedOrder = 5;
    cut.find((s) => s.id === 's6')!.proposedOrder = 4;

    const r = checkCanonCompliance(cut);
    expect(r.ok).toBe(false);
    expect(r.status).toBe('CANON_COMPLIANCE_FAILED');
    const v = r.violations.find((x) => x.constraintId === 'C10_NO_LOCKED_SEGMENT_RELOCATED');
    expect(v).toBeDefined();
    expect(v!.found).toContain('Cigars');
    expect(v!.constraint).toContain('Luck of the Irish');
  });

  it('FAILS when the cold open is not first', () => {
    const cut = goodCut();
    cut.find((s) => s.id === 's1')!.proposedOrder = 99;
    const r = checkCanonCompliance(cut);
    expect(r.ok).toBe(false);
    expect(r.violations.some((v) => v.constraintId === 'C10_NO_LOCKED_SEGMENT_RELOCATED')).toBe(true);
  });

  it('does not repair the cut it rejects', () => {
    const cut = goodCut();
    cut.find((s) => s.id === 's5')!.proposedOrder = 5;
    cut.find((s) => s.id === 's6')!.proposedOrder = 4;
    const before = cut.map((s) => `${s.id}@${s.proposedOrder}`).join(',');
    checkCanonCompliance(cut);
    expect(cut.map((s) => `${s.id}@${s.proposedOrder}`).join(',')).toBe(before);
  });

  it('FAILS a reorder that leaves no trace of being a reorder', () => {
    const cut = goodCut();
    cut.find((s) => s.id === 's8')!.physicalOrder = 2; // shot early, cut late, unexplained
    const r = checkCanonCompliance(cut);
    const v = r.violations.find((x) => x.constraintId === 'C11_REORDER_MUST_BE_VISIBLE');
    expect(v).toBeDefined();
    expect(v!.found).toContain('Joe');
  });

  it('accepts the same reorder once the reason is recorded', () => {
    const cut = goodCut();
    const joe = cut.find((s) => s.id === 's8')!;
    joe.physicalOrder = 2;
    joe.reorderReason = 'editorial order is not shooting order; Joe pays off the bag sequence';
    expect(checkCanonCompliance(cut).ok).toBe(true);
  });

  it('reports a partial cut as advisory, not as a failure', () => {
    const r = checkCanonCompliance([scene('s1', 'Motel', 0), scene('s2', 'Cigars / The Walk', 1)]);
    expect(r.ok).toBe(true);
    const a = r.advisories.find((x) => x.constraintId === 'A12_LOCKED_SEGMENT_ABSENT');
    expect(a).toBeDefined();
    expect(a!.found).toContain('Cold Open');
  });

  it('says so rather than guessing when a scene does not name a canon segment', () => {
    const r = checkCanonCompliance([scene('s1', 'Some unlabelled material', 0)]);
    expect(r.mappings[0].method).toBe('UNMATCHED');
    expect(r.mappings[0].canonSegmentId).toBeUndefined();
    expect(r.advisories.some((a) => a.constraintId === 'A13_SCENE_NOT_TIED_TO_CANON')).toBe(true);
  });
});

describe('canon mapping', () => {
  it('prefers a creator pin over any inference', () => {
    const m = resolveCanonSegment(scene('x', 'Motel', 0, {
      canonSegmentId: 'EP01_COLD_OPEN', storyBeatIds: ['walk.motel_chilling'],
    }));
    expect(m.canonSegmentId).toBe('EP01_COLD_OPEN');
    expect(m.method).toBe('EXPLICIT_ID');
  });

  it('maps a story beat to its canon segment and records which beat', () => {
    const m = resolveCanonSegment(scene('x', 'Untitled', 0, { storyBeatIds: ['joe.tic_tacs'] }));
    expect(m.canonSegmentId).toBe('EP01_JOE');
    expect(m.method).toBe('STORY_BEAT');
    expect(m.matchedOn).toBe('joe.tic_tacs');
  });

  it('does not let "Shumafied" swallow the Shumafied disappointment', () => {
    expect(resolveCanonSegment(scene('x', 'Shumafied Disappointment + Cigar Setup', 0)).canonSegmentId)
      .toBe('EP01_SHUMAFIED_LETDOWN');
    expect(resolveCanonSegment(scene('y', 'Shumafied', 0)).canonSegmentId).toBe('EP01_SHUMAFIED');
  });
});

describe('failure summary', () => {
  it('names the constraint, what was found, and what to do', () => {
    const cut = goodCut();
    cut.find((s) => s.id === 's5')!.proposedOrder = 5;
    cut.find((s) => s.id === 's6')!.proposedOrder = 4;
    const line = summariseCanonFailure(checkCanonCompliance(cut));
    expect(line).toContain('CANON_COMPLIANCE_FAILED');
    expect(line).toContain('C10_NO_LOCKED_SEGMENT_RELOCATED');
    expect(line).toContain('Fix:');
  });

  it('every locked segment is reachable by the mapper', () => {
    // A locked segment nothing can ever map to would make the gate blind to it.
    const titles: Record<string, string> = {
      EP01_COLD_OPEN: 'Cold Open', EP01_MOTEL: 'Motel', EP01_SHUMAFIED: 'Shumafied',
      EP01_SHUMAFIED_LETDOWN: 'Shumafied Disappointment + Cigar Setup',
      EP01_LUCK_OF_THE_IRISH: 'Luck of the Irish', EP01_CIGARS: 'Cigars / The Walk',
      EP01_BAG_SEQUENCE: 'Bag Sequence', EP01_JOE: 'Joe', EP01_TV: 'TV',
      EP01_CLOTHED_AND_CONFUSED: 'Clothed and Confused', EP01_SMOKING: 'Smoking / Hanging Out',
    };
    for (const id of EP01_LOCKED_ORDER) {
      const title = titles[id];
      expect(title, `no title fixture for ${id}`).toBeDefined();
      const m = resolveCanonSegment(scene('t', title, 0, { canonSegmentId: id === 'EP01_TV' ? id : undefined }));
      expect(m.canonSegmentId, `"${title}" did not map to ${id}`).toBe(id);
    }
  });
});
