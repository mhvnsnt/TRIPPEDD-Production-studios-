/**
 * CANON COMPLIANCE CHECK
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * The gate that stands between an assembled cut and a render.
 *
 * It answers one question: does this episode still obey what the creator
 * locked? If it does not, the render STOPS and the violated constraint is
 * named. Nothing here repairs anything. A checker that quietly reorders a cut
 * to make itself pass is how a locked decision gets lost without anyone seeing
 * it happen — the creator would watch a compliant-looking episode that is not
 * the one he asked for.
 *
 * Two kinds of thing get checked, because the canon can be broken from two
 * directions:
 *
 *   BLUEPRINT checks read src/core/canon/episode01.ts itself. They catch a
 *   co-developer (human or AI) editing the blueprint — reordering it,
 *   relabelling Joe as live footage, calling Clothed and Confused a cartoon.
 *   These run on every call, with or without an assembly.
 *
 *   ASSEMBLY checks read the cut the editor produced. They catch the editor
 *   putting the Luck of the Irish commercial in the wrong place, or collapsing
 *   editorial order into physical chronology.
 *
 * Severity is not decoration:
 *   BLOCKING  the render must not happen.
 *   ADVISORY  the creator must be able to see it; the render may proceed.
 * An incomplete cut (locked segments not yet built) is ADVISORY — reviewing a
 * partial episode is normal work, and refusing to render one would make the
 * gate useless during the very phase it matters.
 */
import {
  EPISODE_01, EP01_UNPLACED_CANON, lockedOrder, UNKNOWN_STYLE, CANON_DOC_PATH,
  type CanonSegment,
} from './episode01';

export type CanonSeverity = 'BLOCKING' | 'ADVISORY';

export interface CanonViolation {
  /** Stable id, so a failure can be talked about without quoting prose. */
  constraintId: string;
  /** The rule, in the creator's terms. */
  constraint: string;
  severity: CanonSeverity;
  /** What was actually found. Never a guess. */
  found: string;
  /** What has to change. The check will not do it. */
  requiredAction: string;
  /** BLUEPRINT = the canon file was edited. ASSEMBLY = the cut is wrong. */
  origin: 'BLUEPRINT' | 'ASSEMBLY';
}

/** How a scene in the cut was tied to a canon segment. Traceable on purpose. */
export type CanonMatchMethod = 'EXPLICIT_ID' | 'STORY_BEAT' | 'TITLE' | 'UNMATCHED';

export interface CanonMapping {
  sceneId: string;
  title: string;
  canonSegmentId?: string;
  method: CanonMatchMethod;
  /** Which beat id or phrase produced the match, so a human can overrule it. */
  matchedOn?: string;
}

export interface CanonComplianceReport {
  status: 'CANON_COMPLIANT' | 'CANON_COMPLIANCE_FAILED';
  ok: boolean;
  checkedAt: string;
  /** Number of constraints evaluated on this call. */
  constraintsChecked: number;
  violations: CanonViolation[];
  advisories: CanonViolation[];
  mappings: CanonMapping[];
  /** Locked segments with nothing in the cut yet. Advisory, but always shown. */
  absentLockedSegments: string[];
  canonDoc: string;
}

/** The shape the check needs from a scene. Kept minimal so tests can be honest. */
export interface AssemblyScene {
  id: string;
  proposedTitle: string;
  proposedOrder: number;
  physicalOrder: number;
  reorderReason?: string;
  storyBeatIds?: string[];
  /** Set by the creator or a pinning UI; wins over every inference. */
  canonSegmentId?: string;
}

/**
 * Story beats map to canon segments. A beat is evidence-side vocabulary and a
 * canon segment is episode-side vocabulary; they are different registers and
 * the bridge is written down rather than inferred from similar wording.
 */
const BEAT_TO_SEGMENT: Record<string, string> = {
  'walk.motel_chilling': 'EP01_MOTEL',
  'walk.motel_clerk': 'EP01_MOTEL',
  'walk.shumafied_pack': 'EP01_SHUMAFIED',
  'walk.shumafied_letdown': 'EP01_SHUMAFIED_LETDOWN',
  'walk.cigar_walk': 'EP01_CIGARS',
  'walk.cigar_trip': 'EP01_CIGARS',
  'walk.bag_interruption': 'EP01_BAG_SEQUENCE',
  'walk.bag_return_argument': 'EP01_BAG_SEQUENCE',
  'walk.joe_encounter': 'EP01_JOE',
  'joe.prayer': 'EP01_JOE',
  'joe.tic_tacs': 'EP01_JOE',
  'joe.names_intros': 'EP01_JOE',
  'joe.disappearing': 'EP01_JOE',
  'joe.bag_waiting': 'EP01_JOE',
  'walk.smoking_hanging': 'EP01_SMOKING',
};

