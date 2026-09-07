import { describe, it, expect, beforeEach } from 'vitest';
import { ProductionGraph } from '../productionGraph';
import { CreativeDiscovery, DevelopmentSeed, CreativeDocument, DocumentVersion } from '../../types';

describe('Development / Writers Room Layer', () => {
  let graph: ProductionGraph;

  beforeEach(() => {
    (ProductionGraph as any).instance = new (ProductionGraph as any)();
    graph = ProductionGraph.getInstance();
  });

  it('1. CreativeDiscovery is independent from PhysicalSourceTimeline.', () => {
    const discovery: CreativeDiscovery = {
      id: 'd1', title: 'Absurd seriousness', premise: 'Reality show takes trivial things seriously',
      description: '', status: 'CAPTURED', createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(), sourceRefs: ['clip_123'], evidenceRefs: [], tags: []
    };
    graph.addDiscovery(discovery);
    expect(graph.discoveries.get('d1')).toBeDefined();
    expect(graph.discoveries.get('d1')?.sourceRefs).toContain('clip_123');
  });

  it('2. Source references preserve provenance (lineage relationships).', () => {
    const discovery: CreativeDiscovery = {
      id: 'd2', title: 'Test', premise: 'Test', description: '', status: 'CAPTURED', 
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), 
      sourceRefs: [], evidenceRefs: [], tags: []
    };
    graph.addDiscovery(discovery);
    
    const seed: DevelopmentSeed = {
      id: 's1', discoveryId: 'd2', title: 'Test Seed', logline: '', premise: '', 
      format: '', targetProductionType: 'SKETCH', characters: [], setting: '', tone: '',
      referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', 
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seed);

    const rels = graph.getRelationshipsFor('s1', 'DEVELOPMENT_SEED');
    expect(rels.length).toBeGreaterThan(0);
    expect(rels[0].relationshipType).toBe('DEVELOPMENT_SEED_FROM_DISCOVERY');
    expect(rels[0].targetId).toBe('d2');
  });

  it('4. Document versions are immutable (new rewrites create new versions).', () => {
    const doc: CreativeDocument = { id: 'doc1', seedId: 's1', title: 'Pilot', type: 'SCRIPT', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
    graph.addDocument(doc);

    const v1: DocumentVersion = { id: 'v1', documentId: 'doc1', versionNumber: 1, createdAt: new Date().toISOString(), content: 'V1 content', status: 'DRAFT' };
    const v2: DocumentVersion = { id: 'v2', documentId: 'doc1', versionNumber: 2, createdAt: new Date().toISOString(), content: 'V2 content', status: 'DRAFT' };
    
    graph.addDocumentVersion(v1);
    graph.addDocumentVersion(v2);

    const versions = graph.getVersionsForDocument('doc1');
    expect(versions.length).toBe(2);
    expect(versions[0].versionNumber).toBe(2); // Sorted descending
    expect(versions[1].content).toBe('V1 content');
  });

  it('6. Greenlighting creates a ProductionUnit without deleting the seed.', () => {
    const seed: DevelopmentSeed = {
      id: 's2', title: 'Clothed and Confused', logline: 'Comedy', premise: '', 
      format: '', targetProductionType: 'SKETCH', characters: [], setting: '', tone: '',
      referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', 
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seed);

    const unit = graph.greenlightSeed('s2', 'u_green1');
    
    // Seed is preserved and status updated
    expect(graph.seeds.get('s2')?.status).toBe('GREENLIT');
    
    // ProductionUnit is created
    expect(unit).toBeDefined();
    expect(unit?.id).toBe('u_green1');
    expect(graph.productionUnits.get('u_green1')).toBeDefined();
  });

  it('7. Greenlighting preserves source lineage and 8. creates a ProductionEvent.', () => {
    const seed: DevelopmentSeed = {
      id: 's3', title: 'Test 3', logline: '', premise: '', 
      format: '', targetProductionType: 'SKETCH', characters: [], setting: '', tone: '',
      referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', 
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seed);
    graph.greenlightSeed('s3', 'u_green2');

    // Lineage relationship
    const rels = graph.getRelationshipsFor('u_green2', 'PRODUCTION_UNIT');
    expect(rels.find(r => r.relationshipType === 'PRODUCTION_CREATED_FROM_SEED')).toBeDefined();

    // Event created
    const event = graph.events.find(e => e.type === 'PRODUCTION_CREATED_FROM_SEED' && e.entityId === 'u_green2');
    expect(event).toBeDefined();
    expect(event?.metadata?.seedId).toBe('s3');
  });
});
