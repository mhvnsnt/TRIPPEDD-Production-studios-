import { createEp01PilotPlan, type PilotBeat } from './ep01Pilot';

export interface EpisodeAssemblyItem {
  id: string;
  beatId: string;
  kind: 'SOURCE' | 'GENERATED' | 'EDITORIAL';
  title: string;
  sourceLabels: string[];
  formatId: string;
  generationPurpose?: string;
  approvalRequired: boolean;
  terminal?: boolean;
}

export interface EpisodeAssemblyPlan {
  episodeId: string;
  title: string;
  items: EpisodeAssemblyItem[];
  rule: string;
}

const source = (beat: PilotBeat, labels: string[]): EpisodeAssemblyItem => ({
  id: `ep01-${beat.id}`,
  beatId: beat.id,
  kind: 'SOURCE',
  title: beat.title,
  sourceLabels: labels,
  formatId: 'LIVE_SKETCH',
  approvalRequired: beat.humanApprovalRequired,
});

const generated = (beat: PilotBeat, purpose: string): EpisodeAssemblyItem => ({
  id: `ep01-${beat.id}`,
  beatId: beat.id,
  kind: 'GENERATED',
  title: beat.title,
  sourceLabels: [],
  formatId: 'HYBRID',
  generationPurpose: purpose,
  approvalRequired: beat.humanApprovalRequired,
});

/**
 * Converts the canonical story into a source-traceable assembly recipe.
 * It deliberately does not invent timestamps; those are filled from reviewed
 * physical-timeline evidence after ingest analysis.
 */
export function createEp01AssemblyPlan(): EpisodeAssemblyPlan {
  const plan = createEp01PilotPlan();
  const byId = new Map(plan.beats.map(beat => [beat.id, beat]));
  const items: EpisodeAssemblyItem[] = [
    source(byId.get('motel-reality')!, ['MOTEL_HANGOUT']),
    source(byId.get('shumafied-item')!, ['SHUMAFIED_ITEM']),
    source(byId.get('cigar-run')!, ['DECISION_TO_GET_CIGARS', 'WALK_TO_GET_CIGARS']),
    source(byId.get('walk-and-bag')!, ['BAG_INCIDENT', 'BAG_ARGUMENT', 'PEOPLE_LEAVE']),
    source(byId.get('joe-and-goodville')!, ['JOE_INTERACTION', 'PRAYER', 'TIC_TAC_EXCHANGE', 'INTRODUCTION', 'SMOKING_HANGOUT', 'OTHER']),
    generated(byId.get('shumafied-subjective-shift')!, 'Represent the character\'s subjective experience through live-action distortion, animation, 3D, Blender/CG, and an impossible world. Never label it as recovered source footage.'),
    generated(byId.get('reality-return')!, 'Hard cut back to source/live action so the character can dismiss the spectacle.'),
    source(byId.get('acid-memory')!, ['OTHER']),
    source(byId.get('acid-search')!, ['OTHER']),
    source(byId.get('lost-acid-button')!, ['OTHER']),
  ];

  const terminal = items[items.length - 1];
  terminal.terminal = true;

  return {
    episodeId: plan.episodeId,
    title: plan.title,
    items,
    rule: 'Physical chronology supplies evidence and timestamps. Editorial order supplies the episode. Generated material must remain explicitly synthetic and purpose-bound.',
  };
}
