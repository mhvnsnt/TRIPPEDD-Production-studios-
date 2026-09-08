export type ProgramUnitType =
  | 'EPISODE'
  | 'SEGMENT'
  | 'BUMP'
  | 'INTERSTITIAL'
  | 'NETWORK_ID'
  | 'FAKE_COMMERCIAL'
  | 'PROMO'
  | 'VIEWER_CARD'
  | 'COLD_OPEN'
  | 'TAG'
  | 'SHORT';

export type ProgramPlacement =
  | 'PRE_SHOW'
  | 'IN_SHOW'
  | 'POST_SHOW'
  | 'BETWEEN_SEGMENTS'
  | 'BETWEEN_EPISODES'
  | 'SOCIAL'
  | 'WEB'
  | 'UNKNOWN';

export interface ProgramUnit {
  id: string;
  type: ProgramUnitType;
  title: string;
  durationSeconds?: number;
  placement: ProgramPlacement;
  seriesId?: string;
  episodeId?: string;
  assetIds: string[];
  tags: string[];
  recurringKey?: string;
  provenance?: string;
  editorialPurpose?: string;
}

export interface ProgramSlot {
  id: string;
  order: number;
  unitId: string;
  required: boolean;
  allowMachineSubstitution: boolean;
  notes?: string;
}

export interface ProgramClock {
  programId: string;
  units: ProgramUnit[];
  slots: ProgramSlot[];
  targetDurationSeconds?: number;
  rules: {
    preserveHumanEditorialAuthority: boolean;
    generatedUnitsRequireProvenance: boolean;
    physicalSourceUnitsCannotBeRewrittenAsGenerated: boolean;
  };
}

/**
 * A lightweight programming layer for TRIPPEDD.
 *
 * The studio is not only an episode renderer. It can create a program clock
 * containing episodes, recurring segments, fake commercials, bumps, IDs,
 * promos, viewer cards, tags and short-form units. This keeps interstitial
 * programming separate from physical-source chronology and lets future
 * schedulers assemble channel-like experiences without changing episode truth.
 */
export function createProgramClock(programId: string, units: ProgramUnit[]): ProgramClock {
  return {
    programId,
    units,
    slots: units.map((unit, order) => ({
      id: `${programId}:slot:${order + 1}`,
      order,
      unitId: unit.id,
      required: unit.type === 'EPISODE',
      allowMachineSubstitution: unit.type !== 'EPISODE',
    })),
    rules: {
      preserveHumanEditorialAuthority: true,
      generatedUnitsRequireProvenance: true,
      physicalSourceUnitsCannotBeRewrittenAsGenerated: true,
    },
  };
}
