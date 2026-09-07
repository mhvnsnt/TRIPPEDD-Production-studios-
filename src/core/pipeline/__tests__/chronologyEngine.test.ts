import { describe, it, expect, beforeEach } from 'vitest';
import { PhysicalTimelineManager } from '../physicalTimeline';
import { SourceClip, TranscriptSegment, PhysicalEvent } from '../../types';

describe('Chronology Reconstruction Engine', () => {
  let manager: PhysicalTimelineManager;

  beforeEach(() => {
    manager = new PhysicalTimelineManager();
  });

  it('identical dialogue does NOT automatically create a confirmed overlap', () => {
    manager.getTimeline().clips.push({ id: 'C1' } as SourceClip);
    manager.getTimeline().clips.push({ id: 'C2' } as SourceClip);
    
    manager.addObservation({
      id: 'O1', type: 'TRANSCRIPT', sourceClipId: 'C1', text: 'Hello', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString()
    } as TranscriptSegment);
    manager.addObservation({
      id: 'O2', type: 'TRANSCRIPT', sourceClipId: 'C2', text: 'Hello', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString()
    } as TranscriptSegment);

    manager.analyzeChronology();
    const rels = manager.getTimeline().chronologyRelationships!;
    expect(rels.length).toBeGreaterThan(0);
    expect(rels[0].confidence).not.toBe('CONFIRMED');
    expect(['POSSIBLE', 'PROVISIONAL']).toContain(rels[0].confidence);
    expect(rels[0].relationshipType).not.toBe('OVERLAP'); // Could be RETAKE, etc.
  });

  it('a cut command does NOT automatically establish sequence', () => {
    manager.getTimeline().clips.push({ id: 'C1' } as SourceClip);
    manager.getTimeline().clips.push({ id: 'C2' } as SourceClip);
    
    manager.addObservation({
      id: 'O1', type: 'TRANSCRIPT', sourceClipId: 'C1', text: 'Action', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString(), editorialClassification: 'PRODUCTION_ARTIFACT'
    } as any);
    manager.addObservation({
      id: 'O2', type: 'TRANSCRIPT', sourceClipId: 'C2', text: 'Cut', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString(), editorialClassification: 'PRODUCTION_ARTIFACT'
    } as any);

    manager.analyzeChronology();
    const rels = manager.getTimeline().chronologyRelationships!;
    const seqRel = rels.find(r => r.sourceClipIdA === 'C1' && r.sourceClipIdB === 'C2' && r.relationshipType === 'SEQUENTIAL');
    if (seqRel) {
      expect(seqRel.confidence).toBe('UNRESOLVED');
    }
  });

  it('missing timestamps produce UNRESOLVED rather than guessed chronology', () => {
    manager.getTimeline().clips.push({ id: 'C1' } as SourceClip);
    manager.getTimeline().clips.push({ id: 'C2' } as SourceClip);
    
    manager.analyzeChronology();
    const rels = manager.getTimeline().chronologyRelationships!;
    const rel = rels.find(r => r.sourceClipIdA === 'C1' && r.sourceClipIdB === 'C2');
    expect(rel).toBeDefined();
    expect(rel!.confidence).toBe('UNRESOLVED');
    expect(rel!.evidenceDetails.missingSignals).toContain('EMBEDDED_TIMECODE');
  });

  it('a later upload can strengthen or contradict a provisional relationship', () => {
    manager.getTimeline().clips.push({ id: 'C1' } as SourceClip);
    manager.getTimeline().clips.push({ id: 'C2' } as SourceClip);
    manager.addObservation({ id: 'O1', type: 'TRANSCRIPT', sourceClipId: 'C1', text: 'overlap text', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString() } as TranscriptSegment);
    manager.addObservation({ id: 'O2', type: 'TRANSCRIPT', sourceClipId: 'C2', text: 'overlap text', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString() } as TranscriptSegment);
    
    manager.analyzeChronology();
    let rels = manager.getTimeline().chronologyRelationships!;
    expect(rels[0].confidence).toBe('POSSIBLE');

    // Simulate later upload proving it's from a different day
    manager.getTimeline().clips.find(c => c.id === 'C2')!.startTimecode = 'DIFFERENT_DAY';
    manager.analyzeChronology();
    rels = manager.getTimeline().chronologyRelationships!;
    expect(rels[0].confidence).toBe('CONTRADICTED');
  });

  it('existing human decisions survive incremental ingestion', () => {
    manager.getTimeline().clips.push({ id: 'C1' } as SourceClip);
    manager.getTimeline().clips.push({ id: 'C2' } as SourceClip);
    manager.addObservation({ id: 'O1', type: 'TRANSCRIPT', sourceClipId: 'C1', text: 'text', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString() } as TranscriptSegment);
    manager.addObservation({ id: 'O2', type: 'TRANSCRIPT', sourceClipId: 'C2', text: 'text', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString() } as TranscriptSegment);
    
    manager.analyzeChronology();
    let rel = manager.getTimeline().chronologyRelationships![0];
    
    // Human confirms it
    manager.confirmChronologyRelationship(rel.id);
    
    // Incremental ingest runs again
    manager.analyzeChronology();
    rel = manager.getTimeline().chronologyRelationships![0];
    
    expect(rel.confidence).toBe('CONFIRMED');
    expect(rel.humanConfirmed).toBe(true);
  });
});
