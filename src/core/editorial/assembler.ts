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
  BeatMapEntry, ReconciledBeat, StoryBeat, CandidateKind,
} from './types';
import { classifyAll, type ClassifiedSegment } from './classification';
import { resolveCanonSegment } from '../canon/canonCompliance';
import { EPISODE_01, lockedOrder } from '../canon/episode01';

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
  /**
   * Order the first pass by the locked EP01 canon rather than by physical
   * chronology. This is what makes the autonomous assembly land in the episode
   * the creator actually asked for instead of the order the phone recorded it.
   * A narrativeOrder, when given, still wins — it is the creator speaking.
   */
  useCanonOrder?: boolean;
}

/** Pad around evidence so a cut does not start mid-word. */
const LEAD_IN = 1.0;
const LEAD_OUT = 1.5;

/**
 * A scene has to be long enough to be a scene. A 1.8-second fragment is a beat,
 * an insert or a reaction — not something to put in front of the creator and
 * call Scene 1.
 *
 * The fix is never to pad with unrelated footage: the window is EXPANDED into
 * the surrounding material that belongs to the same exchange, and if there
 * genuinely is not enough, the candidate is reported as a short beat rather
 * than promoted.
 */
const MIN_SCENE_SECONDS = 12;
/** How far either side we will look for material belonging to the same moment. */
const CONTEXT_REACH_SECONDS = 25;
/** A silence longer than this means the exchange has ended; stop expanding. */
const CONVERSATION_GAP = 6;
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

/**
 * How good a candidate is as a scene, and what it should be called.
 * Duration dominates: everything else is a refinement on top of "is there
 * actually enough here to watch".
 */
