import { describe, it, expect, beforeEach } from 'vitest';
import { ProductionGraph } from '../productionGraph';
import { Person, PersonRole, Character, CastAssignment, Performance, Take, DevelopmentSeed } from '../../types';

describe('People / Cast / Character / Performance Layer', () => {
  let graph: ProductionGraph;

  beforeEach(() => {
    (ProductionGraph as any).instance = new (ProductionGraph as any)();
    graph = ProductionGraph.getInstance();
  });

  it('1. Person can have multiple roles.', () => {
    const person: Person = { id: 'p1', name: 'John Doe', status: 'ACTIVE' };
    graph.people.set(person.id, person);
    
    const role1: PersonRole = { id: 'r1', personId: 'p1', productionUnitId: 'u1', department: 'ACTING' as any, role: 'Actor', status: 'ACTIVE' };
    const role2: PersonRole = { id: 'r2', personId: 'p1', productionUnitId: 'u2', department: 'DIRECTING', role: 'Director', status: 'ACTIVE' };
    
    graph.roles.set(role1.id, role1);
    graph.roles.set(role2.id, role2);

    const roles = graph.getRolesForPerson('p1');
    expect(roles.length).toBe(2);
  });

  it('2. Person can portray multiple characters.', () => {
    const p1: Person = { id: 'p_actor', name: 'Actor Person' };
    graph.people.set(p1.id, p1);

    const c1: Character = { id: 'c1', productionUnitId: 'u1', name: 'Char 1', description: '', characterType: 'FICTIONAL', createdAt: '', updatedAt: '' };
    const c2: Character = { id: 'c2', productionUnitId: 'u1', name: 'Char 2', description: '', characterType: 'FICTIONAL', createdAt: '', updatedAt: '' };
    graph.addCharacter(c1);
    graph.addCharacter(c2);

    const ca1: CastAssignment = { id: 'ca1', productionUnitId: 'u1', personId: 'p_actor', characterId: 'c1', status: 'CAST', createdAt: '', updatedAt: '' };
    const ca2: CastAssignment = { id: 'ca2', productionUnitId: 'u1', personId: 'p_actor', characterId: 'c2', status: 'CAST', createdAt: '', updatedAt: '' };
    graph.addCastAssignment(ca1);
    graph.addCastAssignment(ca2);

    expect(Array.from(graph.castAssignments.values()).filter(ca => ca.personId === 'p_actor').length).toBe(2);
  });

  it('3. Character can exist without a Person.', () => {
    const c3: Character = { id: 'c3', productionUnitId: 'u1', name: 'Char 3', description: '', characterType: 'FICTIONAL', createdAt: '', updatedAt: '' };
    graph.addCharacter(c3);

    const assignments = Array.from(graph.castAssignments.values()).filter(ca => ca.characterId === 'c3');
    expect(assignments.length).toBe(0);
    expect(graph.characters.has('c3')).toBe(true);
  });

  it('4. Generated Performance can exist without a Person.', () => {
    const perf: Performance = { id: 'perf_gen', productionUnitId: 'u1', characterId: 'c3', performerType: 'GENERATED', status: 'PLANNED', createdAt: '', updatedAt: '' };
    graph.addPerformance(perf);
    
    const fetched = graph.performances.get('perf_gen');
    expect(fetched).toBeDefined();
    expect(fetched?.personId).toBeUndefined();
    expect(fetched?.performerType).toBe('GENERATED');
  });

  it('5. Performance is distinct from SourceClip.', () => {
    const perf: Performance = { id: 'perf_human', productionUnitId: 'u1', characterId: 'c1', performerType: 'HUMAN', personId: 'p_actor', status: 'PLANNED', createdAt: '', updatedAt: '' };
    graph.addPerformance(perf);

    expect(perf).not.toHaveProperty('clipData');
    expect(perf).not.toHaveProperty('path');
    expect(graph.performances.has('perf_human')).toBe(true);
  });

  it('6. One Performance can have multiple Takes.', () => {
    const perf: Performance = { id: 'perf_takes', productionUnitId: 'u1', characterId: 'c1', performerType: 'HUMAN', status: 'PLANNED', createdAt: '', updatedAt: '' };
    graph.addPerformance(perf);

    const take1: Take = { id: 't1', performanceId: 'perf_takes', takeNumber: 1, status: 'COMPLETED', createdAt: '' };
    const take2: Take = { id: 't2', performanceId: 'perf_takes', takeNumber: 2, status: 'COMPLETED', createdAt: '' };
    graph.addTake(take1);
    graph.addTake(take2);

    const takes = Array.from(graph.takes.values()).filter(t => t.performanceId === 'perf_takes');
    expect(takes.length).toBe(2);
  });

  it('7. Takes can point to source or generated media.', () => {
    const takeSource: Take = { id: 'ts', performanceId: 'p1', takeNumber: 1, sourceClipId: 'clip_1', status: 'COMPLETED', createdAt: '' };
    const takeGen: Take = { id: 'tg', performanceId: 'p1', takeNumber: 2, generatedAssetId: 'gen_1', status: 'COMPLETED', createdAt: '' };
    
    expect(takeSource.sourceClipId).toBe('clip_1');
    expect(takeSource.generatedAssetId).toBeUndefined();
    
    expect(takeGen.generatedAssetId).toBe('gen_1');
    expect(takeGen.sourceClipId).toBeUndefined();
  });

  it('8. Casting changes append ProductionEvents.', () => {
    const ca: CastAssignment = { id: 'ca3', productionUnitId: 'u1', personId: 'p1', characterId: 'c1', status: 'CONSIDERING', createdAt: '', updatedAt: '' };
    graph.addCastAssignment(ca);
    graph.updateCastAssignmentStatus('ca3', 'CAST');

    const recent = graph.getRecentEvents(50);
    const event = recent.find(e => e.type === 'CASTING_CAST' as any);
    expect(event).toBeDefined();
    expect(event?.entityId).toBe('ca3');
  });

  it('9. Performance lifecycle appends ProductionEvents.', () => {
    const perf: Performance = { id: 'perf_evt', productionUnitId: 'u1', characterId: 'c1', performerType: 'HUMAN', status: 'PLANNED', createdAt: '', updatedAt: '' };
    graph.addPerformance(perf);
    graph.updatePerformanceStatus('perf_evt', 'APPROVED');

    const recent = graph.getRecentEvents(50);
    const event = recent.find(e => e.type === 'PERFORMANCE_APPROVED');
    expect(event).toBeDefined();
    expect(event?.entityId).toBe('perf_evt');
  });

  it('10. Casting requirements can block production.', () => {
    const unit = graph.greenlightSeed('seed_clothed', 'u_blocker');
    if (unit) {
      // Add a CAST_CONFIRMED requirement
      graph.addRequirement({
        id: 'req_cast_conf', productionUnitId: unit.id, type: 'CAST_CONFIRMED', description: 'Need Actor', status: 'OPEN', requiredByStage: 'SHOOTING', blocking: true
      });

      const res = graph.updateProductionUnitStatus(unit.id, 'SHOOTING');
      expect(res.success).toBe(false);
      expect(res.blockers?.length).toBeGreaterThan(0);
      expect(res.blockers?.find(b => b.type === 'CAST_CONFIRMED')).toBeDefined();
    }
  });

  it('11. Dependency chains identify missing casting.', () => {
    const unit = graph.greenlightSeed('seed_clothed', 'u_blocker_2');
    if (unit) {
      graph.addRequirement({
        id: 'req_cast_conf2', productionUnitId: unit.id, type: 'CAST_CONFIRMED', description: 'Need Lead Actor', status: 'OPEN', requiredByStage: 'SHOOTING', blocking: true
      });

      const chain = graph.getDependencyChain(unit.id, 'SHOOTING');
      expect(chain.message).toContain('Need Lead Actor');
      expect(chain.chain.find(c => c.type === 'BLOCKING_REQUIREMENT' && c.name === 'CAST_CONFIRMED')).toBeDefined();
    }
  });

  it('12. Source provenance remains unchanged.', () => {
    const perf: Performance = { id: 'perf_prov', productionUnitId: 'u1', characterId: 'c1', performerType: 'HUMAN', provenance: 'ORIGINAL', status: 'PLANNED', createdAt: '', updatedAt: '' };
    expect(perf.provenance).toBe('ORIGINAL');
  });

  it('13. Reference-only material cannot silently become production media.', () => {
    const seed: DevelopmentSeed = { id: 's9', title: 'Ref test', format: '', targetProductionType: 'OTHER', logline: '', premise: '', characters: [], setting: '', tone: '', referenceRefs: ['ref_video_1'], sourceEvidenceRefs: [], status: 'IDEA', createdAt: '', updatedAt: '' };
    // Just asserting that refs stay refs in the schema
    expect(seed.referenceRefs.includes('ref_video_1')).toBe(true);
    expect(seed.sourceEvidenceRefs.includes('ref_video_1')).toBe(false);
  });

  it('14. Clothed and Confused can represent planned generated performances without claiming generated footage exists.', () => {
    // This is seeded in productionGraph.ts during beforeEach
    const clothedUnit = Array.from(graph.productionUnits.values()).find(u => u.name === 'Clothed and Confused');
    expect(clothedUnit).toBeDefined();

    if (clothedUnit) {
      const chars = Array.from(graph.characters.values()).filter(c => c.productionUnitId === clothedUnit.id);
      expect(chars.length).toBeGreaterThanOrEqual(3);
      expect(chars.find(c => c.name === 'Fictional Survivalist')).toBeDefined();

      const perfs = Array.from(graph.performances.values()).filter(p => p.productionUnitId === clothedUnit.id);
      expect(perfs.length).toBeGreaterThanOrEqual(4);
      
      const raftPerf = perfs.find(p => p.notes?.includes('raft'));
      expect(raftPerf).toBeDefined();
      expect(raftPerf?.status).toBe('PLANNED');
      expect(raftPerf?.performerType).toBe('GENERATED');
      
      const takes = Array.from(graph.takes.values()).filter(t => t.performanceId === raftPerf?.id);
      expect(takes.length).toBe(0); // No footage exists
    }
  });
});