/**
 * Title phrases, longest first so "shumafied disappointment" cannot be eaten by
 * "shumafied". Deliberately narrow: a title that does not clearly name a canon
 * segment is reported UNMATCHED rather than forced into one.
 */
const TITLE_PHRASES: [string, string][] = [
  ['shumafied disappointment', 'EP01_SHUMAFIED_LETDOWN'],
  ['clothed and confused', 'EP01_CLOTHED_AND_CONFUSED'],
  ['luck of the irish', 'EP01_LUCK_OF_THE_IRISH'],
  ['cigar setup', 'EP01_SHUMAFIED_LETDOWN'],
  ['bag sequence', 'EP01_BAG_SEQUENCE'],
  ['cold open', 'EP01_COLD_OPEN'],
  ['shumafied', 'EP01_SHUMAFIED'],
  ['smoking', 'EP01_SMOKING'],
  ['motel', 'EP01_MOTEL'],
  ['cigar', 'EP01_CIGARS'],
  ['joe', 'EP01_JOE'],
];

/** Ties one scene to a canon segment, recording HOW so a human can overrule it. */
export function resolveCanonSegment(scene: AssemblyScene): CanonMapping {
  const base = { sceneId: scene.id, title: scene.proposedTitle };

  if (scene.canonSegmentId) {
    return { ...base, canonSegmentId: scene.canonSegmentId, method: 'EXPLICIT_ID', matchedOn: 'pinned by the creator' };
  }

  for (const beatId of scene.storyBeatIds ?? []) {
    const seg = BEAT_TO_SEGMENT[beatId];
    if (seg) return { ...base, canonSegmentId: seg, method: 'STORY_BEAT', matchedOn: beatId };
  }

  const title = scene.proposedTitle.toLowerCase();
  for (const [phrase, seg] of TITLE_PHRASES) {
    if (title.includes(phrase)) return { ...base, canonSegmentId: seg, method: 'TITLE', matchedOn: phrase };
  }

  return { ...base, method: 'UNMATCHED' };
}

// Read live off the blueprint on every call. A cached copy would make the
// check blind to exactly the edit it is here to catch.
const canonPosition = (id: string): number | undefined => EPISODE_01.find((s) => s.id === id)?.position;
const canonName = (id: string): string | undefined => EPISODE_01.find((s) => s.id === id)?.name;
const seg = (id: string): CanonSegment | undefined => EPISODE_01.find((s) => s.id === id);

/** The order the creator stated, independent of the array's current shape. */
const CREATOR_STATED_ORDER = [
  'EP01_COLD_OPEN', 'EP01_MOTEL', 'EP01_SHUMAFIED', 'EP01_SHUMAFIED_LETDOWN',
  'EP01_LUCK_OF_THE_IRISH', 'EP01_CIGARS', 'EP01_BAG_SEQUENCE',
  'EP01_JOE', 'EP01_TV', 'EP01_CLOTHED_AND_CONFUSED', 'EP01_SMOKING',
];

/**
 * Every blueprint constraint this module evaluates. The count reported to the
 * creator is the length of this list, not a number typed in by hand — a
 * hand-typed count drifts the moment a check is added.
 */
export const BLUEPRINT_CONSTRAINT_IDS = [
  'C01_LOCKED_ORDER_INTACT',
  'C02_COLD_OPEN_FIRST',
  'C03_IRISH_BETWEEN_LETDOWN_AND_CIGARS',
  'C04_JOE_IS_RECONSTRUCTION',
  'C04_JOE_IS_2D',
  'C05_CLOTHED_AND_CONFUSED_REALISTIC',
  'C05_CLOTHED_AND_CONFUSED_NOT_2D_OR_3D',
  'C05_CLOTHED_AND_CONFUSED_CLASSIFIED_ANIMATED',
  'C06_MCBRAIN_FEED_SEPARATE',
  'C07_GOODVILLE_IS_A_GAG_FAMILY',
  'C08_UNRECORDED_STYLE_NEVER_LOCKED',
  'C09_METHOD_NOT_COLLAPSED',
] as const;

export const ASSEMBLY_CONSTRAINT_IDS = [
  'C10_NO_LOCKED_SEGMENT_RELOCATED',
  'C11_REORDER_MUST_BE_VISIBLE',
] as const;

