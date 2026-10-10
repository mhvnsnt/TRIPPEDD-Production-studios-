/**
 * Mentioned-material reconciliation.
 *
 * Matches the creator's remembered beats against ACTUAL machine observations
 * from ingested media. The output is deliberately conservative:
 *
 *   - a beat with no supporting evidence is NOT_FOUND, never quietly dropped
 *     and never quietly promoted;
 *   - a PARTIAL mention that finds something is PARTIALLY_FOUND at best,
 *     because a vague memory matching a keyword is not proof;
 *   - evidence spread thinly across many files is AMBIGUOUS_MATCH, not a hit;
 *   - when nothing has been ingested at all, the state is MISSING_SOURCE_MEDIA,
 *     which is a different statement from "this did not happen".
 *
 * Every match carries the observation, the timestamp and the cue that fired, so
 * a human can judge it instead of trusting a number.
 */
import type { MachineObservation } from '../analysis/analyzers';
import type { StoryBeat, ReconciledBeat, MatchEvidence, ReconciliationState } from './types';
import { DEFAULT_STORY_INVENTORY } from './storyInventory';

/** Observations that carry text we can search. */
const TEXT_TYPES = new Set(['TRANSCRIPT_SEGMENT', 'ON_SCREEN_TEXT']);

export interface ObservationWithSource extends MachineObservation {
  sourceFileId: string;
}

