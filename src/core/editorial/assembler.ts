/**
 * Autonomous scene assembly.
 *
 * Builds EditorialSceneCandidates from REAL observation timestamps. Every range
 * in a proposed cut traces back to observations that justify it, so a human
 * reviewing a scene can ask "why this shot?" and get an answer instead of a
 * confidence score.
 *
 * Two things this deliberately does not do:
 *   - assemble from a beat that is not FOUND (a remembered beat is not footage);
 *   - collapse physical chronology into editorial order. Both positions are
 *     carried on every candidate, so a reorder is always visible as a reorder.
 */
import type { MachineObservation } from '../analysis/analyzers';
import type {
  EditorialSceneCandidate, SourceRange, EditorialExclusion,
  BeatMapEntry, ReconciledBeat, StoryBeat,
} from './types';
import { classifyAll, type ClassifiedSegment } from './classification';

export interface AssemblyInput {
  productionUnitId: string;
  observations: (MachineObservation & { sourceFileId: string })[];
  reconciled: ReconciledBeat[];
  beats: StoryBeat[];
  /** Narrative order the creator wants, by beat id. Absent = physical order. */
  narrativeOrder?: string[];
  /**
   * Tools that were resource-blocked during ingest, by source file id. Scenes
   * built from that file declare the gap and carry reduced confidence.
   */
  blockedTools?: Record<string, string[]>;
}

/** Pad around evidence so a cut does not start mid-word. */
const LEAD_IN = 1.0;
const LEAD_OUT = 1.5;
/** Ranges closer than this are merged rather than left as a visible seam. */
const MERGE_GAP = 0.75;

function mergeRanges(ranges: SourceRange[]): SourceRange[] {
  const sorted = [...ranges].sort((a, b) =>
    a.sourceFileId === b.sourceFileId ? a.startTime - b.startTime : a.sourceFileId.localeCompare(b.sourceFileId)
  );
  const out: SourceRange[] = [];
  for (const r of sorted) {
    const last = out[out.length - 1];
    if (last && last.sourceFileId === r.sourceFileId && r.startTime - last.endTime <= MERGE_GAP) {
      last.endTime = Math.max(last.endTime, r.endTime);
      last.derivedFromObservationIds.push(...r.derivedFromObservationIds);
    } else {
      out.push({ ...r, derivedFromObservationIds: [...r.derivedFromObservationIds] });
    }
  }
  return out;
}

function duration(ranges: SourceRange[]): number {
  return Number(ranges.reduce((a, r) => a + (r.endTime - r.startTime), 0).toFixed(3));
}

/** Shot boundaries let a cut land on a real edit point instead of mid-shot. */
function snapToShot(
  t: number, shots: MachineObservation[], edge: 'start' | 'end'
): number {
  let best = t;
  let bestDist = Infinity;
  for (const s of shots) {
    const cand = edge === 'start' ? s.startTime : s.endTime;
    if (cand == null) continue;
    const d = Math.abs(cand - t);
    // Only snap when the boundary is genuinely nearby; otherwise keep the
    // evidence-derived time rather than dragging the cut somewhere arbitrary.
    if (d < bestDist && d <= 2.0) { best = cand; bestDist = d; }
  }
  return Number(best.toFixed(3));
}

/** Two candidates sharing at least this much of their footage are one scene. */
const SCENE_MERGE_OVERLAP = 0.6;

/** Fraction of the smaller candidate's duration that overlaps the larger. */
function overlapFraction(a: EditorialSceneCandidate, b: EditorialSceneCandidate): number {
  let shared = 0;
  for (const ra of a.ranges) {
    for (const rb of b.ranges) {
      if (ra.sourceFileId !== rb.sourceFileId) continue;
      shared += Math.max(0, Math.min(ra.endTime, rb.endTime) - Math.max(ra.startTime, rb.startTime));
    }
  }
  const smaller = Math.min(a.proposedDuration, b.proposedDuration);
  return smaller > 0 ? shared / smaller : 0;
}

/** What the absence of each analyzer actually costs the edit. */
const LIMITATION_EFFECT: Record<string, string> = {
  whisperx: 'cut points come from utterance-level timings, so in/out points are less precise than word-level alignment would give',
  'faster-whisper': 'no transcript, so dialogue could not inform selection or exclusion',
  pyscenedetect: 'no shot boundaries, so cuts were not snapped to real edit points',
  opencv: 'no visual motion or blank-frame analysis',
  tesseract: 'no on-screen text recovery',
  demucs: 'dialogue was not isolated from background audio',
};

/** Confidence multiplier per missing analyzer, floored so a scene stays usable. */
const LIMITATION_WEIGHT: Record<string, number> = {
  'faster-whisper': 0.7,
  pyscenedetect: 0.85,
  whisperx: 0.92,
  opencv: 0.95,
  tesseract: 0.97,
  demucs: 0.98,
};

function limitationsFor(blocked: string[]) {
  return blocked.map((tool) => ({
    tool,
    reason: 'RESOURCE_BLOCKED during ingest',
    effect: LIMITATION_EFFECT[tool] ?? 'this analysis did not contribute to the scene',
  }));
}

