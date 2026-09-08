export type TRIPPEDDFormatCode =
  | 'LIVE_SKETCH'
  | 'MOCKUMENTARY'
  | 'SITCOM_SCENE'
  | 'STREET_OR_REALITY'
  | 'ANIMATED_SKETCH'
  | 'STOP_MOTION_OR_PUPPET'
  | 'FAKE_COMMERCIAL'
  | 'FAKE_TV_OR_MEDIA'
  | 'MUSIC_VIDEO_OR_MUSICAL_BIT'
  | 'INTERVIEW'
  | 'NARRATED_BIT'
  | 'MONTAGE'
  | 'COLD_OPEN'
  | 'TRANSITION_GAG'
  | 'RECURRING_GAG'
  | 'OUTTAKE_OR_META'
  | 'HYBRID';

export interface FormatProfile {
  id: string;
  name: string;
  description: string;
  formats: TRIPPEDDFormatCode[];
  references: string[];
  editorialRules: string[];
  defaultFlow: string[];
}

export const TRIPPEDD_FORMAT_PROFILE: FormatProfile = {
  id: 'trippedd-comedy-anthology-v1',
  name: 'TRIPPEDD',
  description: 'Genre-fluid comedy built from grounded performances, escalating absurdity, sketch structures, media collisions, recurring callbacks, and deliberate format shifts.',
  formats: [
    'LIVE_SKETCH', 'MOCKUMENTARY', 'SITCOM_SCENE', 'STREET_OR_REALITY',
    'ANIMATED_SKETCH', 'STOP_MOTION_OR_PUPPET', 'FAKE_COMMERCIAL',
    'FAKE_TV_OR_MEDIA', 'MUSIC_VIDEO_OR_MUSICAL_BIT', 'INTERVIEW',
    'NARRATED_BIT', 'MONTAGE', 'COLD_OPEN', 'TRANSITION_GAG',
    'RECURRING_GAG', 'OUTTAKE_OR_META', 'HYBRID'
  ],
  references: [
    '12 oz. Mouse',
    'Monty Python',
    'Cheech & Chong',
    'Key & Peele',
    'MADtv',
    'Robot Chicken',
    'Trailer Park Boys',
    'Shameless',
    'Clerks / Jay & Silent Bob',
    'Workaholics'
  ],
  editorialRules: [
    'Performance before polish.',
    'Physical source chronology is authoritative about what happened; editorial chronology describes the constructed show.',
    'Preserve accidental comedy and useful awkwardness as reviewable material.',
    'Treat callbacks, props, phrases, characters, locations, and sounds as linkable production objects.',
    'Permit abrupt format changes without losing provenance.',
    'Never overwrite source evidence with an editorial interpretation.',
    'Human review controls final editorial selection.'
  ],
  defaultFlow: [
    'COLD_OPEN',
    'REALITY_ANCHOR',
    'ESCALATION',
    'FORMAT_SHIFT',
    'CALLBACK',
    'PRESSURE_COOKER',
    'SURREAL_RELEASE',
    'BUTTON'
  ]
};
