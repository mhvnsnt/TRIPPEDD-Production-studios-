export interface PilotEndingBeat {
  id: string;
  title: string;
  purpose: string;
  sourceTruthRequired: boolean;
  generatedMaterialAllowed: boolean;
}

export interface PilotEndingPlan {
  episodeId: string;
  formatId: string;
  beats: PilotEndingBeat[];
  terminalBeatId: string;
  editorialRule: string;
}

/**
 * Canonical editorial plan for the EP01 lost-acid button.
 * Physical evidence is never rewritten by this plan; it only describes the
 * intended editorial ending assembled from evidence and/or clearly-labelled
 * reconstructed material.
 */
export function createPilotLostAcidEnding(): PilotEndingPlan {
  return {
    episodeId: 'EP01',
    formatId: 'LIVE_SKETCH',
    beats: [
      { id: 'lost-acid-false-salvation', title: 'False Salvation', purpose: 'The failed shroomified plan makes the day feel like a bust.', sourceTruthRequired: true, generatedMaterialAllowed: false },
      { id: 'lost-acid-memory', title: 'The Acid Memory', purpose: 'The protagonist remembers the acid and briefly believes the day can be salvaged.', sourceTruthRequired: false, generatedMaterialAllowed: true },
      { id: 'lost-acid-search', title: 'The Search', purpose: 'A frantic search escalates the tiny problem into the final crisis.', sourceTruthRequired: false, generatedMaterialAllowed: true },
      { id: 'lost-acid-deflation', title: 'The Deflation', purpose: 'The energy collapses when the acid cannot be found.', sourceTruthRequired: false, generatedMaterialAllowed: true },
      { id: 'lost-acid-button', title: 'Lost Acid Button', purpose: 'End on the disproportionate sadness of never getting to trip after the entire day.', sourceTruthRequired: false, generatedMaterialAllowed: true },
    ],
    terminalBeatId: 'lost-acid-button',
    editorialRule: 'Do not solve the disappearance. The disappearance itself is the punchline, and nothing follows the terminal button.',
  };
}