function blueprintChecks(): { violations: CanonViolation[]; checked: number } {
  const v: CanonViolation[] = [];
  const order = lockedOrder();
  const B = (
    constraintId: string, constraint: string, found: string, requiredAction: string,
    severity: CanonSeverity = 'BLOCKING'
  ) => v.push({ constraintId, constraint, severity, found, requiredAction, origin: 'BLUEPRINT' });

  // C01 — the locked order in the blueprint is still the order the creator stated.
  if (order.join('>') !== CREATOR_STATED_ORDER.join('>')) {
    B('C01_LOCKED_ORDER_INTACT',
      'The EP01 locked order is: ' + CREATOR_STATED_ORDER.join(' → '),
      'the blueprint now reads: ' + order.join(' → '),
      'restore the creator-stated order in src/core/canon/episode01.ts, or get the creator to change it on the record');
  }

  // C02 — the episode opens with the cold open.
  if (order[0] !== 'EP01_COLD_OPEN') {
    B('C02_COLD_OPEN_FIRST', 'The Cold Open opens the episode.',
      `first locked segment is ${order[0] ?? '(none)'}`,
      'put EP01_COLD_OPEN back at position 1');
  }

  // C03 — the gag sits between the letdown and the trip. This is the constraint
  // the creator has had to restate more than once, so it is checked directly
  // and not merely implied by C01.
  const i = (id: string) => order.indexOf(id);
  const letdown = i('EP01_SHUMAFIED_LETDOWN'), irish = i('EP01_LUCK_OF_THE_IRISH'), cigars = i('EP01_CIGARS');
  if (letdown < 0 || irish < 0 || cigars < 0 || !(letdown < irish && irish < cigars)) {
    B('C03_IRISH_BETWEEN_LETDOWN_AND_CIGARS',
      'Luck of the Irish plays AFTER the Shumafied disappointment / cigar setup and BEFORE the actual cigar trip.',
      `letdown@${letdown}, Luck of the Irish@${irish}, cigars@${cigars}`,
      'restore the gag between the setup and the trip — it is the payoff of the setup, not a floating interstitial');
  }

  // C04 — Joe is a reconstruction of a real event nobody filmed.
  const joe = seg('EP01_JOE');
  if (!joe) {
    B('C04_JOE_IS_RECONSTRUCTION', 'Joe is a 2D reconstruction of a real, unfilmed event.',
      'EP01_JOE is missing from the blueprint', 'restore the Joe segment');
  } else {
    const t = joe.treatment;
    if (t.footageExists || t.sourceReality !== 'REAL_EVENT_NO_FOOTAGE' || t.method === 'LIVE_ACTION') {
      B('C04_JOE_IS_RECONSTRUCTION',
        'Joe genuinely happened but was NOT filmed. It is depicted as a 2D reconstruction, never as recovered footage.',
        `footageExists=${t.footageExists}, sourceReality=${t.sourceReality}, method=${t.method}`,
        'set footageExists=false, sourceReality=REAL_EVENT_NO_FOOTAGE, and a non-LIVE_ACTION method');
    }
    if (!/2d/i.test(t.visualTreatment)) {
      B('C04_JOE_IS_2D', 'The Joe reconstruction is 2D.',
        'the Joe treatment no longer says 2D', 'restore the 2D reconstruction language');
    }
  }

  // C05 — Clothed and Confused is realistic. Not 2D. Not a 3D cartoon.
  const cc = seg('EP01_CLOTHED_AND_CONFUSED');
  if (!cc) {
    B('C05_CLOTHED_AND_CONFUSED_REALISTIC', 'Clothed and Confused is realistic, not animated.',
      'EP01_CLOTHED_AND_CONFUSED is missing from the blueprint', 'restore the segment');
  } else {
    const t = cc.treatment;
    if (!/realistic/i.test(t.visualTreatment)) {
      B('C05_CLOTHED_AND_CONFUSED_REALISTIC',
        'Clothed and Confused looks REALISTIC — survival-documentary language, played straight.',
        'the treatment no longer says realistic', 'restore the realistic survival-documentary treatment');
    }
    // The creator corrected this twice: it is not 2D and not a Blender cartoon.
    // Two separate failures — the exclusion going missing, and a positive claim
    // appearing — because they need different fixes.
    if (!/\bnot 2d\b/i.test(t.visualTreatment) || !/\bnot\b[^.]{0,40}\b3d\b/i.test(t.visualTreatment)) {
      B('C05_CLOTHED_AND_CONFUSED_NOT_2D_OR_3D',
        'Clothed and Confused is NOT 2D and NOT a Blender-looking 3D cartoon.',
        'the explicit "IT IS NOT 2D / NOT A BLENDER-LOOKING 3D CARTOON" exclusion is gone from the treatment',
        'restore the exclusion — it was corrected by the creator and is the reason the joke works');
    }
    // Look for a POSITIVE 2D/3D claim: drop the sentences that are exclusions
    // ("IT IS NOT 2D") first, so a correctly-worded treatment does not trip on
    // the very words it is there to rule out.
    const asserted = t.visualTreatment.split(/[.;]/).filter((sent) => !/\bnot\b/i.test(sent)).join(' ');
    if (/\b(?:2d|3d)\b/i.test(asserted)) {
      B('C05_CLOTHED_AND_CONFUSED_CLASSIFIED_ANIMATED',
        'Clothed and Confused is realistic. Classifying it as 2D or 3D is the correction the creator has already made twice.',
        `the treatment now positively asserts 2D/3D: "${asserted.trim().slice(0, 120)}"`,
        'remove the animated classification; the segment is realistic survival-documentary footage');
    }
  }

  // C06 — McBrain Feed is its own television segment.
  const tv = seg('EP01_TV');
  if (tv && !/mcbrain feed is a separate|separate future television segment/i.test(tv.treatment.visualTreatment)) {
    B('C06_MCBRAIN_FEED_SEPARATE',
      'McBrain Feed is a SEPARATE television segment and must not be merged into Clothed and Confused.',
      'the TV treatment no longer records McBrain Feed as separate',
      'restore the separation note on EP01_TV');
  }

  // C07 — Goodville is a gag FAMILY, and the creator has said there are more of
  // them than the repo records. Collapsing it to one insert loses gags.
  const goodville = EP01_UNPLACED_CANON.find((u) => u.id === 'GOODVILLE');
  if (!goodville) {
    B('C07_GOODVILLE_IS_A_GAG_FAMILY', 'Goodville is a recurring gag family, not a single insert.',
      'the Goodville entry is gone from EP01_UNPLACED_CANON', 'restore it');
  } else if ((goodville.knownMembers?.length ?? 0) < 2) {
    B('C07_GOODVILLE_IS_A_GAG_FAMILY', 'Goodville is a recurring gag family, not a single insert.',
      `only ${goodville.knownMembers?.length ?? 0} Goodville gag(s) recorded`,
      'keep every known Goodville gag listed; the creator has said there are more than are written down');
  }

  // C08 — a style nobody wrote down can never be presented as an instruction.
  for (const s of EPISODE_01) {
    if (s.treatment.visualTreatment === UNKNOWN_STYLE && s.treatment.visualTreatmentStatus === 'LOCKED_CANON') {
      B('C08_UNRECORDED_STYLE_NEVER_LOCKED',
        'A treatment the creator only described verbally stays UNSPECIFIED until it is written down.',
        `${s.name} carries the "not recorded" sentinel but is marked LOCKED_CANON`,
        'set visualTreatmentStatus back to UNSPECIFIED and ask the creator for the style');
    }
  }

  // C09 — production method is not one bucket. A segment with no footage cannot
  // be live action, whatever else it is.
  for (const s of EPISODE_01) {
    if (!s.treatment.footageExists && s.treatment.method === 'LIVE_ACTION') {
      B('C09_METHOD_NOT_COLLAPSED',
        'LIVE_ACTION / AI_ASSISTED_PRODUCTION / GENERATIVE_AI / HYBRID are different claims and are not interchangeable.',
        `${s.name} has no footage but is labelled LIVE_ACTION`,
        'label it with the method that actually produces it');
    }
  }

  return { violations: v, checked: BLUEPRINT_CONSTRAINT_IDS.length };
}

