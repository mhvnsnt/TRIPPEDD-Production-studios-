/**
 * The production graph must agree with the locked blueprint, and must not
 * quietly drop what nobody has built yet.
 */
import { describe, it, expect } from 'vitest';
import { reconcileEpisode01, plannedSegment, canonToProvenance } from '../episode01Reconcile';
import { EpisodeRegistry, EP01_RECONCILIATION, EP01_AUTHORED_SEGMENTS } from '../episodes';
import { EPISODE_01, lockedOrder } from '../../canon/episode01';
import type { Segment } from '../../types';

const ep01 = () => EpisodeRegistry.getEpisode('EP01')!;

describe('EP01 production graph — reconciled against canon', () => {
  it('carries every locked canon segment', () => {
    const present = new Set(ep01().segments.map((s) => s.canonSegmentId).filter(Boolean));
    for (const id of lockedOrder()) expect(present.has(id), `${id} missing from the graph`).toBe(true);
  });

  it('presents them in the locked order, not the order they were authored', () => {
    const inSpine = ep01().segments.filter((s) => s.canonSegmentId).map((s) => s.canonSegmentId);
    expect(inSpine).toEqual(lockedOrder());
    // The authored list is the thing that disagreed: it put Joe second.
    expect(EP01_AUTHORED_SEGMENTS[1].canonSegmentId).toBe('EP01_JOE');
  });

  it('marks the eight unbuilt segments NOT_STARTED rather than leaving them out', () => {
    expect(EP01_RECONCILIATION.planned.length).toBe(8);
    for (const p of EP01_RECONCILIATION.planned) {
      const seg = ep01().segments.find((s) => s.canonSegmentId === p.canonSegmentId)!;
      expect(seg.productionState).toBe('NOT_STARTED');
      expect(seg.description).toContain('NOT YET BUILT');
      // A plan holds no assets and no jobs. Anything else would be a claim.
      expect(seg.assetIds).toEqual([]);
      expect(seg.jobIds).toEqual([]);
    }
  });

  it('keeps the Goodville gags even though nothing locks their position', () => {
    const unplaced = ep01().segments.filter((s) => !s.canonSegmentId).map((s) => s.name);
    expect(unplaced).toContain('Goodville Geography');
    expect(unplaced).toContain('Goodville Cartoon');
  });

  it('does not count a plan as production', () => {
    for (const p of EP01_RECONCILIATION.planned) {
      const seg = ep01().segments.find((s) => s.canonSegmentId === p.canonSegmentId)!;
      expect(seg.provenance.aggregate).toBe('PLAN');
    }
  });

  it('carries the open questions forward instead of resolving them', () => {
    const shumafied = ep01().segments.find((s) => s.canonSegmentId === 'EP01_SHUMAFIED')!;
    expect(shumafied.description).toContain('Open:');
    expect(shumafied.description).toContain('generated/animated component');
  });
});

describe('provenance derived from canon', () => {
  it('says UNKNOWN where the blueprint says UNSPECIFIED, rather than picking one', () => {
    const coldOpen = EPISODE_01.find((s) => s.id === 'EP01_COLD_OPEN')!;
    const p = canonToProvenance(coldOpen);
    expect(coldOpen.treatment.methodStatus).toBe('UNSPECIFIED');
    expect(p.authorship).toBe('UNKNOWN');
    expect(p.generationMethods).toEqual([]);
  });

  it('records Joe as a reconstruction, never as captured footage', () => {
    const p = canonToProvenance(EPISODE_01.find((s) => s.id === 'EP01_JOE')!);
    expect(p.captureStatus).toBe('RECONSTRUCTED');
    expect(p.assemblyMode).toBe('RECONSTRUCTED_REAL_EVENT');
    expect(p.realityStatus).toBe('FICTIONALIZED_FACT');
  });

  it('records Clothed and Confused as generated and fictional, not animated live action', () => {
    const p = canonToProvenance(EPISODE_01.find((s) => s.id === 'EP01_CLOTHED_AND_CONFUSED')!);
    expect(p.realityStatus).toBe('FICTIONAL');
    expect(p.assemblyMode).toBe('PURE_GENERATED');
    expect(p.generationMethods).toContain('AI_GENERATED');
    expect(p.generationMethods).not.toContain('2D_ANIMATED');
    expect(p.generationMethods).not.toContain('3D_ANIMATED');
  });
});

describe('reconcileEpisode01', () => {
  it('prefers an authored segment over a placeholder', () => {
    const authored: Segment[] = [{
      id: 'X', name: 'My Cold Open', description: 'real work',
      canonSegmentId: 'EP01_COLD_OPEN', productionState: 'BUILT',
      performances: [], gags: [], sourceClips: [], assetIds: ['A1'], jobIds: [],
      provenance: canonToProvenance(EPISODE_01[0]),
    }];
    const { segments, report } = reconcileEpisode01(authored);
    expect(segments[0].id).toBe('X');
    expect(report.built.map((b) => b.canonSegmentId)).toContain('EP01_COLD_OPEN');
    expect(report.planned.map((p) => p.canonSegmentId)).not.toContain('EP01_COLD_OPEN');
  });

  it('fills every gap when nothing is authored at all', () => {
    const { segments, report } = reconcileEpisode01([]);
    expect(segments.length).toBe(lockedOrder().length);
    expect(report.built).toEqual([]);
    expect(report.planned.length).toBe(lockedOrder().length);
  });

  it('a placeholder is unmistakably a placeholder', () => {
    const s = plannedSegment(EPISODE_01.find((x) => x.id === 'EP01_CIGARS')!);
    expect(s.id).toMatch(/^PLAN_/);
    expect(s.productionState).toBe('NOT_STARTED');
    expect(s.provenance.aggregate).toBe('PLAN');
  });
});
