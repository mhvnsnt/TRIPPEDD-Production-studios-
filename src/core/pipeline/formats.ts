import { ProductionFormat, LocationRecord } from '../types';

export class FormatRegistry {
  private static formats = new Map<string, ProductionFormat>();
  private static locations = new Map<string, LocationRecord>();

  static registerFormat(format: ProductionFormat) {
    this.formats.set(format.id, format);
  }

  static getFormat(id: string): ProductionFormat | undefined {
    return this.formats.get(id);
  }

  static getAllFormats(): ProductionFormat[] {
    return Array.from(this.formats.values());
  }

  static registerLocation(location: LocationRecord) {
    this.locations.set(location.id, location);
  }

  static getLocation(id: string): LocationRecord | undefined {
    return this.locations.get(id);
  }

  static getAllLocations(): LocationRecord[] {
    return Array.from(this.locations.values());
  }
}

// Register default formats
FormatRegistry.registerFormat({
  id: 'TRIPPEDD_ADULT_ANIMATION_PARODY',
  name: 'TRIPPEDD Cutout Comedy 2D',
  description: 'Adult animation parody invoking flat, cutout 2D style. Must use original characters, locations, and lore.',
  ipMode: 'PARODY',
  guidelines: [
    '2D cutout-inspired animation with deliberately limited movement',
    'Exaggerated facial poses and deadpan staging',
    'Fast comedic timing with sudden absurd escalation',
    'MUST use proprietary character construction, proportions, and facial system',
    'NEVER use copied character designs, dialogue, or music from existing properties'
  ],
  defaultProvenance: {
    realityStatus: 'FICTIONAL',
    captureStatus: 'NOT_CAPTURED',
    authorship: 'COLLABORATIVE_AUTHORED',
    generationMethods: ['AI_ASSISTED', 'AI_GENERATED', '2D_ANIMATED'],
    assemblyMode: 'MULTI_ENGINE_HYBRID',
    aiContributions: ['AI_CO_GENERATED', 'AI_CO_ANIMATED'],
    aggregate: 'FICTIONAL_CREATION'
  }
});

FormatRegistry.registerFormat({
  id: 'REAL_EVENT_RECONSTRUCTION',
  name: 'Real Event Reconstruction',
  description: 'Reconstruction of factual events where some visual or audio material is missing or generated.',
  ipMode: 'DOCUMENTARY',
  guidelines: [
    'Use real performances when available to drive timing and blocking',
    'Clearly label generated aspects of the shot',
    'Preserve the original context and dialogue of the factual event'
  ],
  defaultProvenance: {
    realityStatus: 'FACTUAL',
    captureStatus: 'PARTIALLY_CAPTURED',
    authorship: 'USER_AUTHORED',
    generationMethods: ['MIXED'],
    assemblyMode: 'RECONSTRUCTED_REAL_EVENT',
    aiContributions: ['AI_CO_GENERATED', 'AI_CO_ANIMATED'],
    aggregate: 'HYBRID_PRODUCTION'
  }
});

// Register locations
FormatRegistry.registerLocation({
  id: 'GOODVILLE_TN',
  name: 'Goodville, Tennessee',
  type: 'FICTIONALIZED_REALITY',
  description: 'A fictional Tennessee town occupying the cultural space of the Nashville/Madison/Goodlettsville corridor.',
  metadata: {
    geographyRule: 'The distance between Goodville and Nashville is whatever the character currently believes it to be. 45 minutes, 5 minutes, or an hour and a half.',
    visualLanguage: 'Utility poles, construction everywhere, old houses mixed with new, motels, fast food, pawn shops.'
  }
});