function assemblyChecks(scenes: AssemblyScene[]): {
  violations: CanonViolation[]; advisories: CanonViolation[];
  mappings: CanonMapping[]; absent: string[]; checked: number;
} {
  const violations: CanonViolation[] = [];
  const advisories: CanonViolation[] = [];
  const mappings = scenes.map(resolveCanonSegment);

  const ordered = [...scenes].sort((a, b) => a.proposedOrder - b.proposedOrder);
  const mapOf = new Map(mappings.map((m) => [m.sceneId, m]));

  // C10 — no locked segment relocated. Compared pairwise on distinct canon ids,
  // so two scenes covering the same segment never fight each other.
  outer: for (let a = 0; a < ordered.length; a++) {
    for (let b = a + 1; b < ordered.length; b++) {
      const ma = mapOf.get(ordered[a].id), mb = mapOf.get(ordered[b].id);
      const ida = ma?.canonSegmentId, idb = mb?.canonSegmentId;
      if (!ida || !idb || ida === idb) continue;
      const pa = canonPosition(ida), pb = canonPosition(idb);
      if (pa === undefined || pb === undefined) continue;
      if (pa > pb) {
        violations.push({
          constraintId: 'C10_NO_LOCKED_SEGMENT_RELOCATED',
          constraint:
            `${canonName(idb)} comes before ${canonName(ida)} in the locked EP01 order.`,
          severity: 'BLOCKING',
          found:
            `the cut plays "${ordered[a].proposedTitle}" (${ida}) at position ${a + 1}, ` +
            `before "${ordered[b].proposedTitle}" (${idb}) at position ${b + 1}`,
          requiredAction:
            `move "${ordered[b].proposedTitle}" before "${ordered[a].proposedTitle}", ` +
            'or have the creator change the locked order',
          origin: 'ASSEMBLY',
        });
        break outer; // one named violation is actionable; a cascade is not.
      }
    }
  }

  // C11 — editorial order and physical chronology stay separate fields. A scene
  // moved out of shooting order must say why, or the reorder becomes invisible.
  for (const s of scenes) {
    if (s.proposedOrder !== s.physicalOrder && !s.reorderReason?.trim()) {
      violations.push({
        constraintId: 'C11_REORDER_MUST_BE_VISIBLE',
        constraint:
          'Editorial order may differ from physical chronology, but the difference is always recorded as a reorder.',
        severity: 'BLOCKING',
        found: `"${s.proposedTitle}" sits at editorial ${s.proposedOrder} vs physical ${s.physicalOrder} with no reorderReason`,
        requiredAction: 'record why it moved, so the creator can see the reorder rather than discover it',
        origin: 'ASSEMBLY',
      });
    }
  }

  // A12 — locked segments with nothing in the cut. Normal mid-review; shown anyway.
  const present = new Set(mappings.map((m) => m.canonSegmentId).filter(Boolean) as string[]);
  const absent = lockedOrder().filter((id) => !present.has(id));
  if (absent.length) {
    advisories.push({
      constraintId: 'A12_LOCKED_SEGMENT_ABSENT',
      constraint: 'Every locked EP01 segment is eventually in the episode.',
      severity: 'ADVISORY',
      found: `${absent.length} locked segment(s) not in this cut: ${absent.map((id) => canonName(id) ?? id).join(', ')}`,
      requiredAction: 'build or approve them before this counts as the finished episode',
      origin: 'ASSEMBLY',
    });
  }

  // A13 — scenes the check could not tie to canon. It will not guess.
  const unmatched = mappings.filter((m) => m.method === 'UNMATCHED');
  if (unmatched.length) {
    advisories.push({
      constraintId: 'A13_SCENE_NOT_TIED_TO_CANON',
      constraint: 'Every scene in the episode is traceable to a canon segment.',
      severity: 'ADVISORY',
      found: `${unmatched.length} scene(s) could not be tied to canon: ${unmatched.map((m) => `"${m.title}"`).join(', ')}`,
      requiredAction: 'pin them with canonSegmentId, or confirm they are extra material outside the locked spine',
      origin: 'ASSEMBLY',
    });
  }

  return { violations, advisories, mappings, absent, checked: ASSEMBLY_CONSTRAINT_IDS.length };
}

