/**
 * EP01: the production graph, reconciled against the locked blueprint.
 *
 * The graph in episodes.ts was authored before the canon was written down. It
 * held five segments — Motel, Joe, Goodville Geography, Luck of the Irish,
 * Goodville Cartoon — in an order that puts Joe second and the Luck of the
 * Irish commercial fourth. The blueprint locks eleven segments in a different
 * order. Where the two disagree, THE BLUEPRINT WINS; the fixture is not
 * authoritative about the episode.
 *
 * The eight segments the graph never had are not omitted here. They are
 * materialised with productionState 'NOT_STARTED', so the episode carries every
 * locked segment and the ones nobody has built are visibly unbuilt. A missing
 * segment is a gap somebody eventually notices; an absent one is a gap nobody
 * ever sees.
 *
 * Provenance for an unbuilt segment is DERIVED FROM THE BLUEPRINT, never
 * invented: where the creator has stated the method, it is carried across;
 * where the blueprint says UNSPECIFIED, the provenance says UNKNOWN.
 */
import type { ContentProvenance, Segment } from '../types';
import { EPISODE_01, lockedOrder, type CanonSegment } from '../canon/episode01';

/** Blueprint treatment → production provenance. UNSPECIFIED becomes UNKNOWN. */
export function canonToProvenance(s: CanonSegment): ContentProvenance {
  const t = s.treatment;
  const specified = t.methodStatus !== 'UNSPECIFIED';

  const realityStatus: ContentProvenance['realityStatus'] =
    t.sourceReality === 'FICTIONAL' ? 'FICTIONAL'
    : t.sourceReality === 'REAL_EVENT_NO_FOOTAGE' ? 'FICTIONALIZED_FACT'
    : 'FACTUAL';

  const captureStatus: ContentProvenance['captureStatus'] =
    t.sourceReality === 'REAL_EVENT_NO_FOOTAGE' ? 'RECONSTRUCTED'
    : !t.footageExists ? 'NOT_CAPTURED'
    : t.method === 'HYBRID' ? 'PARTIALLY_CAPTURED'
    : t.method === 'LIVE_ACTION' ? 'DIRECTLY_CAPTURED'
    : 'UNKNOWN';

  const generationMethods: ContentProvenance['generationMethods'] =
    !specified ? []
    : t.method === 'LIVE_ACTION' ? ['LIVE_CAPTURE']
    : t.method === 'GENERATIVE_AI' ? ['AI_GENERATED']
    : t.method === 'AI_ASSISTED_PRODUCTION' ? ['AI_ASSISTED']
    : ['LIVE_CAPTURE', 'AI_GENERATED'];

  const assemblyMode: ContentProvenance['assemblyMode'] =
    t.method === 'LIVE_ACTION' ? 'PURE_LIVE_ACTION'
    : t.method === 'GENERATIVE_AI' ? 'PURE_GENERATED'
    : t.sourceReality === 'REAL_EVENT_NO_FOOTAGE' ? 'RECONSTRUCTED_REAL_EVENT'
    : 'LIVE_ACTION_WITH_GENERATED_ELEMENTS';

  return {
    realityStatus,
    captureStatus,
    authorship: !specified ? 'UNKNOWN'
      : t.method === 'LIVE_ACTION' ? 'USER_AUTHORED' : 'COLLABORATIVE_AUTHORED',
    generationMethods,
    assemblyMode,
    aiContributions: t.method === 'LIVE_ACTION' ? ['NONE'] : ['AI_CO_GENERATED'],
    // Not yet made. 'PLAN' is what this is, and saying so keeps it out of any
    // count of real production.
    aggregate: 'PLAN',
  };
}

/** A locked segment nobody has built, present in the graph and marked as such. */
export function plannedSegment(s: CanonSegment): Segment {
  return {
    id: `PLAN_${s.id}`,
    name: s.name,
    description:
      `${s.placementReason} NOT YET BUILT — locked into EP01 by the creator, no production work started.` +
      (s.openQuestions.length ? ` Open: ${s.openQuestions.join(' ')}` : ''),
    canonSegmentId: s.id,
    productionState: 'NOT_STARTED',
    performances: [],
    gags: [],
    sourceClips: [],
    assetIds: [],
    jobIds: [],
    provenance: canonToProvenance(s),
  };
}

export interface Ep01ReconciliationReport {
  /** Locked segments with a real authored segment behind them. */
  built: { canonSegmentId: string; segmentId: string; name: string }[];
  /** Locked segments carried as explicit NOT_STARTED placeholders. */
  planned: { canonSegmentId: string; name: string; openQuestions: string[] }[];
  /** Authored segments outside the locked spine (the Goodville gag family). */
  unplaced: { segmentId: string; name: string }[];
  /** The order the graph will present, which is the blueprint's order. */
  order: string[];
}

/**
 * Composes the episode's segments in the locked canon order: an authored
 * segment where one exists, an explicit placeholder where one does not, and
 * everything outside the locked spine appended afterwards rather than dropped.
 */
export function reconcileEpisode01(authored: Segment[]): {
  segments: Segment[]; report: Ep01ReconciliationReport;
} {
  const byCanon = new Map<string, Segment>();
  for (const seg of authored) if (seg.canonSegmentId) byCanon.set(seg.canonSegmentId, seg);

  const segments: Segment[] = [];
  const report: Ep01ReconciliationReport = { built: [], planned: [], unplaced: [], order: [] };

  for (const canonId of lockedOrder()) {
    const canon = EPISODE_01.find((s) => s.id === canonId)!;
    const existing = byCanon.get(canonId);
    if (existing) {
      segments.push(existing);
      report.built.push({ canonSegmentId: canonId, segmentId: existing.id, name: canon.name });
    } else {
      segments.push(plannedSegment(canon));
      report.planned.push({ canonSegmentId: canonId, name: canon.name, openQuestions: canon.openQuestions });
    }
    report.order.push(canon.name);
  }

  // Anything the creator has not locked a position for still belongs to the
  // episode. Dropping it because the spine has no slot is how a Goodville gag
  // disappears.
  for (const seg of authored) {
    if (seg.canonSegmentId && byCanon.get(seg.canonSegmentId) === seg) continue;
    segments.push(seg);
    report.unplaced.push({ segmentId: seg.id, name: seg.name });
    report.order.push(`${seg.name} (position not locked)`);
  }

  return { segments, report };
}
