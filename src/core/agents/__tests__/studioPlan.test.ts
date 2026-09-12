import { describe, expect, it } from 'vitest';
import { AutonomousStudioOrchestrator } from '../orchestrator';
import { planSourceClip } from '../studioPlan';

describe('planSourceClip', () => {
  it('creates a complete source-to-delivery chain with explicit gates', () => {
    const studio = new AutonomousStudioOrchestrator();
    const plan = planSourceClip(studio, 'drive:file-001', 'camera_001.mp4');

    expect(plan.work).toHaveLength(7);
    expect(plan.work.map(item => item.kind)).toEqual([
      'INGEST',
      'MEDIA_ANALYSIS',
      'GAG_DISCOVERY',
      'STORY_DEVELOPMENT',
      'EDITORIAL_ASSEMBLY',
      'QC',
      'DELIVERY',
    ]);
    expect(plan.work[0].status).toBe('READY');
    expect(plan.work.slice(1).every(item => item.status === 'BLOCKED')).toBe(true);
    expect(plan.work[3].requiresHumanApproval).toBe(true);
    expect(plan.work[4].requiresHumanApproval).toBe(true);
    expect(plan.work[6].requiresHumanApproval).toBe(true);
  });
});
