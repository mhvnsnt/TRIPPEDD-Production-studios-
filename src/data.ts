import { ProductionRecord } from './types';

export const initialProductionData: ProductionRecord[] = [
  // LUCK OF THE IRISH - Recurring Skit
  {
    id: 'story-02',
    title: 'Luck of the Irish!',
    description: 'A recurring interdimensional-TV style commercial interruption. Boring reality suddenly hijacked by a maniacal cartoon leprechaun screaming "LUCK OF THE IRISH!!!" followed by a green Looney Tunes-style iris wipe and absurd disclaimers for a product that doesn\'t exist.',
    type: 'STORY',
    status: 'IDEA',
    contentType: 'FICTIONAL_CREATION',
    provenance: {
      realityStatus: 'FICTIONAL',
      captureStatus: 'NOT_CAPTURED',
      authorship: 'USER_AUTHORED',
      generationMethods: ['AI_GENERATED', '2D_ANIMATED'],
      assemblyMode: 'PURE_GENERATED',
      aiContributions: ['AI_CO_GENERATED'],
      aggregate: 'FICTIONAL_CREATION'
    },
    verified: 'not_applicable',
    metadata: {
      recurrence: 'OPTIONAL / RANDOM_TRIGGER'
    }
  },
  {
    id: 'char-01',
    title: 'Hood Leprechaun',
    description: 'Little crazy animated evil manic wild wide-eyed wrinkly mad hatter "leprechaun from the hood" cartoon mascot. Green suit, tiny hat, gold teeth. Transforms from live-action character.',
    type: 'CHARACTER',
    status: 'IDEA',
    contentType: 'FICTIONAL_CREATION',
    provenance: {
      realityStatus: 'FICTIONAL',
      captureStatus: 'NOT_CAPTURED',
      authorship: 'USER_AUTHORED',
      generationMethods: ['AI_GENERATED', '2D_ANIMATED'],
      assemblyMode: 'PURE_GENERATED',
      aiContributions: ['AI_CO_GENERATED'],
      aggregate: 'FICTIONAL_CREATION'
    },
    verified: 'not_applicable'
  },
  // A fictional story concept
  {
    id: 'story-01',
    title: 'The Demon Convenience Store',
    description: 'Two idiots accidentally enter a demon-run convenience store.',
    type: 'STORY',
    status: 'IDEA',
    contentType: 'FICTIONAL_CREATION',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'USER_AUTHORED',
      generationMethods: [],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['NONE'],
      aggregate: 'IDEA'
    },
    verified: 'not_applicable'
  },
  // Previous Brainstormed episode 
  {
    id: 'char-joe',
    title: 'Joe',
    description: 'A normal guy. Average build, average clothes. Speaks casually. Inexplicably defies spatial continuity.',
    type: 'CHARACTER',
    status: 'PLANNED',
    contentType: 'FICTIONAL_CREATION',
    provenance: {
      realityStatus: 'FACTUAL',
      captureStatus: 'RECONSTRUCTED',
      authorship: 'USER_AUTHORED',
      generationMethods: ['AI_GENERATED', 'AI_CO_ANIMATED'],
      assemblyMode: 'RECONSTRUCTED_REAL_EVENT',
      aiContributions: ['AI_CO_ANIMATED'],
      aggregate: 'HYBRID_PRODUCTION'
    },
    verified: 'not_applicable'
  },
  {
    id: 'ep-01',
    title: 'Episode 1: Motel / Joe Prayer Scene',
    type: 'EPISODE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'FACTUAL',
      captureStatus: 'PARTIALLY_CAPTURED',
      authorship: 'USER_AUTHORED',
      generationMethods: ['MIXED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_CO_ANIMATED'],
      aggregate: 'HYBRID_PRODUCTION'
    },
    verified: false
  },
  {
    id: 'sc-joe',
    title: 'Scene: Joe Prayer',
    description: 'Mars and Tanesha are sitting outside their motel room. A man named Joe walks past, then inexplicably approaches from the wrong direction, asks for a prayer, offers a Tic Tac, and leaves, breaking spatial reality.',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'FACTUAL',
      captureStatus: 'PARTIALLY_CAPTURED',
      authorship: 'USER_AUTHORED',
      generationMethods: ['LIVE_CAPTURE', 'AI_GENERATED', 'AI_CO_ANIMATED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_CO_ANIMATED'],
      aggregate: 'HYBRID_PRODUCTION'
    },
    verified: false,
    metadata: {
      location: 'UNKNOWN / NEEDS_LOCATION_VERIFICATION'
    }
  },
  {
    id: 'sc-01',
    title: 'Scene 1: The Briefing (Motel 6 Balcony)',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_ASSISTED',
      generationMethods: ['AI_ASSISTED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_ASSISTED'],
      aggregate: 'IDEA'
    },
    verified: false
  },
  {
    id: 'sc-02',
    title: 'Scene 2: The A24 Horror Walk',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_ASSISTED',
      generationMethods: ['AI_ASSISTED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_ASSISTED'],
      aggregate: 'IDEA'
    },
    verified: false
  },
  {
    id: 'sc-03',
    title: 'Scene 3: The Anime Reality Bleed',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_ASSISTED',
      generationMethods: ['AI_ASSISTED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_ASSISTED'],
      aggregate: 'IDEA'
    },
    verified: false
  },
  {
    id: 'sc-04',
    title: 'Scene 4: The Epic UE5 Bricolage',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_ASSISTED',
      generationMethods: ['AI_ASSISTED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_ASSISTED'],
      aggregate: 'IDEA'
    },
    verified: false
  },
  {
    id: 'sc-05',
    title: 'Scene 5: The Deadpan Payoff',
    type: 'SCENE',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_ASSISTED',
      generationMethods: ['AI_ASSISTED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_ASSISTED'],
      aggregate: 'IDEA'
    },
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
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_AUTHORED',
      generationMethods: ['AI_GENERATED'],
      assemblyMode: 'PURE_GENERATED',
      aiContributions: ['AI_CO_GENERATED'],
      aggregate: 'FICTIONAL_CREATION'
    },
    verified: false
  },
  {
    id: 'sh-02',
    title: 'The Dismissal',
    description: 'Tossing wrapper at trash can.',
    type: 'SHOT',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_AUTHORED',
      generationMethods: ['AI_GENERATED'],
      assemblyMode: 'PURE_GENERATED',
      aiContributions: ['AI_CO_GENERATED'],
      aggregate: 'FICTIONAL_CREATION'
    },
    verified: false
  },
  {
    id: 'sh-03',
    title: 'The Call to Action',
    description: '"Whatever. Let\'s go get cigars. We\'re moving."',
    type: 'SHOT',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_AUTHORED',
      generationMethods: ['AI_GENERATED'],
      assemblyMode: 'PURE_GENERATED',
      aiContributions: ['AI_CO_GENERATED'],
      aggregate: 'FICTIONAL_CREATION'
    },
    verified: false
  },
  {
    id: 'sh-04',
    title: 'The Door Swing',
    description: 'Throwing door open into bright daylight.',
    type: 'SHOT',
    status: 'PLANNED',
    contentType: 'PLAN',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_AUTHORED',
      generationMethods: ['AI_GENERATED'],
      assemblyMode: 'PURE_GENERATED',
      aiContributions: ['AI_CO_GENERATED'],
      aggregate: 'FICTIONAL_CREATION'
    },
    verified: false
  },
  {
    id: 'sh-05',
    title: 'Extreme close-up: eyes darting',
    type: 'SHOT',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'USER_AUTHORED',
      generationMethods: [],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['NONE'],
      aggregate: 'IDEA'
    },
    verified: false
  },
  {
    id: 'sh-06',
    title: 'Tight shot: Tyneshia annoyed',
    type: 'SHOT',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'USER_AUTHORED',
      generationMethods: [],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['NONE'],
      aggregate: 'IDEA'
    },
    verified: false
  },
  // Ideas for VFX/Edits
  {
    id: 'vfx-01',
    title: 'Vid2Vid Anime Generation (Gas Station)',
    type: 'VFX',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'USER_AUTHORED',
      generationMethods: [],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['NONE'],
      aggregate: 'IDEA'
    },
    verified: false
  },
  {
    id: 'vfx-02',
    title: 'UE5 Post-apocalyptic wasteland composite',
    type: 'VFX',
    status: 'IDEA',
    contentType: 'IDEA',
    provenance: {
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'USER_AUTHORED',
      generationMethods: [],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['NONE'],
      aggregate: 'IDEA'
    },
    verified: false
  }
];
