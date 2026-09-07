import { describe, it, expect, beforeEach } from 'vitest';
import { ProductionGraph } from '../productionGraph';
import { DevelopmentSeed, ProductionType, ProductionTemplate, RequirementTemplate } from '../../types';

describe('Production Types & Templates Layer', () => {
  let graph: ProductionGraph;

  beforeEach(() => {
    (ProductionGraph as any).instance = new (ProductionGraph as any)();
    graph = ProductionGraph.getInstance();
  });

  it('1. Production Types are instantiated correctly', () => {
    expect(graph.productionTypes.size).toBeGreaterThan(0);
    expect(graph.productionTypes.get('pt_live_action_sketch')).toBeDefined();
    expect(graph.productionTypes.get('pt_generated_media')).toBeDefined();
  });

  it('2. Templates can be versioned and are immutable for existing productions', () => {
    const seed: DevelopmentSeed = {
      id: 's1', discoveryId: 'd1', title: 'Test Seed', logline: '', premise: '', 
      format: '', targetProductionType: 'LIVE_ACTION_SKETCH', characters: [], setting: '', tone: '',
      referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', 
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seed);
    const unit = graph.greenlightSeed('s1', 'u_green1');
    expect(unit).toBeDefined();
    
    const initialRequirements = graph.getRequirementsForProduction('u_green1');
    expect(initialRequirements.length).toBeGreaterThan(0);

    // If we duplicate and change a template, it shouldn't retroactively alter 'u_green1' unless explicitly migrated (which is out of scope)
    const oldTemplate = graph.productionTemplates.get(unit!.templateId!);
    const newTemplate = { ...oldTemplate!, id: 'tmpl_v2', version: 2, requirements: [] };
    graph.productionTemplates.set(newTemplate.id, newTemplate);
    
    // The unit still refers to the old template ID implicitly by state, or explicitly in its field
    expect(unit!.templateId).toBe(oldTemplate!.id);
    expect(graph.getRequirementsForProduction('u_green1').length).toBe(initialRequirements.length);
  });

  it('3. Only applicable requirements are instantiated', () => {
    const seedLive: DevelopmentSeed = {
      id: 's_live', title: 'Live Action', logline: '', premise: '', format: '', targetProductionType: 'LIVE_ACTION_SKETCH', characters: [], setting: '', tone: '', referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    const seedGen: DevelopmentSeed = {
      id: 's_gen', title: 'Gen Media', logline: '', premise: '', format: '', targetProductionType: 'GENERATED_MEDIA', characters: [], setting: '', tone: '', referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seedLive);
    graph.addSeed(seedGen);
    
    const unitLive = graph.greenlightSeed('s_live', 'u_live');
    const unitGen = graph.greenlightSeed('s_gen', 'u_gen');

    const liveReqs = graph.getRequirementsForProduction('u_live');
    const genReqs = graph.getRequirementsForProduction('u_gen');

    expect(liveReqs.find(r => r.type === 'req_cast' as any)).toBeDefined();
    expect(liveReqs.find(r => r.type === 'req_human_review' as any)).toBeUndefined(); // shouldn't have gen media requirement

    expect(genReqs.find(r => r.type === 'req_human_review' as any)).toBeDefined();
    expect(genReqs.find(r => r.type === 'req_cast' as any)).toBeUndefined();
  });

  it('4. Greenlighting from seed preserves lineage and bootstraps operational unit', () => {
    const seed: DevelopmentSeed = {
      id: 's2', title: 'Test Bootstrap', logline: '', premise: '', format: '', targetProductionType: 'ANIMATION', characters: [], setting: '', tone: '', referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seed);
    const unit = graph.greenlightSeed('s2', 'u_anim');
    
    expect(unit?.type).toBe('ANIMATION');
    expect(unit?.templateId).toBeDefined();

    const events = graph.getRecentEvents(50);
    const createEvent = events.find(e => e.type === 'PRODUCTION_CREATED_FROM_SEED' && e.entityId === 'u_anim');
    expect(createEvent).toBeDefined();
    expect(createEvent?.metadata.seedId).toBe('s2');
  });

  it('5. Dependency chain outputs human-readable blocker explanations', () => {
    const seed: DevelopmentSeed = {
      id: 's3', title: 'Live Action Blocking', logline: '', premise: '', format: '', targetProductionType: 'LIVE_ACTION_SKETCH', characters: [], setting: '', tone: '', referenceRefs: [], sourceEvidenceRefs: [], status: 'IDEA', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seed);
    graph.greenlightSeed('s3', 'u_block');

    const chainResult = graph.getDependencyChain('u_block', 'PRE_PRODUCTION');
    // The requirement rtScript requires PRE_PRODUCTION, so it will block PRE_PRODUCTION transition
    expect(chainResult.blockers).toBeDefined();
    expect(chainResult.blockers.length).toBeGreaterThan(0);
    expect(chainResult.message).toContain('Cannot enter PRE_PRODUCTION because the Live Action Sketch template requires');
  });
});