function normalise(s: string): string {
  return s.toLowerCase().replace(/[^\w\s']/g, ' ').replace(/\s+/g, ' ').trim();
}

/** Whole-token containment, so "pack" does not match "backpack". */
function containsCue(haystack: string, cue: string): boolean {
  const h = normalise(haystack);
  const c = normalise(cue);
  if (!c) return false;
  if (c.includes(' ')) return h.includes(c);
  return new RegExp(`(^|\\s)${c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(\\s|$)`).test(h);
}

function allCues(beat: StoryBeat): { cue: string; kind: string }[] {
  const out: { cue: string; kind: string }[] = [];
  for (const c of beat.cues.dialogue ?? []) out.push({ cue: c, kind: 'dialogue' });
  for (const c of beat.cues.onScreenText ?? []) out.push({ cue: c, kind: 'onScreenText' });
  for (const c of beat.cues.entities ?? []) out.push({ cue: c, kind: 'entity' });
  return out;
}

export interface ReconcileOptions {
  /** Distinct cues needed before a match is more than incidental. */
  strongCueThreshold?: number;
  /** Fraction of a beat's cues that must fire for a FOUND verdict. */
  foundCueFraction?: number;
}

export function reconcileBeat(
  beat: StoryBeat,
  observations: ObservationWithSource[],
  opts: ReconcileOptions = {}
): ReconciledBeat {
  const strongCueThreshold = opts.strongCueThreshold ?? 2;
  const foundCueFraction = opts.foundCueFraction ?? 0.34;

  const cues = allCues(beat);
  const evidence: MatchEvidence[] = [];
  const firedCues = new Set<string>();
  const perFile = new Map<string, number>();

  for (const o of observations) {
    const text = o.text ?? '';
    if (!text || !TEXT_TYPES.has(o.type)) continue;
    for (const { cue } of cues) {
      if (!containsCue(text, cue)) continue;
      firedCues.add(cue);
      perFile.set(o.sourceFileId, (perFile.get(o.sourceFileId) ?? 0) + 1);
      evidence.push({
        observationId: o.id,
        sourceFileId: o.sourceFileId,
        type: o.type,
        startTime: o.startTime,
        endTime: o.endTime,
        excerpt: text.slice(0, 160),
        matchedCue: cue,
        tool: o.tool,
      });
    }
  }

  const unmatchedCues = cues.map((c) => c.cue).filter((c) => !firedCues.has(c));
  const candidateSourceFileIds = [...perFile.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([id]) => id);

  // Nothing ingested at all is a different claim from "not in the footage".
  if (observations.length === 0) {
    return {
      beatId: beat.id, title: beat.title, mentionStrength: beat.mentionStrength,
      state: 'MISSING_SOURCE_MEDIA', confidence: 0, evidence: [],
      candidateSourceFileIds: [],
      rationale: 'No source media has been ingested yet, so this beat cannot be looked for.',
      unmatchedCues: cues.map((c) => c.cue),
    };
  }

  let state: ReconciliationState;
  let rationale: string;
  const distinctCues = firedCues.size;
  const cueFraction = cues.length ? distinctCues / cues.length : 0;

  if (distinctCues === 0) {
    state = 'NOT_FOUND';
    rationale = `None of the ${cues.length} cues for this beat appear in any ingested transcript or on-screen text. This is an absence of evidence in the media ingested so far, not proof the event did not happen.`;
  } else if (candidateSourceFileIds.length > 2 && distinctCues < strongCueThreshold) {
    // One weak cue scattered across several clips is noise, not a location.
    state = 'AMBIGUOUS_MATCH';
    rationale = `${distinctCues} cue(s) matched across ${candidateSourceFileIds.length} different source files without a clear concentration. Needs a human to say which, if any, is the beat.`;
  } else if (beat.mentionStrength === 'PARTIAL') {
    // A vague memory matching keywords is never a confident find.
    state = 'PARTIALLY_FOUND';
    rationale = `${distinctCues} cue(s) matched, but this beat was only partially described, so the match cannot be treated as confirmed. Human confirmation required.`;
  } else if (distinctCues >= strongCueThreshold && cueFraction >= foundCueFraction) {
    state = 'FOUND';
    rationale = `${distinctCues} of ${cues.length} cues matched in ${candidateSourceFileIds.length} source file(s), concentrated enough to propose as this beat.`;
  } else {
    state = 'PARTIALLY_FOUND';
    rationale = `${distinctCues} of ${cues.length} cues matched — enough to flag, not enough to call it found.`;
  }

  // Confidence is bounded by how firmly the beat was described in the first
  // place: a partial memory can never yield a high-confidence match.
  const raw = Math.min(1, cueFraction * 0.7 + Math.min(distinctCues, 4) / 4 * 0.3);
  const ceiling = beat.mentionStrength === 'PARTIAL' ? 0.6 : 0.95;
  const confidence = state === 'NOT_FOUND' ? 0 : Math.min(raw, ceiling);

  return {
    beatId: beat.id, title: beat.title, mentionStrength: beat.mentionStrength,
    state, confidence: Number(confidence.toFixed(3)),
    evidence, candidateSourceFileIds, rationale, unmatchedCues,
  };
}

export interface ReconciliationReport {
  beats: ReconciledBeat[];
  summary: Record<ReconciliationState, number>;
  /** Beats the editor may build scenes from. */
  actionable: ReconciledBeat[];
  /** Beats that need footage or a human before they can be scened. */
  blocked: ReconciledBeat[];
  observationCount: number;
  sourceFileCount: number;
}

export function reconcileInventory(
  observations: ObservationWithSource[],
  beats: StoryBeat[] = DEFAULT_STORY_INVENTORY,
  opts: ReconcileOptions = {}
): ReconciliationReport {
  const results = beats.map((b) => reconcileBeat(b, observations, opts));

  const summary = {
    FOUND: 0, PARTIALLY_FOUND: 0, NOT_FOUND: 0,
    AMBIGUOUS_MATCH: 0, MISSING_SOURCE_MEDIA: 0,
  } as Record<ReconciliationState, number>;
  for (const r of results) summary[r.state]++;

  return {
    beats: results,
    summary,
    // Only FOUND beats are safe to assemble from without a human first.
    actionable: results.filter((r) => r.state === 'FOUND'),
    blocked: results.filter((r) => r.state !== 'FOUND'),
    observationCount: observations.length,
    sourceFileCount: new Set(observations.map((o) => o.sourceFileId)).size,
  };
}
