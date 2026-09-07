/**
 * EPISODE 1 — "THE WALK"  ·  CANONICAL EDITORIAL BLUEPRINT
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * THIS FILE OUTRANKS THE EDITOR.
 *
 * The autonomous editor may choose coverage, cut points, pacing, transitions
 * and treatment DETAIL. It may not reorder anything marked LOCKED_CANON, and it
 * may not fill an UNSPECIFIED field with its own invention and then treat that
 * as the creator's intent.
 *
 * Physical chronology of the footage does NOT determine episode order. The order
 * below does.
 *
 * ── HOW TO READ THE STATUS FIELD ──────────────────────────────────────────
 *   LOCKED_CANON  the creator established this. Immutable unless they change it.
 *   UNSPECIFIED   not yet decided. The editor may PROPOSE, never assume.
 *   AI_DERIVED    a decision the editor made inside the canon.
 *   AI_PROPOSAL   a new idea awaiting approval. Never silently promoted.
 *   USER_OVERRIDE a later creator change; supersedes, and versions the old value.
 *
 * ── PRODUCTION METHOD IS NOT ONE BUCKET ───────────────────────────────────
 * "Animated", "3D" and "AI" are different claims and must not be collapsed:
 *   LIVE_ACTION             captured on camera
 *   AI_ASSISTED_PRODUCTION  made with real open-source tools (Blender, FFmpeg,
 *                           compositing, procedural work) where AI helps write
 *                           the code / direct the process. The asset is produced
 *                           BY THE TOOLCHAIN. This is NOT "AI-generated".
 *   GENERATIVE_AI           text/image/video/audio generation used deliberately
 *   HYBRID                  a genuine mix, stated per segment
 */

export type CanonStatus =
  | 'LOCKED_CANON' | 'UNSPECIFIED' | 'AI_DERIVED' | 'AI_PROPOSAL' | 'USER_OVERRIDE';

export type ProductionMethod =
  | 'LIVE_ACTION' | 'AI_ASSISTED_PRODUCTION' | 'GENERATIVE_AI' | 'HYBRID';

export interface SegmentTreatment {
  /** How it is made. Never inferred from the fact that it is animated. */
  method: ProductionMethod;
  methodStatus: CanonStatus;
  /** The visual language, in the creator's own terms. */
  visualTreatment: string;
  visualTreatmentStatus: CanonStatus;
  /** Where the content comes from: real event, fiction, reconstruction. */
  sourceReality: 'REAL_EVENT' | 'FICTIONAL' | 'REAL_EVENT_NO_FOOTAGE';
  /** Whether footage of it exists at all. */
  footageExists: boolean;
  /** What the dialogue/action is based on. */
  dialogueSource: string;
  referenceLanguage?: string;
}

export interface CanonSegment {
  position: number;
  id: string;
  name: string;
  /** LOCKED_CANON here means: do not move this. */
  positionStatus: CanonStatus;
  /** Why it sits exactly here. The comedic/structural reason. */
  placementReason: string;
  treatment: SegmentTreatment;
  /** Shot construction where the creator specified one. */
  shots?: { id: string; description: string; status: CanonStatus }[];
  /** What the editor still needs from the creator before building this. */
  openQuestions: string[];
  /** Cross-references into src/core/pipeline/episodes.ts where they exist. */
  existingSegmentId?: string;
}

const UNKNOWN_STYLE =
  'NOT RECORDED IN THE REPO — the creator specified this verbally; ask before building.';

/**
 * THE LOCKED ORDER.
 *
 * Stated by the creator, verbatim in intent: cold open, motel, Shumafied, then
 * the Shumafied disappointment and the cigar discussion, THEN the Luck of the
 * Irish commercial, and only then the actual trip to get cigars.
 */