/**
 * Runs the whole check. Pass the assembly to validate a cut; omit it to
 * validate the blueprint alone (useful as a repo-level guard).
 */
export function checkCanonCompliance(scenes?: AssemblyScene[]): CanonComplianceReport {
  const bp = blueprintChecks();
  const asm = scenes ? assemblyChecks(scenes) : undefined;

  const violations = [...bp.violations, ...(asm?.violations ?? [])];
  const ok = violations.length === 0;

  return {
    status: ok ? 'CANON_COMPLIANT' : 'CANON_COMPLIANCE_FAILED',
    ok,
    checkedAt: new Date().toISOString(),
    constraintsChecked: bp.checked + (asm?.checked ?? 0),
    violations,
    advisories: asm?.advisories ?? [],
    mappings: asm?.mappings ?? [],
    absentLockedSegments: asm?.absent ?? [],
    canonDoc: CANON_DOC_PATH,
  };
}

/** One line a human can read without opening the report. */
export function summariseCanonFailure(report: CanonComplianceReport): string {
  if (report.ok) return 'canon compliant';
  const first = report.violations[0];
  const more = report.violations.length - 1;
  return `CANON_COMPLIANCE_FAILED — ${first.constraintId}: ${first.constraint} ` +
    `Found: ${first.found}. Fix: ${first.requiredAction}.` +
    (more > 0 ? ` (+${more} more violation${more === 1 ? '' : 's'})` : '');
}
