import { describe, it, expect, beforeEach } from 'vitest';
import { PhysicalTimelineManager } from '../physicalTimeline';
import { Observation, PhysicalEvent } from '../../types';

describe('Physical Timeline Manager', () => {
  let manager: PhysicalTimelineManager;

  beforeEach(() => {
    manager = new PhysicalTimelineManager();
  });

  it('keeps physical timeline independent of editorial', () => {
    expect(manager.getTimeline().clips.length).toBe(0);
  });

  it('preserves machine observations but does not make them facts automatically', () => {
    const obs: Observation = {
      id: 'obs_1',
      sourceClipId: 'clip_1',
      type: 'VISUAL',
      description: 'Two people standing',
      confidence: 0.8,
      origin: 'MACHINE_GENERATED',
      reviewState: 'UNREVIEWED',
      createdAt: new Date().toISOString()
    };
    manager.addObservation(obs);
    
    const retrieved = manager.getObservation('obs_1');
    expect(retrieved.origin).toBe('MACHINE_GENERATED');
    expect(retrieved.reviewState).toBe('UNREVIEWED');
  });

  it('human correction preserves original data trail', () => {
    const obs: Observation = {
      id: 'obs_1',
      sourceClipId: 'clip_1',
      type: 'VISUAL',
      description: 'Two people standing',
      confidence: 0.8,
      origin: 'MACHINE_GENERATED',
      reviewState: 'UNREVIEWED',
      createdAt: new Date().toISOString()
    };
    manager.addObservation(obs);
    
    manager.correctObservation('obs_1', { description: 'Bag Incident Confirmed' });
    
    const retrieved = manager.getObservation('obs_1');
    expect(retrieved.origin).toBe('HUMAN_CORRECTED');
    expect(retrieved.reviewState).toBe('CORRECTED');
    expect(retrieved.description).toBe('Bag Incident Confirmed');
    
    const feedback = manager.getTimeline().feedbackHistory.find(f => f.observationId === 'obs_1');
    expect(feedback?.action).toBe('EDIT');
    expect(feedback?.previousValue.description).toBe('Two people standing');
  });

  it('split preserves lineage', () => {
    const obs: Observation = {
      id: 'obs_1',
      sourceClipId: 'clip_1',
      type: 'VISUAL',
      description: 'Long segment',
      origin: 'MACHINE_GENERATED',
      reviewState: 'UNREVIEWED',
      createdAt: new Date().toISOString()
    };
    manager.addObservation(obs);
    
    const split1: Observation = { ...obs, id: 'obs_1a', description: 'Part 1' };
    const split2: Observation = { ...obs, id: 'obs_1b', description: 'Part 2' };
    
    manager.splitObservation('obs_1', split1, split2);
    
    expect(manager.getObservation('obs_1').reviewState).toBe('REJECTED');
    expect(manager.getObservation('obs_1a').parentObservationIds).toContain('obs_1');
    expect(manager.getObservation('obs_1b').parentObservationIds).toContain('obs_1');
  });

  it('merge preserves contributors', () => {
    const obs1: Observation = { id: 'o1', sourceClipId: 'c1', type: 'VISUAL', description: 'P1', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', createdAt: '' };
    const obs2: Observation = { id: 'o2', sourceClipId: 'c1', type: 'VISUAL', description: 'P2', origin: 'MACHINE_GENERATED', reviewState: 'UNREVIEWED', createdAt: '' };
    manager.addObservation(obs1);
    manager.addObservation(obs2);
    
    const merged: Observation = { id: 'om', sourceClipId: 'c1', type: 'VISUAL', description: 'Merged', origin: 'HUMAN_CREATED', reviewState: 'UNREVIEWED', createdAt: '' };
    manager.mergeObservations(['o1', 'o2'], merged);
    
    expect(manager.getObservation('o1').reviewState).toBe('REJECTED');
    expect(manager.getObservation('o2').reviewState).toBe('REJECTED');
    expect(manager.getObservation('om').parentObservationIds).toEqual(['o1', 'o2']);
  });

  it('identifies chronology discrepancies vs storyboard', () => {
    const event1: PhysicalEvent = {
      id: 'e1', sourceClipId: 'c1', type: 'EVENT', eventLabel: 'JOE_INTERACTION',
      origin: 'HUMAN_CREATED', reviewState: 'CONFIRMED', description: '', createdAt: '2023-01-01T10:00:00'
    };
    const event2: PhysicalEvent = {
      id: 'e2', sourceClipId: 'c1', type: 'EVENT', eventLabel: 'BAG_INCIDENT',
      origin: 'HUMAN_CREATED', reviewState: 'CONFIRMED', description: '', createdAt: '2023-01-01T10:05:00'
    };
    
    manager.addObservation(event1);
    manager.addObservation(event2);
    
    const comp = manager.compareWithStoryboard('EP01');
    // Storyboard expects BAG_INCIDENT -> JOE_INTERACTION
    // We fed it JOE_INTERACTION -> BAG_INCIDENT
    
    const discrepancy = comp.find(c => c.status === 'CHRONOLOGY_DISCREPANCY');
    expect(discrepancy).toBeDefined();
  });
});