export const EPISODE_01: CanonSegment[] = [
  {
    position: 1, id: 'EP01_COLD_OPEN', name: 'Cold Open',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'Opens the episode.',
    treatment: {
      method: 'LIVE_ACTION', methodStatus: 'UNSPECIFIED',
      visualTreatment: UNKNOWN_STYLE, visualTreatmentStatus: 'UNSPECIFIED',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: ['Which footage is the cold open? Is it a real moment or a constructed teaser?'],
  },
  {
    position: 2, id: 'EP01_MOTEL', name: 'Motel',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'Establishes the location and the day.',
    treatment: {
      method: 'LIVE_ACTION', methodStatus: 'LOCKED_CANON',
      visualTreatment: 'Real captured motel material.', visualTreatmentStatus: 'AI_DERIVED',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: [],
    existingSegmentId: 'SEG01',
  },
  {
    position: 3, id: 'EP01_SHUMAFIED', name: 'Shumafied',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'The Shumafied pack/device bit, at the motel.',
    treatment: {
      method: 'LIVE_ACTION', methodStatus: 'UNSPECIFIED',
      visualTreatment: UNKNOWN_STYLE, visualTreatmentStatus: 'UNSPECIFIED',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: ['Does Shumafied have a generated/animated component, or is it purely live action?'],
  },
  {
    position: 4, id: 'EP01_SHUMAFIED_LETDOWN', name: 'Shumafied Disappointment + Cigar Setup',
    positionStatus: 'LOCKED_CANON',
    placementReason:
      'The beat where the Shumafied thing is not working ("this is not doing shit"), leading into ' +
      'the conversation about going to get cigars. This is the SETUP that Luck of the Irish pays off.',
    treatment: {
      method: 'LIVE_ACTION', methodStatus: 'LOCKED_CANON',
      visualTreatment: 'Real captured conversation.', visualTreatmentStatus: 'AI_DERIVED',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: [],
  },
  {
    position: 5, id: 'EP01_LUCK_OF_THE_IRISH', name: 'Luck of the Irish',
    positionStatus: 'LOCKED_CANON',
    placementReason:
      'LOCKED between the Shumafied disappointment/cigar setup and the actual cigar trip. ' +
      'It is a comedic escalation off the disappointment, not a floating interstitial the ' +
      'editor may relocate. Later episodes may place this gag family freely; EP01 may not.',
    treatment: {
      method: 'HYBRID', methodStatus: 'LOCKED_CANON',
      visualTreatment:
        'Live-action suspense build, then a fourth-wall break into a generative handoff. ' +
        'Plays as a fake commercial interrupting the episode.',
      visualTreatmentStatus: 'LOCKED_CANON',
      sourceReality: 'FICTIONAL', footageExists: true,
      dialogueSource: 'scripted gag; the "LUCK OF THE IRISH!!!" break is the hinge',
    },
    shots: [
      { id: 'SHOT_A', description: 'Far away, slow zoom in, suspense-building, chilling.', status: 'LOCKED_CANON' },
      { id: 'SHOT_B', description: 'Different angle, closer, up near the subject, suspense-building.', status: 'LOCKED_CANON' },
      { id: 'SHOT_C', description: 'Back to wide. Fourth-wall break "LUCK OF THE IRISH!!!". Generative handoff.', status: 'LOCKED_CANON' },
    ],
    openQuestions: [
      'What does the generated portion after the handoff actually look like? Style is not recorded.',
      'The creator has mentioned MORE Luck of the Irish gags than this one — those are not recorded here.',
    ],
    existingSegmentId: 'SEG04',
  },
  {
    position: 6, id: 'EP01_CIGARS', name: 'Cigars / The Walk',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'The actual trip to get cigars, AFTER the Luck of the Irish commercial.',
    treatment: {
      method: 'LIVE_ACTION', methodStatus: 'LOCKED_CANON',
      visualTreatment: 'Real captured walk.', visualTreatmentStatus: 'AI_DERIVED',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: [],
  },
  {
    position: 7, id: 'EP01_BAG_SEQUENCE', name: 'Bag Sequence',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'The bag interruption/return argument.',
    treatment: {
      method: 'LIVE_ACTION', methodStatus: 'LOCKED_CANON',
      visualTreatment: 'Real captured interaction.', visualTreatmentStatus: 'AI_DERIVED',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: [],
  },
  {
    position: 8, id: 'EP01_JOE', name: 'Joe',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'The Joe encounter.',
    treatment: {
      // The creator was explicit: this is a 2D reconstruction, NOT generic
      // "AI-generated scene" and NOT live-action reconstruction.
      method: 'HYBRID', methodStatus: 'LOCKED_CANON',
      visualTreatment:
        '2D reconstruction. The event genuinely happened but was NOT captured on video, so it is ' +
        'depicted in the specific 2D treatment established for Joe. The audience should understand ' +
        'they are seeing a reconstruction, not recovered footage. ' +
        'THE EXACT 2D STYLE IS NOT RECORDED IN THIS REPO — ask the creator before building.',
      visualTreatmentStatus: 'LOCKED_CANON',
      sourceReality: 'REAL_EVENT_NO_FOOTAGE', footageExists: false,
      dialogueSource:
        'derived from the documented/recalled real event and from Tyneshia performance timing. ' +
        'NOT invented, and NOT presented as if it were recovered footage.',
    },
    openQuestions: [
      'The exact 2D visual style for Joe is not encoded here. The creator specified it verbally.',
      'Which real captured material supplies the performance timing?',
    ],
    existingSegmentId: 'SEG02',
  },
  {
    position: 9, id: 'EP01_TV', name: 'TV',
    positionStatus: 'LOCKED_CANON',
    placementReason:
      'Tyneshia enters, sits down, lands on the Nickelodeon/Harry Potter material, reacts, ' +
      'changes the channel, and hits the survival-show material — which is what launches ' +
      'Clothed and Confused.',
    treatment: {
      method: 'HYBRID', methodStatus: 'UNSPECIFIED',
      visualTreatment:
        'Live-action TV watching, with on-screen television content that escalates. ' +
        'Harry Potter here is universe setup for later parody material. ' +
        'McBrain Feed is a SEPARATE future television segment and must not be merged into ' +
        'Clothed and Confused.',
      visualTreatmentStatus: 'LOCKED_CANON',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: ['How is the on-screen TV content produced — composited, generated, or animated?'],
  },
  {
    position: 10, id: 'EP01_CLOTHED_AND_CONFUSED', name: 'Clothed and Confused',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'Escalates directly out of the TV channel change.',
    treatment: {
      // Explicitly NOT 2D and NOT 3D. The comedy depends on it looking real.
      method: 'GENERATIVE_AI', methodStatus: 'LOCKED_CANON',
      visualTreatment:
        'REALISTIC survival-documentary look, deliberately resembling the visual language of ' +
        'Naked and Afraid. Realistic generated people, realistic environments, ' +
        'survival-documentary cinematography, documentary narration, serious survival graphics, ' +
        'censored/blurred nudity treatment, dramatic survival music, authentic-looking wilderness. ' +
        'The comedy is that it looks like a SERIOUS survival show while the behaviour is absurd, ' +
        'played completely straight. ' +
        'IT IS NOT 2D. IT IS NOT A BLENDER-LOOKING 3D CARTOON. ' +
        'Original characters, dialogue, locations, footage and graphics — not actual ' +
        'Naked and Afraid material.',
      visualTreatmentStatus: 'LOCKED_CANON',
      sourceReality: 'FICTIONAL', footageExists: false,
      dialogueSource: 'original fictional script, played straight as documentary',
      referenceLanguage: 'Naked and Afraid (visual language only; nothing lifted)',
    },
    openQuestions: ['Which generation pipeline produces the realistic footage?'],
  },
  {
    position: 11, id: 'EP01_SMOKING', name: 'Smoking / Hanging Out',
    positionStatus: 'LOCKED_CANON',
    placementReason: 'Closes the episode.',
    treatment: {
      method: 'LIVE_ACTION', methodStatus: 'LOCKED_CANON',
      visualTreatment: 'Real captured material.', visualTreatmentStatus: 'AI_DERIVED',
      sourceReality: 'REAL_EVENT', footageExists: true,
      dialogueSource: 'captured on camera',
    },
    openQuestions: ['Is there a tag/button after this?'],
  },
];

/**
 * Recurring material that exists in the show's vocabulary and appears in EP01,
 * but whose exact placement the creator has not locked. The editor may PROPOSE
 * positions for these; it may not assume them.
 */
export const EP01_UNPLACED_CANON = [
  {
    id: 'GOODVILLE',
    name: 'Goodville',
    note:
      'A recurring GAG FAMILY, not a single insert. The repo records two: Goodville Geography ' +
      '(a documentary gag built on real interview material, the "45 minutes away" bit) and ' +
      'Goodville Cartoon (an animated cutaway set in Goodville TN). The creator has said there ' +
      'are MORE Goodville gags than these two. They are not recorded here.',
    knownMembers: ['Goodville Geography (SEG03, DOCUMENTARY_GAG)', 'Goodville Cartoon (SEG05, animated cutaway)'],
    status: 'UNSPECIFIED' as CanonStatus,
    openQuestions: ['What are the other Goodville gags, and where do they sit in EP01?'],
  },
  {
    id: 'INTERSTITIALS',
    name: 'Mundane → surreal transitions',
    note:
      'The show deliberately derails: mundane reality mutating into trippy, liminal, psychedelic ' +
      'or genre-jumping material and snapping back. Anthology rhythm in the Mad TV / Robot Chicken ' +
      'sense, mixed with the show\'s own reference vocabulary. These transitions are part of the ' +
      'episode, not decoration.',
    status: 'UNSPECIFIED' as CanonStatus,
    openQuestions: [
      'The full reference-show list and the specific transition treatments are NOT in this repo.',
      'Which transitions are locked to specific junctions in EP01?',
    ],
  },
];

/** Order-only view, for the editor to obey. */
export const EP01_LOCKED_ORDER = EPISODE_01
  .filter((s) => s.positionStatus === 'LOCKED_CANON')
  .sort((a, b) => a.position - b.position)
  .map((s) => s.id);

/** Everything the editor must ask about instead of inventing. */
export function openCreativeQuestions(): { segment: string; question: string }[] {
  const out: { segment: string; question: string }[] = [];
  for (const s of EPISODE_01) for (const q of s.openQuestions) out.push({ segment: s.name, question: q });
  for (const u of EP01_UNPLACED_CANON) for (const q of u.openQuestions) out.push({ segment: u.name, question: q });
  return out;
}

/** True when moving `id` would break locked canon. */
export function isPositionLocked(id: string): boolean {
  return EPISODE_01.some((s) => s.id === id && s.positionStatus === 'LOCKED_CANON');
}
