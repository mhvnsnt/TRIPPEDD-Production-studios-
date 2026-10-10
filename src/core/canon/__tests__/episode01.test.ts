import { describe, it, expect } from 'vitest';
import {
  EPISODE_01, EP01_LOCKED_ORDER, EP01_UNPLACED_CANON,
  openCreativeQuestions, isPositionLocked,
} from '../episode01';

describe('Episode 1 canon — the order the creator set', () => {
  it('holds the exact locked sequence', () => {
    expect(EP01_LOCKED_ORDER).toEqual([
      'EP01_COLD_OPEN',
      'EP01_MOTEL',
      'EP01_SHUMAFIED',
      'EP01_SHUMAFIED_LETDOWN',
      'EP01_LUCK_OF_THE_IRISH',
      'EP01_CIGARS',
      'EP01_BAG_SEQUENCE',
      'EP01_JOE',
      'EP01_TV',
      'EP01_CLOTHED_AND_CONFUSED',
      'EP01_SMOKING',
    ]);
  });

  it('puts Luck of the Irish AFTER the Shumafied letdown and BEFORE the cigar trip', () => {
    const i = (id: string) => EP01_LOCKED_ORDER.indexOf(id);
    // This is the placement the creator corrected twice. It is the whole point
    // of the file: the gag pays off the disappointment, then they go.
    expect(i('EP01_SHUMAFIED_LETDOWN')).toBeLessThan(i('EP01_LUCK_OF_THE_IRISH'));
    expect(i('EP01_LUCK_OF_THE_IRISH')).toBeLessThan(i('EP01_CIGARS'));
  });

  it('runs Clothed and Confused straight out of the TV beat', () => {
    const i = (id: string) => EP01_LOCKED_ORDER.indexOf(id);
    expect(i('EP01_CLOTHED_AND_CONFUSED')).toBe(i('EP01_TV') + 1);
  });

  it('marks every position locked, so nothing may be quietly reordered', () => {
    for (const id of EP01_LOCKED_ORDER) expect(isPositionLocked(id)).toBe(true);
    expect(isPositionLocked('SOMETHING_THE_EDITOR_INVENTED')).toBe(false);
  });
});

describe('Episode 1 canon — production method is never collapsed', () => {
  it('Joe is a 2D reconstruction of a real event with no footage', () => {
    const joe = EPISODE_01.find((s) => s.id === 'EP01_JOE')!;
    expect(joe.treatment.sourceReality).toBe('REAL_EVENT_NO_FOOTAGE');
    expect(joe.treatment.footageExists).toBe(false);
    expect(joe.treatment.visualTreatment).toMatch(/2D reconstruction/i);
    // It must not be describable as recovered footage.
    expect(joe.treatment.dialogueSource).toMatch(/NOT presented as if it were recovered footage/i);
    expect(joe.treatment.visualTreatmentStatus).toBe('LOCKED_CANON');
  });

  it('Clothed and Confused is realistic — explicitly not 2D and not 3D', () => {
    const cc = EPISODE_01.find((s) => s.id === 'EP01_CLOTHED_AND_CONFUSED')!;
    expect(cc.treatment.visualTreatment).toMatch(/REALISTIC survival-documentary/i);
    expect(cc.treatment.visualTreatment).toMatch(/IT IS NOT 2D/);
    expect(cc.treatment.visualTreatment).toMatch(/NOT A BLENDER-LOOKING 3D CARTOON/);
    expect(cc.treatment.referenceLanguage).toMatch(/Naked and Afraid/);
    // Original material, not lifted.
    expect(cc.treatment.visualTreatment).toMatch(/not actual\s+Naked and Afraid material/i);
  });

  it('keeps Joe and Clothed and Confused as different productions', () => {
    const joe = EPISODE_01.find((s) => s.id === 'EP01_JOE')!;
    const cc = EPISODE_01.find((s) => s.id === 'EP01_CLOTHED_AND_CONFUSED')!;
    // Both involve AI; they are not the same kind of thing.
    expect(joe.treatment.visualTreatment).not.toBe(cc.treatment.visualTreatment);
    expect(joe.treatment.sourceReality).not.toBe(cc.treatment.sourceReality);
  });

  it('separates Harry Potter setup from McBrain Feed', () => {
    const tv = EPISODE_01.find((s) => s.id === 'EP01_TV')!;
    expect(tv.treatment.visualTreatment).toMatch(/McBrain Feed is a SEPARATE future television segment/);
  });

  it('records Luck of the Irish as three specific shots into a generative handoff', () => {
    const loti = EPISODE_01.find((s) => s.id === 'EP01_LUCK_OF_THE_IRISH')!;
    expect(loti.shots).toHaveLength(3);
    expect(loti.shots!.every((s) => s.status === 'LOCKED_CANON')).toBe(true);
    expect(loti.shots![2].description).toMatch(/Fourth-wall break/i);
    expect(loti.shots![2].description).toMatch(/Generative handoff/i);
  });
});

describe('Episode 1 canon — what is NOT known is admitted', () => {
  it('flags the unrecorded creative detail instead of inventing it', () => {
    const qs = openCreativeQuestions();
    const text = qs.map((q) => q.question).join(' | ');
    // The specific things the creator said are missing.
    expect(text).toMatch(/2D visual style for Joe is not encoded/i);
    expect(text).toMatch(/other Goodville gags/i);
    expect(text).toMatch(/reference-show list/i);
    expect(qs.length).toBeGreaterThan(5);
  });

  it('treats Goodville as a gag family with more members than are recorded', () => {
    const g = EP01_UNPLACED_CANON.find((u) => u.id === 'GOODVILLE')!;
    expect(g.note).toMatch(/GAG FAMILY, not a single insert/);
    expect(g.knownMembers.length).toBeGreaterThanOrEqual(2);
    expect(g.status).toBe('UNSPECIFIED');
  });

  it('never marks an unrecorded style as locked', () => {
    for (const s of EPISODE_01) {
      if (/NOT RECORDED IN THE REPO/.test(s.treatment.visualTreatment)) {
        // An unknown style must not masquerade as an established decision.
        expect(s.treatment.visualTreatmentStatus).toBe('UNSPECIFIED');
      }
    }
  });
});
