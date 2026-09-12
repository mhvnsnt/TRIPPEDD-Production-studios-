export type ProvenanceRole = 'HUMAN_AUTHORED' | 'AI_ASSISTED' | 'GENERATED' | 'PHYSICAL_SOURCE' | 'EDITORIAL_ASSEMBLY';

export interface ProvenanceItem {
  id: string;
  role: ProvenanceRole;
  description: string;
  source?: string;
  generated?: boolean;
  physicalSourceTruth?: boolean;
  humanDecision?: boolean;
  notes?: string;
}

export interface EpisodeProvenanceManifest {
  schemaVersion: 1;
  episodeId: string;
  title: string;
  authorship: {
    humanShowrunner: true;
    finalEditorialAuthority: 'HUMAN';
  };
  items: ProvenanceItem[];
  disclosureAssessment: {
    containsGeneratedMaterial: boolean;
    containsRealisticSyntheticPeopleOrEvents: boolean;
    containsMeaningfulSyntheticAlteration: boolean;
    platformDisclosureReviewRequired: boolean;
    assessmentBasis: string;
  };
}

export function createEpisodeProvenance(
  episodeId: string,
  title: string,
  items: ProvenanceItem[],
): EpisodeProvenanceManifest {
  const containsGeneratedMaterial = items.some(item => item.role === 'GENERATED' || item.generated === true);
  const containsRealisticSyntheticPeopleOrEvents = items.some(
    item => item.role === 'GENERATED' && /realistic|synthetic (person|people|event)|deepfake/i.test(item.notes || item.description),
  );
  const containsMeaningfulSyntheticAlteration = items.some(
    item => item.role === 'GENERATED' && /alter(ed|ation)|replace|fabricat|synthetic/i.test(item.notes || item.description),
  );

  return {
    schemaVersion: 1,
    episodeId,
    title,
    authorship: { humanShowrunner: true, finalEditorialAuthority: 'HUMAN' },
    items,
    disclosureAssessment: {
      containsGeneratedMaterial,
      containsRealisticSyntheticPeopleOrEvents,
      containsMeaningfulSyntheticAlteration,
      platformDisclosureReviewRequired: containsRealisticSyntheticPeopleOrEvents || containsMeaningfulSyntheticAlteration,
      assessmentBasis: 'This is a production-provenance assessment, not a platform-policy verdict. Review the destination platform rules for the specific delivered work.',
    },
  };
}