function confidencePenalty(blocked: string[]): number {
  return Math.max(0.5, blocked.reduce((acc, t) => acc * (LIMITATION_WEIGHT[t] ?? 0.95), 1));
}

let seq = 0;

export function assembleScenes(input: AssemblyInput): EditorialSceneCandidate[] {
  const { productionUnitId, observations, reconciled, beats } = input;
  const classified = classifyAll(observations);
  const byFileClassified = new Map<string, ClassifiedSegment[]>();
  for (const c of classified) {
    if (!byFileClassified.has(c.sourceFileId)) byFileClassified.set(c.sourceFileId, []);
    byFileClassified.get(c.sourceFileId)!.push(c);
  }

  const shotsByFile = new Map<string, MachineObservation[]>();
  for (const o of observations) {
    if (o.type !== 'SHOT_BOUNDARY') continue;
    if (!shotsByFile.has(o.sourceFileId)) shotsByFile.set(o.sourceFileId, []);
    shotsByFile.get(o.sourceFileId)!.push(o);
  }

  const candidates: EditorialSceneCandidate[] = [];

  // Only FOUND beats are assembled autonomously. Everything else is surfaced
  // in the reconciliation report for a human to resolve first.
  for (const rb of reconciled.filter((r) => r.state === 'FOUND')) {
    const beat = beats.find((b) => b.id === rb.beatId);
    if (!beat) continue;

    const fileId = rb.candidateSourceFileIds[0];
    if (!fileId) continue;

    const ev = rb.evidence.filter((e) => e.sourceFileId === fileId && e.startTime != null);
    if (!ev.length) continue;

    const shots = shotsByFile.get(fileId) ?? [];
    const segs = byFileClassified.get(fileId) ?? [];

    // Window: from the first supporting moment to the last, padded.
    const evStart = Math.min(...ev.map((e) => e.startTime!));
    const evEnd = Math.max(...ev.map((e) => e.endTime ?? e.startTime!));
    const winStart = snapToShot(Math.max(0, evStart - LEAD_IN), shots, 'start');
    const winEnd = snapToShot(evEnd + LEAD_OUT, shots, 'end');

    const inWindow = segs.filter((s) => s.endTime > winStart && s.startTime < winEnd);

    // Production artifacts are excluded from the cut and preserved in source.
    const exclusions: EditorialExclusion[] = inWindow
      .filter((s) => s.classification !== 'PROGRAM_CONTENT' && !(s.classification === 'UNCERTAIN'))
      .map((s) => ({
        range: {
          sourceFileId: s.sourceFileId,
          startTime: Math.max(winStart, s.startTime),
          endTime: Math.min(winEnd, s.endTime),
          derivedFromObservationIds: [s.observationId],
        },
        classification: s.classification,
        reason: s.reason,
        preservedInPhysicalTimeline: true,
        excerpt: s.text || undefined,
      }));

    // Program content only. An UNCERTAIN segment is KEPT (never silently cut)
    // and flagged as an assumption for the human to settle.
    const keep = inWindow.filter(
      (s) => s.classification === 'PROGRAM_CONTENT' || s.classification === 'UNCERTAIN'
    );

    const rawRanges: SourceRange[] = keep.length
      ? keep.map((s) => ({
          sourceFileId: s.sourceFileId,
          startTime: Math.max(winStart, s.startTime - 0.2),
          endTime: Math.min(winEnd, s.endTime + 0.3),
          derivedFromObservationIds: [s.observationId],
        }))
      : [{
          sourceFileId: fileId, startTime: winStart, endTime: winEnd,
          derivedFromObservationIds: ev.map((e) => e.observationId),
        }];

    const ranges = mergeRanges(rawRanges);
    if (!ranges.length) continue;

    const beatMap: BeatMapEntry[] = [];
    beatMap.push({ role: 'OPENING', range: ranges[0], rationale: 'first program content supporting this beat' });
    if (ranges.length > 2) {
      beatMap.push({ role: 'ESCALATION', range: ranges[Math.floor(ranges.length / 2)], rationale: 'mid-scene development' });
    }
    // Payoff: the range carrying the most supporting evidence.
    const payoff = ranges.reduce((a, b) =>
      b.derivedFromObservationIds.length > a.derivedFromObservationIds.length ? b : a, ranges[0]);
    beatMap.push({ role: 'PAYOFF', range: payoff, rationale: 'densest concentration of supporting evidence' });
    beatMap.push({ role: 'EXIT', range: ranges[ranges.length - 1], rationale: 'last program content before the window closes' });

    const uncertain = inWindow.filter((s) => s.classification === 'UNCERTAIN');

    candidates.push({
      id: `scene_${Date.now().toString(36)}_${(seq++).toString(36)}`,
      productionUnitId,
      proposedTitle: beat.title,
      purpose: beat.description,
      sourceEvidenceIds: rb.evidence.map((e) => e.observationId),
      sourceClipIds: [fileId],
      transcriptSegmentIds: keep.map((s) => s.observationId),
      visualObservationIds: observations
        .filter((o) => o.sourceFileId === fileId && (o.type === 'VISUAL_CHANGE' || o.type === 'ON_SCREEN_TEXT'))
        .map((o) => o.id),
      referenceIds: [],
      storyBeatIds: [beat.id],
      proposedOrder: 0,   // assigned below
      physicalOrder: 0,   // assigned below
      ranges,
      proposedDuration: duration(ranges),
      beatMap,
      excludedMaterial: exclusions,
      // Missing analysis lowers confidence rather than being silently ignored.
      confidence: Number(
        (rb.confidence * confidencePenalty(input.blockedTools?.[fileId] ?? [])).toFixed(3)
      ),
      editorialRationale:
        `Assembled from ${ev.length} supporting observation(s) in ${fileId}. ` +
        `${exclusions.length} production-artifact segment(s) excluded from the cut and preserved in the physical timeline.`,
      chronologyAssumptions: uncertain.map((u) => ({
        statement: `"${u.text.slice(0, 80)}" at ${u.startTime.toFixed(1)}s may be a camera cue rather than dialogue; kept in the cut pending review.`,
        confidence: 'POSSIBLE' as const,
      })),
      missingEvidence: rb.unmatchedCues.length
        ? [`cues with no supporting evidence: ${rb.unmatchedCues.join(', ')}`]
        : [],
      evidenceLimitations: limitationsFor(input.blockedTools?.[fileId] ?? []),
      requiredAssets: [],
      generatedAssetIds: [],
      humanReviewState: 'PROPOSED',
      revisionHistory: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
  }

  // Two beats can legitimately describe the same moment ("bag interruption"
  // and "bag-return argument" both land on the same argument). Emitting both as
  // separate scenes would put the identical cut in the episode twice, so
  // candidates covering substantially the same footage are merged and carry
  // every beat they satisfy.
  const merged: EditorialSceneCandidate[] = [];
  for (const c of candidates) {
    const twin = merged.find((m) => overlapFraction(m, c) >= SCENE_MERGE_OVERLAP);
    if (!twin) { merged.push(c); continue; }

    twin.storyBeatIds.push(...c.storyBeatIds.filter((b) => !twin.storyBeatIds.includes(b)));
    twin.sourceEvidenceIds = [...new Set([...twin.sourceEvidenceIds, ...c.sourceEvidenceIds])];
    twin.transcriptSegmentIds = [...new Set([...twin.transcriptSegmentIds, ...c.transcriptSegmentIds])];
    // Keep the strongest supporting evidence as the headline confidence.
    twin.confidence = Math.max(twin.confidence, c.confidence);
    const titles = twin.storyBeatIds
      .map((id) => beats.find((b) => b.id === id)?.title)
      .filter(Boolean) as string[];
    twin.proposedTitle = titles.join(' / ');
    twin.editorialRationale +=
      ` Merged with "${c.proposedTitle}": both beats resolve to the same footage, so the moment appears once.`;
  }
  candidates.length = 0;
  candidates.push(...merged);

  // Physical order: when the material actually occurred, by earliest range.
  const byPhysical = [...candidates].sort((a, b) => {
    const as = Math.min(...a.ranges.map((r) => r.startTime));
    const bs = Math.min(...b.ranges.map((r) => r.startTime));
    return a.sourceClipIds[0] === b.sourceClipIds[0]
      ? as - bs
      : a.sourceClipIds[0].localeCompare(b.sourceClipIds[0]);
  });
  byPhysical.forEach((c, i) => { c.physicalOrder = i; });

  // Editorial order: the creator's narrative order when given. A difference
  // between the two is recorded as a deliberate reorder, never hidden.
  const order = input.narrativeOrder;
  if (order?.length) {
    const rank = new Map(order.map((id, i) => [id, i]));
    // A merged scene satisfies several beats, so it ranks by the EARLIEST beat
    // the creator placed. Ranking on storyBeatIds[0] alone would let the merge
    // order decide narrative position, which is arbitrary.
    const rankOf = (c: EditorialSceneCandidate) =>
      Math.min(...c.storyBeatIds.map((id) => rank.get(id) ?? Number.MAX_SAFE_INTEGER));
    const byEditorial = [...candidates].sort((a, b) => {
      const ar = rankOf(a), br = rankOf(b);
      return ar === br ? a.physicalOrder - b.physicalOrder : ar - br;
    });
    byEditorial.forEach((c, i) => {
      c.proposedOrder = i;
      if (c.proposedOrder !== c.physicalOrder) {
        c.reorderReason =
          `Editorial position ${i} differs from physical position ${c.physicalOrder}: ` +
          `placed to follow the creator's narrative order. Physical chronology is unchanged.`;
      }
    });
  } else {
    byPhysical.forEach((c, i) => { c.proposedOrder = i; });
  }

  return candidates.sort((a, b) => a.proposedOrder - b.proposedOrder);
}
