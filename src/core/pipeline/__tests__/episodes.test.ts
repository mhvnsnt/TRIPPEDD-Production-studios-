import { describe, it, expect } from 'vitest';
import { EpisodeRegistry } from '../episodes';
import { FormatRegistry } from '../formats';

describe('Episode and Segment Ontology Tests', () => {
  it('should have the Documentary Gag format registered', () => {
    const format = FormatRegistry.getFormat('DOCUMENTARY_GAG');
    expect(format).toBeDefined();
    expect(format?.ipMode).toBe('DOCUMENTARY');
    expect(format?.defaultProvenance.realityStatus).toBe('FACTUAL');
  });

  it('should retrieve Episode 1 test fixture', () => {
    const episode = EpisodeRegistry.getEpisode('EP01');
    expect(episode).toBeDefined();
    expect(episode?.segments.length).toBe(5);
  });

  it('should distinguish real capture in Motel Reality segment', () => {
    const episode = EpisodeRegistry.getEpisode('EP01');
    const motelReality = episode?.segments.find(s => s.id === 'SEG01');
    expect(motelReality).toBeDefined();
    expect(motelReality?.provenance.realityStatus).toBe('FACTUAL');
    expect(motelReality?.provenance.assemblyMode).toBe('PURE_LIVE_ACTION');
    expect(motelReality?.provenance.aiContributions).toContain('NONE');
    
    // Verify source clips
    expect(motelReality?.sourceClips.length).toBeGreaterThan(0);
    expect(motelReality?.sourceClips[0].assetId).toBe('RAW_MOTEL_VID_001');
  });

  it('should handle reconstructed factual events correctly', () => {
    const episode = EpisodeRegistry.getEpisode('EP01');
    const reconstruction = episode?.segments.find(s => s.id === 'SEG02');
    
    expect(reconstruction).toBeDefined();
    expect(reconstruction?.provenance.realityStatus).toBe('FACTUAL');
    expect(reconstruction?.provenance.captureStatus).toBe('RECONSTRUCTED');
    expect(reconstruction?.provenance.assemblyMode).toBe('RECONSTRUCTED_REAL_EVENT');
    expect(reconstruction?.provenance.aiContributions).toContain('AI_CO_GENERATED');
    
    // Verify performance linkage to original raw footage
    expect(reconstruction?.performances.length).toBe(1);
    expect(reconstruction?.performances[0].actorId).toBe('TYNESHIA');
    expect(reconstruction?.performances[0].characterId).toBe('JOE');
    expect(reconstruction?.performances[0].sourceClipIds).toContain('SC_MOTEL_RAW_001');
  });

  it('should allow real documentary clips as source material inside a Goodville Geography gag', () => {
    const episode = EpisodeRegistry.getEpisode('EP01');
    const goodvilleGag = episode?.segments.find(s => s.id === 'SEG03');
    
    expect(goodvilleGag).toBeDefined();
    expect(goodvilleGag?.formatId).toBe('DOCUMENTARY_GAG');
    expect(goodvilleGag?.locationId).toBe('GOODVILLE_TN');
    
    expect(goodvilleGag?.gags.length).toBe(1);
    const gag = goodvilleGag?.gags[0];
    
    expect(gag?.type).toBe('RECURRING');
    
    // Check that the source material retains original FACTUAL reality status
    const sourceMaterial = gag?.sourceMaterial?.[0];
    expect(sourceMaterial).toBeDefined();
    expect(sourceMaterial?.originalProvenance?.realityStatus).toBe('FACTUAL');
    expect(sourceMaterial?.originalProvenance?.captureStatus).toBe('DIRECTLY_CAPTURED');
  });

  it('should handle completely fictional Goodville animation segments', () => {
    const episode = EpisodeRegistry.getEpisode('EP01');
    const cartoon = episode?.segments.find(s => s.id === 'SEG05');
    
    expect(cartoon).toBeDefined();
    expect(cartoon?.locationId).toBe('GOODVILLE_TN');
    expect(cartoon?.provenance.realityStatus).toBe('FICTIONAL');
    expect(cartoon?.provenance.assemblyMode).toBe('PURE_ANIMATION');
    expect(cartoon?.provenance.aiContributions).toContain('AI_CO_ANIMATED');
  });
});
