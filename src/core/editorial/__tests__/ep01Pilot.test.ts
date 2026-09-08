import { describe, expect, it } from 'vitest';
import { createEp01AssemblyPlan } from '../ep01Assembly';
import { createEp01PilotPlan } from '../ep01Pilot';
import { EP01_LOST_ACID_SUBJECTIVITY } from '../subjectivityRule';

describe('TRIPPEDD EP01 pilot production grammar', () => {
  it('keeps the lost-acid beat terminal', () => {
    const plan = createEp01PilotPlan();
    expect(plan.terminalBeatId).toBe('lost-acid-button');
    expect(plan.beats.at(-1)?.id).toBe('lost-acid-button');
    expect(plan.neverDo).toContain('Do not explain or solve the disappearance of the acid.');
  });

  it('requires approval for synthetic subjective material', () => {
    const plan = createEp01PilotPlan();
    const shift = plan.beats.find(beat => beat.id === 'shumafied-subjective-shift');
    expect(shift?.generatedMaterialAllowed).toBe(true);
    expect(shift?.humanApprovalRequired).toBe(true);
  });

  it('keeps source chronology separate from editorial order', () => {
    const assembly = createEp01AssemblyPlan();
    expect(assembly.items.find(item => item.beatId === 'cigar-run')?.sourceLabels).toEqual([
      'DECISION_TO_GET_CIGARS',
      'WALK_TO_GET_CIGARS',
    ]);
    expect(assembly.items.find(item => item.beatId === 'shumafied-subjective-shift')?.kind).toBe('GENERATED');
  });

  it('uses the canonical subjective mode progression', () => {
    expect(EP01_LOST_ACID_SUBJECTIVITY.modes).toEqual([
      'LIVE_ACTION',
      'VISUAL_DISTORTION',
      'ANIMATION',
      'THREE_D',
      'BLENDER_CG',
      'IMPOSSIBLE_WORLD',
      'LIVE_ACTION_RETURN',
    ]);
    expect(EP01_LOST_ACID_SUBJECTIVITY.characterAcknowledges).toBe(false);
  });
});
