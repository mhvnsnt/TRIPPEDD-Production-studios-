import { TRIPPEDD_STUDIO_BIBLE, type StudioMedium } from './studioBible';

export type ProductionStage =
  | 'INGEST'
  | 'PHYSICAL_TIMELINE'
  | 'MEDIA_ANALYSIS'
  | 'COMEDY_DISCOVERY'
  | 'STORY_DEVELOPMENT'
  | 'FORMAT_PLANNING'
  | 'GENERATED_PRODUCTION'
  | 'ROUGH_ASSEMBLY'
  | 'SOUND_POST'
  | 'COLOR_VFX'
  | 'TECHNICAL_QC'
  | 'EDITORIAL_REVIEW'
  | 'EDITORIAL_LOCK'
  | 'SHOWRUNNER_GREENLIGHT'
  | 'DELIVERY';

export type AutonomyMode = 'AUTO' | 'AUTO_UNTIL_REVIEW' | 'HUMAN_GATE';

export interface ProductionStageDefinition {
  id: ProductionStage;
  name: string;
  autonomy: AutonomyMode;
  dependsOn: ProductionStage[];
  parallelGroup?: string;
  outputs: string[];
  purpose: string;
}

export interface GeneratedUnitPlan {
  id: string;
  medium: StudioMedium;
  editorialPurpose: string;
  sourceAnchors: string[];
  requiredAssets: string[];
  forbiddenClaims: string[];
  autonomy: AutonomyMode;
}

export const TRIPPEDD_PRODUCTION_PIPELINE: ProductionStageDefinition[] = [
  { id: 'INGEST', name: 'Ingest & Preserve', autonomy: 'AUTO', dependsOn: [], outputs: ['source_media', 'source_identity', 'provenance'], purpose: 'Register original media without altering source truth.' },
  { id: 'PHYSICAL_TIMELINE', name: 'Physical Source Timeline', autonomy: 'AUTO_UNTIL_REVIEW', dependsOn: ['INGEST'], outputs: ['events', 'dialogue', 'visual_observations', 'chronology_evidence'], purpose: 'Establish what physically happened before editorial interpretation.' },
  { id: 'MEDIA_ANALYSIS', name: 'Media Intelligence', autonomy: 'AUTO', dependsOn: ['INGEST'], parallelGroup: 'analysis', outputs: ['technical_metadata', 'shots', 'transcript', 'ocr', 'visual_samples'], purpose: 'Extract machine-readable evidence using open-source tools.' },
  { id: 'COMEDY_DISCOVERY', name: 'Comedy Discovery', autonomy: 'AUTO', dependsOn: ['MEDIA_ANALYSIS', 'PHYSICAL_TIMELINE'], outputs: ['gag_candidates', 'callbacks', 'subjectivity_signals', 'buttons'], purpose: 'Find comedy without changing the underlying evidence.' },
  { id: 'STORY_DEVELOPMENT', name: 'Story Department', autonomy: 'AUTO_UNTIL_REVIEW', dependsOn: ['COMEDY_DISCOVERY'], outputs: ['segment_candidates', 'episode_beats'], purpose: 'Convert evidence into reversible editorial possibilities.' },
  { id: 'FORMAT_PLANNING', name: 'Format Department', autonomy: 'AUTO', dependsOn: ['STORY_DEVELOPMENT'], outputs: ['medium_assignments', 'shot_plans', 'format_shifts'], purpose: 'Choose live action, animation, Blender, fake TV, commercials, bumpers, or hybrid treatment per beat.' },
  { id: 'GENERATED_PRODUCTION', name: 'Generated Production', autonomy: 'AUTO_UNTIL_REVIEW', dependsOn: ['FORMAT_PLANNING'], outputs: ['generated_video', 'blender_scenes', 'graphics', 'interstitials', 'assets'], purpose: 'Create missing bridges and subjective material with explicit provenance.' },
  { id: 'ROUGH_ASSEMBLY', name: 'Autonomous Editorial', autonomy: 'AUTO_UNTIL_REVIEW', dependsOn: ['STORY_DEVELOPMENT', 'GENERATED_PRODUCTION'], outputs: ['rough_cut', 'otio_timeline', 'edit_manifest'], purpose: 'Continuously assemble the best current cut while retaining source traceability.' },
  { id: 'SOUND_POST', name: 'Sound Department', autonomy: 'AUTO_UNTIL_REVIEW', dependsOn: ['ROUGH_ASSEMBLY'], outputs: ['mix', 'room_tones', 'sfx', 'music_maps'], purpose: 'Treat sound, silence, texture, and transitions as authored production language.' },
  { id: 'COLOR_VFX', name: 'Finishing Department', autonomy: 'AUTO_UNTIL_REVIEW', dependsOn: ['ROUGH_ASSEMBLY'], outputs: ['color_pass', 'vfx_pass', 'graphics_pass'], purpose: 'Finish the picture without erasing the accidental texture that makes the show human.' },
  { id: 'TECHNICAL_QC', name: 'Technical QC', autonomy: 'AUTO', dependsOn: ['SOUND_POST', 'COLOR_VFX'], outputs: ['qc_report'], purpose: 'Detect decode errors, missing media, bad audio, broken provenance, and delivery defects.' },
  { id: 'EDITORIAL_REVIEW', name: 'Editorial Review', autonomy: 'HUMAN_GATE', dependsOn: ['TECHNICAL_QC'], outputs: ['editorial_notes', 'approved_changes'], purpose: 'Human review of the actual watchable cut.' },
  { id: 'EDITORIAL_LOCK', name: 'Editorial Lock', autonomy: 'HUMAN_GATE', dependsOn: ['EDITORIAL_REVIEW'], outputs: ['locked_timeline'], purpose: 'Freeze the intended sequence and approved generated material.' },
  { id: 'SHOWRUNNER_GREENLIGHT', name: 'Showrunner Greenlight', autonomy: 'HUMAN_GATE', dependsOn: ['EDITORIAL_LOCK'], outputs: ['greenlight'], purpose: 'Final creative authority remains with the showrunner.' },
  { id: 'DELIVERY', name: 'Delivery', autonomy: 'HUMAN_GATE', dependsOn: ['SHOWRUNNER_GREENLIGHT'], outputs: ['master', 'archive', 'metadata'], purpose: 'Produce the final master only after explicit approval.' },
];

export function validateGeneratedUnit(unit: GeneratedUnitPlan): string[] {
  const errors: string[] = [];
  if (!unit.editorialPurpose.trim()) errors.push('Generated unit requires an editorial purpose.');
  if (!unit.sourceAnchors.length) errors.push('Generated unit requires at least one source or story anchor.');
  if (!unit.forbiddenClaims.length) errors.push('Generated unit must declare forbidden physical-source claims.');
  if (!TRIPPEDD_STUDIO_BIBLE.allowedMediums.includes(unit.medium)) errors.push(`Unsupported TRIPPEDD medium: ${unit.medium}`);
  return errors;
}
