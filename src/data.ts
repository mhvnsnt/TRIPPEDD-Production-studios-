import { ProductionRecord } from './types';

export const initialProductionData: ProductionRecord[] = [
  // A fictional story concept
  {
    id: 'story-01',
    title: 'The Demon Convenience Store',
    description: 'Two idiots accidentally enter a demon-run convenience store.',
    type: 'STORY',
    status: 'IDEA',
    contentType: 'FICTIONAL_CREATION',
    provenance: 'USER_CREATED',
    verified: 'not_applicable'
  },
  // Previous Brainstormed episode 
  {
    id: 'ep-01',
    title: 'Episode 01: The Walk',
    type: 'EPISODE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'USER_CREATED',
    verified: false
  },
  {
    id: 'sc-01',
    title: 'Scene 1: The Briefing (Motel 6 Balcony)',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_ASSISTED',
    verified: false
  },
  {
    id: 'sc-02',
    title: 'Scene 2: The A24 Horror Walk',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_ASSISTED',
    verified: false
  },
  {
    id: 'sc-03',
    title: 'Scene 3: The Anime Reality Bleed',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_ASSISTED',
    verified: false
  },
  {
    id: 'sc-04',
    title: 'Scene 4: The Epic UE5 Bricolage',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_ASSISTED',
    verified: false
  },
  {
    id: 'sc-05',
    title: 'Scene 5: The Deadpan Payoff',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_ASSISTED',
    verified: false
  },
  // Shots based on brainstorming
  {
    id: 'sh-01',
    title: 'The Wrapper (Close Up)',
    description: 'Raw phone footage inside Motel 6 room. Squeezing last crumb.',
    type: 'SHOT',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_GENERATED',
    verified: false
  },
  {
    id: 'sh-02',
    title: 'The Dismissal',
    description: 'Tossing wrapper at trash can.',
    type: 'SHOT',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_GENERATED',
    verified: false
  },
  {
    id: 'sh-03',
    title: 'The Call to Action',
    description: '"Whatever. Let\'s go get cigars. We\'re moving."',
    type: 'SHOT',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_GENERATED',
    verified: false
  },
  {
    id: 'sh-04',
    title: 'The Door Swing',
    description: 'Throwing door open into bright daylight.',
    type: 'SHOT',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: 'AI_GENERATED',
    verified: false
  },
  {
    id: 'sh-05',
    title: 'Extreme close-up: eyes darting',
    type: 'SHOT',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: 'USER_CREATED',
    verified: false
  },
  {
    id: 'sh-06',
    title: 'Tight shot: Tyneshia annoyed',
    type: 'SHOT',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: 'USER_CREATED',
    verified: false
  },
  // Ideas for VFX/Edits
  {
    id: 'vfx-01',
    title: 'Vid2Vid Anime Generation (Gas Station)',
    type: 'VFX',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: 'USER_CREATED',
    verified: false
  },
  {
    id: 'vfx-02',
    title: 'UE5 Post-apocalyptic wasteland composite',
    type: 'VFX',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: 'USER_CREATED',
    verified: false
  }
];