function scoreCandidate(x: {
  seconds: number; pieces: number; evidence: number;
  exclusions: number; confidence: number; spokenLines: number;
}): { kind: CandidateKind; reason: string; score: number } {
  const durationScore = Math.min(1, x.seconds / 45);
  const evidenceScore = Math.min(1, x.evidence / 6);
  const talkScore = Math.min(1, x.spokenLines / 5);
  const score = Number((durationScore * 0.45 + evidenceScore * 0.2 + talkScore * 0.2 + x.confidence * 0.15).toFixed(3));

  if (x.seconds < 4) {
    return {
      kind: 'INSERT', score,
      reason: `Only ${x.seconds.toFixed(1)}s of usable material — this is a cutaway or insert, not a scene on its own.`,
    };
  }
  if (x.seconds < MIN_SCENE_SECONDS) {
    return {
      kind: 'BEAT', score,
      reason: `${x.seconds.toFixed(1)}s — one beat inside a larger moment. I could not find enough surrounding footage to build it into a full scene.`,
    };
  }
  if (x.spokenLines === 0 && x.seconds < 20) {
    return {
      kind: 'INSUFFICIENT_COVERAGE', score,
      reason: `${x.seconds.toFixed(1)}s with no dialogue detected — not enough to tell what is happening.`,
    };
  }
  return {
    kind: 'SCENE', score,
    reason: `${x.seconds.toFixed(1)}s across ${x.pieces} piece${x.pieces === 1 ? '' : 's'} with ${x.spokenLines} spoken line${x.spokenLines === 1 ? '' : 's'} — enough for a beginning, a middle and an end.`,
  };
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

    // Grow the window outwards through speech that belongs to the same
    // exchange, so the scene contains the whole interaction rather than the one
    // line that happened to match a cue.
    const ordered = [...segs].sort((a, b) => a.startTime - b.startTime);
    let expStart = winStart, expEnd = winEnd;

    for (let pass = 0; pass < 40; pass++) {
      const before = ordered.filter((x) => x.endTime <= expStart && expStart - x.endTime <= CONVERSATION_GAP);
      const after = ordered.filter((x) => x.startTime >= expEnd && x.startTime - expEnd <= CONVERSATION_GAP);
      const prev = before[before.length - 1];
      const next = after[0];
      let grew = false;

      if (prev && expStart - prev.startTime <= CONTEXT_REACH_SECONDS) {
        expStart = Math.max(0, prev.startTime - 0.3);
        grew = true;
      }
      if (next && next.endTime - expEnd <= CONTEXT_REACH_SECONDS) {
        expEnd = next.endTime + 0.4;
        grew = true;
      }
      if (!grew) break;
      if (expEnd - expStart >= MIN_SCENE_SECONDS * 2.5) break; // long enough
    }

    const winStartX = expStart, winEndX = expEnd;
    const inWindow = segs.filter((s) => s.endTime > winStartX && s.startTime < winEndX);

    // Production artifacts are excluded from the cut and preserved in source.
    const exclusions: EditorialExclusion[] = inWindow
      .filter((s) => s.classification !== 'PROGRAM_CONTENT' && !(s.classification === 'UNCERTAIN'))
      .map((s) => ({
        range: {
          sourceFileId: s.sourceFileId,
          startTime: Math.max(winStartX, s.startTime),
          endTime: Math.min(winEndX, s.endTime),
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
          startTime: Math.max(winStartX, s.startTime - 0.2),
          endTime: Math.min(winEndX, s.endTime + 0.3),
          derivedFromObservationIds: [s.observationId],
        }))
      : [{
          sourceFileId: fileId, startTime: winStartX, endTime: winEndX,
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

    const sceneSeconds = duration(ranges);
    const quality = scoreCandidate({
      seconds: sceneSeconds,
      pieces: ranges.length,
      evidence: ev.length,
      exclusions: exclusions.length,
      confidence: rb.confidence,
      spokenLines: keep.length,
    });

    candidates.push({
      id: `scene_${Date.now().toString(36)}_${(seq++).toString(36)}`,
      kind: quality.kind,
      kindReason: quality.reason,
      qualityScore: quality.score,
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
  } else if (input.useCanonOrder) {
    // The locked EP01 spine. Each candidate is tied to a canon segment (and the
    // id is stamped on it, so the compliance check reads a decision rather than
    // re-deriving one). Anything that does not resolve keeps physical order and
    // sits after the spine — it is extra material, not a reason to guess.
    const canonRank = new Map(lockedOrder().map((id, i) => [id, i]));
    const spineSize = canonRank.size;

    for (const c of candidates) {
      const m = resolveCanonSegment({
        id: c.id, proposedTitle: c.proposedTitle,
        proposedOrder: c.proposedOrder, physicalOrder: c.physicalOrder,
        storyBeatIds: c.storyBeatIds, canonSegmentId: c.canonSegmentId,
      });
      if (m.canonSegmentId) c.canonSegmentId = m.canonSegmentId;
    }

    const rankOf = (c: EditorialSceneCandidate) =>
      c.canonSegmentId !== undefined ? canonRank.get(c.canonSegmentId) ?? spineSize : spineSize;

    const byCanon = [...candidates].sort((a, b) => {
      const ar = rankOf(a), br = rankOf(b);
      return ar === br ? a.physicalOrder - b.physicalOrder : ar - br;
    });
    byCanon.forEach((c, i) => {
      c.proposedOrder = i;
      if (c.proposedOrder !== c.physicalOrder) {
        const seg = EPISODE_01.find((x) => x.id === c.canonSegmentId);
        c.reorderReason = seg
          ? `Editorial position ${i} differs from physical position ${c.physicalOrder}: ` +
            `placed at the locked EP01 position for ${seg.name}. ${seg.placementReason} ` +
            'Physical chronology is unchanged.'
          : `Editorial position ${i} differs from physical position ${c.physicalOrder}: ` +
            'material outside the locked EP01 spine, kept in physical order behind it. ' +
            'Physical chronology is unchanged.';
      }
    });
  } else {
    byPhysical.forEach((c, i) => { c.proposedOrder = i; });
  }

  // Real scenes are shown before beats and inserts, so the creator is never
  // handed a 2-second fragment as "Scene 1" while a proper scene waits behind it.
  const rank: Record<CandidateKind, number> = { SCENE: 0, BEAT: 1, INSERT: 2, INSUFFICIENT_COVERAGE: 3 };
  return candidates.sort((a, b) =>
    rank[a.kind] !== rank[b.kind] ? rank[a.kind] - rank[b.kind] : a.proposedOrder - b.proposedOrder);
}
