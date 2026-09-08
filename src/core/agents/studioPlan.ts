import { AutonomousStudioOrchestrator, ProductionWorkItem } from './orchestrator';

export interface SourceProductionPlan {
  sourceId: string;
  work: ProductionWorkItem[];
}

/**
 * Builds the default autonomous path for a newly ingested source clip.
 * The plan is intentionally reversible: analysis can run without changing
 * source truth, while editorial and delivery remain gated.
 */
export function planSourceClip(studio: AutonomousStudioOrchestrator, sourceId: string, label: string): SourceProductionPlan {
  const ingest = studio.addWork({
    kind: 'INGEST',
    title: `Register source: ${label}`,
    description: 'Preserve the original media identity, hash, Drive reference, and provenance.',
    dependencies: [],
    requiredCapabilities: ['READ_SOURCE'],
    requiresHumanApproval: false,
    sourceRefs: [sourceId],
    outputRefs: [],
  });

  const analysis = studio.addWork({
    kind: 'MEDIA_ANALYSIS',
    title: `Analyze source: ${label}`,
    description: 'Run technical metadata, shot detection, audio/transcript, frame sampling, and visual evidence extraction.',
    dependencies: [ingest.id],
    requiredCapabilities: ['READ_SOURCE', 'ANALYZE_MEDIA'],
    requiresHumanApproval: false,
    sourceRefs: [sourceId],
    outputRefs: [],
  });

  const gags = studio.addWork({
    kind: 'GAG_DISCOVERY',
    title: `Find comedy: ${label}`,
    description: 'Score escalation, reactions, awkwardness, interruptions, visual jokes, accidental comedy, and callback potential.',
    dependencies: [analysis.id],
    requiredCapabilities: ['DISCOVER_GAGS'],
    requiresHumanApproval: false,
    sourceRefs: [sourceId, analysis.id],
    outputRefs: [],
  });

  const story = studio.addWork({
    kind: 'STORY_DEVELOPMENT',
    title: `Develop segment candidates: ${label}`,
    description: 'Turn confirmed evidence and comedy candidates into reversible segment concepts using TRIPPEDD format grammar.',
    dependencies: [gags.id],
    requiredCapabilities: ['DRAFT_STORY'],
    requiresHumanApproval: true,
    sourceRefs: [sourceId, gags.id],
    outputRefs: [],
  });

  const assembly = studio.addWork({
    kind: 'EDITORIAL_ASSEMBLY',
    title: `Build editorial assembly: ${label}`,
    description: 'Construct a source-traceable assembly from approved segment candidates without modifying source media.',
    dependencies: [story.id],
    requiredCapabilities: ['EDIT_ASSEMBLY'],
    requiresHumanApproval: true,
    sourceRefs: [sourceId, story.id],
    outputRefs: [],
  });

  const qc = studio.addWork({
    kind: 'QC',
    title: `QC assembly: ${label}`,
    description: 'Validate media completeness, provenance, continuity, technical integrity, and unresolved editorial risks.',
    dependencies: [assembly.id],
    requiredCapabilities: ['RUN_QC'],
    requiresHumanApproval: false,
    sourceRefs: [sourceId, assembly.id],
    outputRefs: [],
  });

  const delivery = studio.addWork({
    kind: 'DELIVERY',
    title: `Prepare delivery: ${label}`,
    description: 'Prepare a final delivery package only after QC passes and the showrunner explicitly greenlights release.',
    dependencies: [qc.id],
    requiredCapabilities: ['PUBLISH_INTERNAL'],
    requiresHumanApproval: true,
    sourceRefs: [sourceId, qc.id],
    outputRefs: [],
  });

  return { sourceId, work: [ingest, analysis, gags, story, assembly, qc, delivery] };
}
