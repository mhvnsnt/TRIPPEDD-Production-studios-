import { createEpisodeProvenance } from '../src/server/provenance';

const manifest = createEpisodeProvenance('EP01', 'The Walk', [
  { id: 'source-footage', role: 'PHYSICAL_SOURCE', description: 'Original live-action episode footage.', physicalSourceTruth: true },
  { id: 'editorial', role: 'HUMAN_AUTHORED', description: 'Showrunner story and editorial decisions.', humanDecision: true },
  { id: 'analysis', role: 'AI_ASSISTED', description: 'Transcription and scene-analysis assistance.' },
  { id: 'subjectivity', role: 'GENERATED', description: 'Procedural 3D subjective-state sequence.', generated: true, physicalSourceTruth: false },
]);

if (!manifest.authorship.humanShowrunner || manifest.authorship.finalEditorialAuthority !== 'HUMAN') throw new Error('Human authorship authority was not preserved.');
if (!manifest.disclosureAssessment.containsGeneratedMaterial) throw new Error('Generated material was not detected.');
if (manifest.disclosureAssessment.containsRealisticSyntheticPeopleOrEvents) throw new Error('Non-realistic generated subjectivity was incorrectly classified as realistic synthetic people/events.');
if (manifest.disclosureAssessment.platformDisclosureReviewRequired) throw new Error('Platform review was incorrectly required for this fixture.');

const realistic = createEpisodeProvenance('TEST', 'Synthetic Test', [
  { id: 'synthetic', role: 'GENERATED', description: 'Realistic synthetic person replacing a real person.', generated: true },
]);
if (!realistic.disclosureAssessment.platformDisclosureReviewRequired) throw new Error('Realistic synthetic material did not trigger platform review.');

console.log('Provenance test passed.');
