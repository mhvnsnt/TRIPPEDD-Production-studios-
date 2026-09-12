import { EP01_LOST_ACID_SUBJECTIVITY } from './subjectivityRule';

export type PilotBeatKind =
  | 'COLD_OPEN'
  | 'REALITY_ANCHOR'
  | 'ESCALATION'
  | 'FORMAT_SHIFT'
  | 'CALLBACK'
  | 'PRESSURE_COOKER'
  | 'SURREAL_RELEASE'
  | 'BUTTON';

export interface PilotBeat {
  id: string;
  title: string;
  kind: PilotBeatKind;
  purpose: string;
  sourceTruthRequired: boolean;
  generatedMaterialAllowed: boolean;
  humanApprovalRequired: boolean;
}

export interface PilotEpisodePlan {
  episodeId: string;
  title: string;
  sourceStory: string;
  formatId: string;
  grammar: PilotBeatKind[];
  beats: PilotBeat[];
  subjectivitySequenceId: string;
  terminalBeatId: string;
  neverDo: string[];
}

const beat = (
  id: string,
  title: string,
  kind: PilotBeatKind,
  purpose: string,
  options: Partial<Pick<PilotBeat, 'sourceTruthRequired' | 'generatedMaterialAllowed' | 'humanApprovalRequired'>> = {},
): PilotBeat => ({
  id,
  title,
  kind,
  purpose,
  sourceTruthRequired: options.sourceTruthRequired ?? true,
  generatedMaterialAllowed: options.generatedMaterialAllowed ?? false,
  humanApprovalRequired: options.humanApprovalRequired ?? false,
});

/** Canonical production plan for the actual EP01 pilot, The Walk. */
export function createEp01PilotPlan(): PilotEpisodePlan {
  return {
    episodeId: 'EP01',
    title: 'The Walk',
    sourceStory:
      'A real motel hangout grows into a cigar run, interruptions, encounters, and an attempted altered-state experience that ultimately collapses into the character losing the acid he bought.',
    formatId: 'HYBRID',
    grammar: [
      'COLD_OPEN',
      'REALITY_ANCHOR',
      'ESCALATION',
      'FORMAT_SHIFT',
      'CALLBACK',
      'PRESSURE_COOKER',
      'SURREAL_RELEASE',
      'BUTTON',
    ],
    subjectivitySequenceId: EP01_LOST_ACID_SUBJECTIVITY.id,
    terminalBeatId: 'lost-acid-button',
    beats: [
      beat('motel-reality', 'Motel Reality', 'REALITY_ANCHOR', 'Establish the actual people, motel environment, chemistry, and accidental comedy in the source footage.'),
      beat('shumafied-item', 'The Shumafied Item', 'ESCALATION', 'Seed the altered-state expectation and make the object/idea recur as a real production thread.'),
      beat('cigar-run', 'Decision to Get Cigars', 'ESCALATION', 'Let the ordinary errand become the engine for the episode.'),
      beat('walk-and-bag', 'The Walk / Bag Incident', 'PRESSURE_COOKER', 'Preserve interruptions, argument, awkward pauses, and physical business from the real chronology.'),
      beat('joe-and-goodville', 'Joe / Goodville Material', 'CALLBACK', 'Use the strongest real interactions and recurring language as editorial callbacks without pretending they happened in a different order.'),
      beat('shumafied-subjective-shift', 'The Shumafied Experience', 'FORMAT_SHIFT', 'Move from live action into distortion, animation, 3D/Blender/CG, and an impossible subjective world because the audience is seeing the character\'s experience.', { generatedMaterialAllowed: true, humanApprovalRequired: true }),
      beat('reality-return', 'That Wasn\'t Even Shit', 'SURREAL_RELEASE', 'Return abruptly to ordinary live action. The character dismisses the enormous subjective sequence as insignificant.', { generatedMaterialAllowed: true }),
      beat('acid-memory', 'Oh Yeah, I Got the Acid', 'CALLBACK', 'Trigger the final hope: the character remembers the roughly $30 worth of acid he bought, about two and a half double hits of yellow gel tabs.', { humanApprovalRequired: true }),
      beat('acid-search', 'Where the Fuck Is It?', 'PRESSURE_COOKER', 'Build a frantic but mundane search. Do not invent a resolution to the disappearance.', { humanApprovalRequired: true }),
      beat('lost-acid-button', 'The Lost Acid', 'BUTTON', 'He cannot find it, becomes genuinely sad, and the episode ends because he never got to trip.', { humanApprovalRequired: true }),
    ],
    neverDo: [
      'Do not rewrite physical chronology as though it were the editorial order.',
      'Do not present generated material as recovered real footage.',
      'Do not explain or solve the disappearance of the acid.',
      'Do not add a post-button scene.',
      'Do not use spectacle without a subjective-story reason.',
    ],
  };
}
