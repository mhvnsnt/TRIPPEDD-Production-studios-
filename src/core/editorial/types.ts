/**
 * Editorial layer types.
 *
 * The hard rule this layer exists to hold: what the creator REMEMBERS wanting
 * is not the same kind of thing as what the camera actually RECORDED. Those are
 * kept in separate fields with separate provenance, and nothing promotes one
 * into the other.
 */

/** Where a claim comes from. Never silently converted between kinds. */
export type EvidenceClass =
  | 'OBSERVED_FACT'        // present in source media
  | 'HUMAN_DIRECTION'      // the creator explicitly asked for it
  | 'REFERENCE'            // an artistic/structural influence
  | 'EDITORIAL_INFERENCE'  // a machine proposal
  | 'GENERATED_MEDIA';     // a separately generated asset that actually exists

/** How firmly the creator named a beat when describing the material. */
export type MentionStrength = 'EXPLICIT' | 'PARTIAL';

/** Result of matching remembered material against actual ingested evidence. */
export type ReconciliationState =
  | 'FOUND'
  | 'PARTIALLY_FOUND'
  | 'NOT_FOUND'
  | 'AMBIGUOUS_MATCH'
  | 'MISSING_SOURCE_MEDIA';

/** Editorial treatment of a stretch of real source material. */
export type EditorialClassification =
  | 'PROGRAM_CONTENT'
  | 'PRODUCTION_ARTIFACT'
  | 'CAMERA_DIRECTION'
  | 'SETUP'
  | 'RESET'
  | 'DEAD_AIR'
  | 'TECHNICAL_INTERRUPTION'
  | 'OUTTAKE'
  | 'UNCERTAIN';

/** Confidence in a chronology relationship. Mirrors the existing vocabulary. */
export type ChronologyConfidence =
  | 'CONFIRMED' | 'SUPPORTED' | 'PROVISIONAL'
  | 'POSSIBLE' | 'UNRESOLVED' | 'CONTRADICTED';

export type SceneReviewState =
  | 'PROPOSED' | 'UNDER_REVIEW' | 'REVISION_REQUESTED'
  | 'REVISED' | 'APPROVED' | 'LOCKED' | 'REJECTED';

/** A beat the creator described, before any footage is consulted. */
export interface StoryBeat {
  id: string;
  title: string;
  /** The creator's own description. Never treated as an observation. */
  description: string;
  mentionStrength: MentionStrength;
  /** Grouping, e.g. 'WALK' or 'JOE'. */
  thread: string;
  /** Cues used to look for this beat in real evidence. */
  cues: {
    dialogue?: string[];
    onScreenText?: string[];
    entities?: string[];
  };
  evidenceClass: 'HUMAN_DIRECTION';
}

/** One piece of real evidence supporting a match. */
export interface MatchEvidence {
  observationId: string;
  sourceFileId: string;
  type: string;
  startTime?: number;
  endTime?: number;
  excerpt?: string;
  /** Which cue fired, so a human can judge the match rather than trust a score. */
  matchedCue: string;
  tool: string;
}

export interface ReconciledBeat {
  beatId: string;
  title: string;
  mentionStrength: MentionStrength;
  state: ReconciliationState;
  /** 0..1, derived from evidence found. A beat with no evidence scores 0. */
  confidence: number;
  evidence: MatchEvidence[];
  /** Candidate source files, most-supported first. */
  candidateSourceFileIds: string[];
  /** Why the engine landed on this state, in plain words. */
  rationale: string;
  /** Cues that found nothing, so the gap is visible rather than implied. */
  unmatchedCues: string[];
}

/** A real range of real media. Timecodes always come from actual observations. */
export interface SourceRange {
  sourceFileId: string;
  startTime: number;
  endTime: number;
  /** Observations that justify this exact range. */
  derivedFromObservationIds: string[];
}

export interface EditorialExclusion {
  range: SourceRange;
  classification: EditorialClassification;
  reason: string;
  /** Source evidence is preserved; this only removes it from the cut. */
  preservedInPhysicalTimeline: true;
  excerpt?: string;
}

export interface BeatMapEntry {
  role: 'OPENING' | 'ESCALATION' | 'PAYOFF' | 'EXIT';
  range: SourceRange;
  rationale: string;
}

/**
 * What a candidate actually is. A short fragment is a beat or an insert; it
 * should not be handed to the creator as a finished scene.
 */
export type CandidateKind = 'SCENE' | 'BEAT' | 'INSERT' | 'INSUFFICIENT_COVERAGE';

export interface EditorialSceneCandidate {
  id: string;
  kind: CandidateKind;
  /** Why it is (or is not) a scene, in the creator's language. */
  kindReason: string;
  /** 0..1 — duration, continuity, evidence strength, dead air, chatter. */
  qualityScore: number;
  productionUnitId: string;
  proposedTitle: string;
  purpose: string;

  /** Provenance back to real evidence. */
  sourceEvidenceIds: string[];
  sourceClipIds: string[];
  transcriptSegmentIds: string[];
  visualObservationIds: string[];
  referenceIds: string[];
  storyBeatIds: string[];

  /** Editorial position, which may deliberately differ from physical order. */
  proposedOrder: number;
  /** Physical position, retained so a reorder is always visible as a reorder. */
  physicalOrder: number;
  reorderReason?: string;

  /** The actual cut: real ranges of real media, in editorial order. */
  ranges: SourceRange[];
  proposedDuration: number;

  beatMap: BeatMapEntry[];
  excludedMaterial: EditorialExclusion[];

  confidence: number;
  editorialRationale: string;
  chronologyAssumptions: { statement: string; confidence: ChronologyConfidence }[];
  missingEvidence: string[];
  /**
   * Analyzers that would normally have contributed but could not run. A scene
   * assembled without word-level alignment is still usable — but the creator
   * must be able to see that before approving it.
   */
  evidenceLimitations: {
    tool: string;
    reason: string;
    effect: string;
  }[];
  requiredAssets: string[];
  generatedAssetIds: string[];

  humanReviewState: SceneReviewState;
  revisionHistory: SceneRevision[];
  timelineAssetId?: string;

  createdAt: string;
  updatedAt: string;
}

export interface SceneRevision {
  at: string;
  from: SceneReviewState;
  to: SceneReviewState;
  actor: 'MACHINE' | 'CREATOR';
  note?: string;
  /** Snapshot of the ranges at this point, so history is never rewritten. */
  rangesSnapshot?: SourceRange[];
}

/** What the creator's decisions taught us, for later proposals only. */
export interface EditorialFeedback {
  sceneId: string;
  at: string;
  decision: 'APPROVED' | 'REJECTED' | 'REVISION_REQUESTED';
  note?: string;
  signals: {
    keptRanges?: number;
    removedRanges?: number;
    durationDeltaSec?: number;
    preferredClassifications?: EditorialClassification[];
    rejectedReason?: string;
  };
}
