import { describe, expect, it } from 'vitest';
import { AutonomousStudioOrchestrator } from '../orchestrator';

describe('AutonomousStudioOrchestrator', () => {
  it('builds a dependency-aware production queue', () => {
    const studio = new AutonomousStudioOrchestrator();
    const ingest = studio.addWork({
      kind: 'INGEST',
      title: 'Ingest source media',
      description: 'Register source media and preserve provenance.',
      dependencies: [],
      requiredCapabilities: ['READ_SOURCE'],
      requiresHumanApproval: false,
      sourceRefs: [],
      outputRefs: [],
    });
    const analysis = studio.addWork({
      kind: 'MEDIA_ANALYSIS',
      title: 'Analyze source',
      description: 'Run technical, visual, audio, and transcript analysis.',
      dependencies: [ingest.id],
      requiredCapabilities: ['READ_SOURCE', 'ANALYZE_MEDIA'],
      requiresHumanApproval: false,
      sourceRefs: [ingest.id],
      outputRefs: [],
    });

    expect(ingest.status).toBe('READY');
    expect(analysis.status).toBe('BLOCKED');
    studio.complete(ingest.id, ['source:clip-001']);
    expect(studio.getReadyWork().map(item => item.id)).toContain(analysis.id);
  });

  it('keeps delivery behind a human gate', () => {
    const studio = new AutonomousStudioOrchestrator();
    const delivery = studio.addWork({
      kind: 'DELIVERY',
      title: 'Deliver episode',
      description: 'Prepare final delivery package.',
      dependencies: [],
      requiredCapabilities: ['PUBLISH_INTERNAL'],
      requiresHumanApproval: false,
      sourceRefs: [],
      outputRefs: [],
    });

    const decision = studio.decide('production-manager', delivery.id);
    expect(decision.allowed).toBe(true);
    expect(decision.requiresHumanApproval).toBe(true);
    expect(decision.reason).toContain('human review gate');
  });
});
