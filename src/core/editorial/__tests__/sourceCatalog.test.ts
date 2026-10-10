/**
 * The catalog exists to make the creator's confirmations permanent and to keep
 * a display label from ever being mistaken for a filename. Both are tested from
 * the failing side.
 */
import { describe, it, expect } from 'vitest';
import { SourceCatalog, type SourceClipEntry } from '../sourceCatalog';

const clip = (sourceId: string, originalFilename: string): Partial<SourceClipEntry> & Pick<SourceClipEntry, 'sourceId' | 'originalFilename'> =>
  ({ sourceId, originalFilename, recordedAt: '2026-09-06T15:47:42.101Z', durationSec: 18.2 });

function catalog() {
  const c = new SourceCatalog();
  c.register(clip('VID_20260906_104742101', 'VID_20260906_104742101.mp4') as any);
  c.register(clip('VID_20260906_110016345', 'VID_20260906_110016345.mp4') as any);
  return c;
}

describe('source identity is immutable', () => {
  it('a display name never replaces the filename to open in Drive', () => {
    const c = catalog();
    c.confirm('VID_20260906_104742101', 'EP01_CIGARS', { displayName: 'Cigars — Actual Trip — Candidate 1' });
    const v = c.view('VID_20260906_104742101')!;
    expect(v.openInDriveAs).toBe('VID_20260906_104742101.mp4');
    expect(v.catalogDisplayName).toBe('Cigars — Actual Trip — Candidate 1');
    expect(v.driveFileRenamed).toBe(false);
  });

  it('keeps the original filename after every kind of assignment', () => {
    const c = catalog();
    c.propose('VID_20260906_110016345', 'EP01_CIGARS', 'transcript mentions the store', 'Walk — Candidate');
    c.reject('VID_20260906_110016345', 'EP01_CIGARS');
    expect(c.get('VID_20260906_110016345')!.originalFilename).toBe('VID_20260906_110016345.mp4');
  });
});

describe('a human confirmation is permanent', () => {
  it('an AI pass cannot overwrite a confirmed assignment', () => {
    const c = catalog();
    c.confirm('VID_20260906_104742101', 'EP01_CIGARS', { note: 'this is the cigar store' });
    expect(c.propose('VID_20260906_104742101', 'EP01_MOTEL', 'looks like a room')).toBe('REFUSED_HUMAN_CONFIRMED');
    const e = c.get('VID_20260906_104742101')!;
    expect(e.canonSegmentId).toBe('EP01_CIGARS');
    expect(e.assignmentStatus).toBe('HUMAN_CONFIRMED');
  });

  it('a rejection stops the same wrong guess coming back', () => {
    const c = catalog();
    c.reject('VID_20260906_110016345', 'EP01_JOE');
    expect(c.propose('VID_20260906_110016345', 'EP01_JOE', 'the word joe appears')).toBe('REFUSED_HUMAN_REJECTED');
    expect(c.propose('VID_20260906_110016345', 'EP01_CIGARS', 'the store')).toBe('APPLIED');
  });

  it('survives a re-ingest — re-running analysis is not the creator changing his mind', () => {
    const c = catalog();
    c.confirm('VID_20260906_104742101', 'EP01_CIGARS', { displayName: 'Cigars — Actual Trip' });
    // Same clip comes back through the pipeline with fresh measurements.
    c.register({ ...clip('VID_20260906_104742101', 'VID_20260906_104742101.mp4'),
      transcriptLineCount: 6, durationSec: 18.2 } as any);
    const e = c.get('VID_20260906_104742101')!;
    expect(e.assignmentStatus).toBe('HUMAN_CONFIRMED');
    expect(e.canonSegmentId).toBe('EP01_CIGARS');
    expect(e.displayName).toBe('Cigars — Actual Trip');
    expect(e.transcriptLineCount).toBe(6);
  });

  it('only confirmed assignments are offered as ground truth', () => {
    const c = catalog();
    c.propose('VID_20260906_110016345', 'EP01_CIGARS', 'guess');
    c.confirm('VID_20260906_104742101', 'EP01_CIGARS');
    expect(c.confirmedMappings()).toEqual([{ sourceId: 'VID_20260906_104742101', canonSegmentId: 'EP01_CIGARS' }]);
  });

  it('a confirmation clears an earlier rejection of that same segment', () => {
    const c = catalog();
    c.reject('VID_20260906_104742101', 'EP01_CIGARS');
    c.confirm('VID_20260906_104742101', 'EP01_CIGARS');
    expect(c.get('VID_20260906_104742101')!.rejectedSegmentIds).not.toContain('EP01_CIGARS');
  });
});

describe('confidence is per channel', () => {
  it('keeps visual and audio confidence apart — on this footage audio is the weaker one', () => {
    const c = new SourceCatalog();
    c.register({ ...clip('X', 'X.mp4'), confidence: { visual: 'HIGH', audio: 'LOW', chronology: 'HIGH' } } as any);
    const e = c.get('X')!;
    expect(e.confidence.visual).toBe('HIGH');
    expect(e.confidence.audio).toBe('LOW');
  });
});

describe('round trip', () => {
  it('survives serialisation with its statuses intact', () => {
    const c = catalog();
    c.confirm('VID_20260906_104742101', 'EP01_CIGARS', { displayName: 'Cigars — Actual Trip' });
    c.reject('VID_20260906_110016345', 'EP01_JOE');
    const back = SourceCatalog.fromJSON(JSON.parse(JSON.stringify(c.toJSON())));
    expect(back.confirmedMappings()).toEqual([{ sourceId: 'VID_20260906_104742101', canonSegmentId: 'EP01_CIGARS' }]);
    expect(back.propose('VID_20260906_110016345', 'EP01_JOE', 'again')).toBe('REFUSED_HUMAN_REJECTED');
  });
});
