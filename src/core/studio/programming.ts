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

export interface ProgramClockIssue {
  code:
    | 'EMPTY_PROGRAM_ID'
    | 'EMPTY_UNITS'
    | 'DUPLICATE_UNIT_ID'
    | 'DUPLICATE_SLOT_ID'
    | 'MISSING_UNIT_REFERENCE'
    | 'INVALID_DURATION'
    | 'MISSING_PROVENANCE'
    | 'MISSING_EDITORIAL_PURPOSE'
    | 'PHYSICAL_SOURCE_REWRITTEN';
  message: string;
  unitId?: string;
}

const provenanceRequiredTypes = new Set<ProgramUnitType>([
  'BUMP',
  'INTERSTITIAL',
  'NETWORK_ID',
  'FAKE_COMMERCIAL',
  'PROMO',
  'VIEWER_CARD',
  'TAG',
  'SHORT',
]);

/**
 * Build a deterministic program clock. The clock is a programming layer and
 * must not mutate the physical-source timeline.
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

/**
 * Validate a program clock before it is scheduled or serialized. This turns
 * the programming model into an executable integrity boundary rather than a
 * passive collection of types.
 */
export function validateProgramClock(clock: ProgramClock): ProgramClockIssue[] {
  const issues: ProgramClockIssue[] = [];
  if (!clock.programId.trim()) issues.push({ code: 'EMPTY_PROGRAM_ID', message: 'Program clock requires a non-empty program id.' });
  if (!clock.units.length) issues.push({ code: 'EMPTY_UNITS', message: 'Program clock must contain at least one program unit.' });

  const unitIds = new Set<string>();
  for (const unit of clock.units) {
    if (unitIds.has(unit.id)) issues.push({ code: 'DUPLICATE_UNIT_ID', message: `Duplicate program unit id: ${unit.id}`, unitId: unit.id });
    unitIds.add(unit.id);

    if (unit.durationSeconds !== undefined && (!Number.isFinite(unit.durationSeconds) || unit.durationSeconds < 0)) {
      issues.push({ code: 'INVALID_DURATION', message: `Invalid duration for ${unit.id}.`, unitId: unit.id });
    }
    if (clock.rules.generatedUnitsRequireProvenance && provenanceRequiredTypes.has(unit.type) && !unit.provenance?.trim()) {
      issues.push({ code: 'MISSING_PROVENANCE', message: `${unit.type} unit ${unit.id} requires provenance.`, unitId: unit.id });
    }
    if (unit.type !== 'EPISODE' && !unit.editorialPurpose?.trim()) {
      issues.push({ code: 'MISSING_EDITORIAL_PURPOSE', message: `${unit.type} unit ${unit.id} requires an editorial purpose.`, unitId: unit.id });
    }
    const claimsPhysicalSource = unit.tags.some(tag => tag.toUpperCase() === 'PHYSICAL_SOURCE') || unit.tags.some(tag => tag.toUpperCase() === 'PHYSICAL_TRUTH');
    if (clock.rules.physicalSourceUnitsCannotBeRewrittenAsGenerated && claimsPhysicalSource && unit.tags.some(tag => tag.toUpperCase() === 'GENERATED')) {
      issues.push({ code: 'PHYSICAL_SOURCE_REWRITTEN', message: `Unit ${unit.id} cannot claim both physical-source truth and generated status.`, unitId: unit.id });
    }
  }

  const slotIds = new Set<string>();
  const referencedUnits = new Set<string>();
  for (const slot of clock.slots) {
    if (slotIds.has(slot.id)) issues.push({ code: 'DUPLICATE_SLOT_ID', message: `Duplicate program slot id: ${slot.id}` });
    slotIds.add(slot.id);
    referencedUnits.add(slot.unitId);
    if (!unitIds.has(slot.unitId)) issues.push({ code: 'MISSING_UNIT_REFERENCE', message: `Slot ${slot.id} references missing unit ${slot.unitId}.` });
  }

  for (const unit of clock.units) {
    if (!referencedUnits.has(unit.id)) issues.push({ code: 'MISSING_UNIT_REFERENCE', message: `Program unit ${unit.id} has no program slot.`, unitId: unit.id });
  }

  if (!clock.rules.preserveHumanEditorialAuthority) {
    issues.push({ code: 'MISSING_EDITORIAL_PURPOSE', message: 'Program clock must preserve human editorial authority.' });
  }
  return issues;
}
