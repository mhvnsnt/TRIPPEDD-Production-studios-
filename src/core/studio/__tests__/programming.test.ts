import { describe, expect, it } from 'vitest';
import { createProgramClock, validateProgramClock, type ProgramUnit } from '../programming';

const episode: ProgramUnit = {
  id: 'ep01',
  type: 'EPISODE',
  title: 'The Walk',
  placement: 'IN_SHOW',
  episodeId: 'EP01',
  assetIds: ['ep01-cut'],
  tags: ['PHYSICAL_SOURCE'],
};

const bump: ProgramUnit = {
  id: 'bump-01',
  type: 'BUMP',
  title: 'Lost Signal',
  placement: 'BETWEEN_EPISODES',
  assetIds: ['bump-01-video'],
  tags: ['GENERATED'],
  provenance: 'TRIPPEDD_GENERATED_BUMP_V1',
  editorialPurpose: 'Give the program clock a short recurring identity fragment.',
};

describe('ProgramClock', () => {
  it('creates deterministic slots and validates a complete clock', () => {
    const clock = createProgramClock('trippedd-demo', [episode, bump]);
    expect(clock.slots.map(slot => slot.id)).toEqual(['trippedd-demo:slot:1', 'trippedd-demo:slot:2']);
    expect(validateProgramClock(clock)).toEqual([]);
  });

  it('rejects missing provenance and editorial purpose on non-episode units', () => {
    const broken: ProgramUnit = { ...bump, provenance: undefined, editorialPurpose: undefined };
    const clock = createProgramClock('trippedd-demo', [episode, broken]);
    const codes = validateProgramClock(clock).map(issue => issue.code);
    expect(codes).toContain('MISSING_PROVENANCE');
    expect(codes).toContain('MISSING_EDITORIAL_PURPOSE');
  });

  it('rejects a unit that simultaneously claims physical truth and generated status', () => {
    const broken: ProgramUnit = { ...bump, tags: ['PHYSICAL_SOURCE', 'GENERATED'] };
    const clock = createProgramClock('trippedd-demo', [episode, broken]);
    expect(validateProgramClock(clock).some(issue => issue.code === 'PHYSICAL_SOURCE_REWRITTEN')).toBe(true);
  });

  it('rejects slots that reference units not present in the clock', () => {
    const clock = createProgramClock('trippedd-demo', [episode]);
    clock.slots.push({ id: 'orphan', order: 1, unitId: 'missing', required: false, allowMachineSubstitution: true });
    expect(validateProgramClock(clock).some(issue => issue.code === 'MISSING_UNIT_REFERENCE')).toBe(true);
  });
});
