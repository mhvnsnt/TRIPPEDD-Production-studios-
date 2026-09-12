export type StudioMedium =
  | 'LIVE_ACTION'
  | 'ANIMATION_2D'
  | 'ANIMATION_3D'
  | 'BLENDER_CG'
  | 'GENERATED_VIDEO'
  | 'FAKE_COMMERCIAL'
  | 'FAKE_TV'
  | 'PUBLIC_ACCESS'
  | 'FOUND_OR_ARCHIVAL'
  | 'MONTAGE'
  | 'INTERSTITIAL';

export type AudienceMechanism =
  | 'COMFORT_TO_VIOLATION'
  | 'LOGIC_TO_CONTRADICTION'
  | 'OBJECT_TO_SYMBOL'
  | 'REALITY_TO_SUBJECTIVITY'
  | 'MEANING_OVERLOAD_TO_BUTTON'
  | 'CALLBACK'
  | 'MISDIRECTION'
  | 'ANTICLIMAX'
  | 'AMBIGUITY';

export interface StudioBible {
  studioId: 'TRIPPEDD';
  mission: string;
  identity: string[];
  inspirations: string[];
  episodeGrammar: string[];
  psychologicalGrammar: string[];
  allowedMediums: StudioMedium[];
  audienceMechanisms: AudienceMechanism[];
  productionRules: string[];
  sourceTruthRules: string[];
  autonomyRules: string[];
}

/** The machine-readable creative constitution used by autonomous production workers. */
export const TRIPPEDD_STUDIO_BIBLE: StudioBible = {
  studioId: 'TRIPPEDD',
  mission: 'Produce an authored, surreal, psychologically active comedy series with a one-person human production team and an autonomous AI production staff.',
  identity: [
    'Performance before polish.',
    'The AI is a production instrument, not the aesthetic.',
    'Make the audience participate instead of merely showing them something weird.',
    'Preserve accidental comedy, dead air, awkwardness, and human imperfection when they strengthen the piece.',
    'Abrupt changes in production language are allowed when they communicate subjective experience or editorial intent.',
  ],
  inspirations: [
    'Adult Swim experimental and sketch programming',
    'Off the Air',
    'Xavier: Renegade Angel',
    '12 oz. Mouse',
    'Monty Python',
    'Cheech & Chong',
    'Key & Peele',
    'MADtv',
    'Robot Chicken',
    'Trailer Park Boys',
    'Shameless',
    'Clerks / Jay & Silent Bob',
    'Workaholics',
  ],
  episodeGrammar: [
    'COLD_OPEN',
    'REALITY_ANCHOR',
    'ESCALATION',
    'FORMAT_SHIFT',
    'CALLBACK',
    'PRESSURE_COOKER',
    'SURREAL_RELEASE',
    'BUTTON',
  ],
  psychologicalGrammar: [
    'NORMALITY -> PATTERN -> WRONG_DETAIL -> ESCALATION -> ASSOCIATION -> REALITY_SLIP -> RETURN -> DENIAL -> BUTTON',
    'MUNDANE -> PHILOSOPHICAL_QUESTION -> STUPID_ANSWER -> CONSEQUENCE',
    'REAL_EVENT -> SUBJECTIVE_WORLD -> EXTREME_VISUALIZATION -> MUNDANE_CHARACTER_RESPONSE',
    'ARGUMENT -> NON_SEQUITUR -> NEW_WORLD_RULE -> COMMITMENT -> COLLAPSE',
  ],
  allowedMediums: [
    'LIVE_ACTION', 'ANIMATION_2D', 'ANIMATION_3D', 'BLENDER_CG', 'GENERATED_VIDEO',
    'FAKE_COMMERCIAL', 'FAKE_TV', 'PUBLIC_ACCESS', 'FOUND_OR_ARCHIVAL', 'MONTAGE', 'INTERSTITIAL',
  ],
  audienceMechanisms: [
    'COMFORT_TO_VIOLATION',
    'LOGIC_TO_CONTRADICTION',
    'OBJECT_TO_SYMBOL',
    'REALITY_TO_SUBJECTIVITY',
    'MEANING_OVERLOAD_TO_BUTTON',
    'CALLBACK',
    'MISDIRECTION',
    'ANTICLIMAX',
    'AMBIGUITY',
  ],
  productionRules: [
    'Every generated shot must have an editorial purpose.',
    'Choose the medium because it serves the story, not because the tool is impressive.',
    'Use sound, silence, texture, pacing, graphics, and format changes as authored language.',
    'Do not flatten every episode into one visual treatment.',
    'Keep reusable locations, props, characters, sounds, phrases, and gags linkable across episodes.',
    'Automate repetitive work; preserve human authority over final creative judgment.',
  ],
  sourceTruthRules: [
    'Physical source chronology is authoritative about what physically happened.',
    'Editorial chronology may rearrange or construct material but must retain provenance.',
    'Generated material must never be inserted into the physical timeline as captured fact.',
    'Subjective sequences may be spectacular while the character denies or minimizes them.',
    'Never solve an intentional terminal anticlimax unless the editorial plan explicitly requires it.',
  ],
  autonomyRules: [
    'Ingest, analysis, transcription, shot detection, comedy discovery, asset preparation, rough assembly, and technical QC may execute automatically.',
    'Generated-production workers may create reversible drafts with explicit provenance.',
    'The system may iterate rough cuts automatically when new evidence arrives.',
    'Editorial lock, final QC acceptance, and showrunner greenlight remain human-controlled.',
  ],
};
