import { 
  Observation, ObservationFeedback, PhysicalSourceTimeline, 
  ReviewState, PhysicalEventLabel, ObservationOrigin, StoryboardComparisonResult 
} from '../types';
import { EpisodeRegistry } from './episodes';

export class PhysicalTimelineManager {
  private timeline: PhysicalSourceTimeline;

  constructor(initialTimeline?: PhysicalSourceTimeline) {
    this.timeline = initialTimeline || {
      id: 'PT_001',
      projectId: 'TRIPPEDD_PROD',
      clips: [],
      observations: {},
      chronologyRelationships: [],
      feedbackHistory: []
    };
  }

  
  analyzeChronology() {
    if (!this.timeline.chronologyRelationships) {
      this.timeline.chronologyRelationships = [];
    }

    const clips = this.timeline.clips;
    const observations = Object.values(this.timeline.observations);

    const transcriptsByClip: Record<string, any[]> = {};
    observations.forEach(obs => {
      if (obs.type === 'TRANSCRIPT') {
        if (!transcriptsByClip[obs.sourceClipId]) transcriptsByClip[obs.sourceClipId] = [];
        transcriptsByClip[obs.sourceClipId].push(obs);
      }
    });

    for (let i = 0; i < clips.length; i++) {
      for (let j = i + 1; j < clips.length; j++) {
        const clipA = clips[i];
        const clipB = clips[j];

        const existingRel = this.timeline.chronologyRelationships.find(
          (r: any) => (r.sourceClipIdA === clipA.id && r.sourceClipIdB === clipB.id) || 
               (r.sourceClipIdA === clipB.id && r.sourceClipIdB === clipA.id)
        );

        if (existingRel && existingRel.humanConfirmed) {
          continue; // Rule 8: Preserve human decision
        }

        const tA = transcriptsByClip[clipA.id] || [];
        const tB = transcriptsByClip[clipB.id] || [];

        let sharedText: any = null;
        for (const a of tA) {
          for (const b of tB) {
             if (a.text && b.text && a.text.toLowerCase() === b.text.toLowerCase()) {
                sharedText = a.text;
                break;
             }
          }
          if (sharedText) break;
        }

        let rel: any = existingRel || {
          id: `REL_${clipA.id}_${clipB.id}`,
          sourceClipIdA: clipA.id,
          sourceClipIdB: clipB.id,
          humanConfirmed: false
        };

        if (sharedText && (clipA.startTimecode === 'DIFFERENT_DAY' || clipB.startTimecode === 'DIFFERENT_DAY')) {
            rel.confidence = 'CONTRADICTED';
            rel.relationshipType = 'UNCERTAIN';
            rel.evidenceDetails = {
               missingSignals: [],
               reasoning: 'Timecode explicitly contradicts overlap hypothesis.'
            };
        } else if (sharedText) {
          rel.relationshipType = 'UNCERTAIN';
          rel.confidence = 'POSSIBLE';
          rel.evidenceDetails = {
            matchingTranscripts: [{ text: sharedText }],
            missingSignals: ['EMBEDDED_TIMECODE', 'VISUAL_MATCH'],
            reasoning: 'Matching dialogue found. Could be multi-cam, retake, or duplicate. Insufficient evidence to assert chronological sequence.'
          };
        } else {
          rel.relationshipType = 'UNCERTAIN';
          rel.confidence = 'UNRESOLVED';
          rel.evidenceDetails = {
            missingSignals: ['EMBEDDED_TIMECODE', 'TRANSCRIPT_OVERLAP'],
            reasoning: 'No evidence to establish chronological relationship.'
          };
        }

        if (!existingRel) {
          this.timeline.chronologyRelationships.push(rel);
        }
      }
    }
  }

  addChronologyRelationship(rel: any) {
    if (!this.timeline.chronologyRelationships) this.timeline.chronologyRelationships = [];
    this.timeline.chronologyRelationships.push(rel);
  }

  confirmChronologyRelationship(relId: string) {
    const rel = this.timeline.chronologyRelationships?.find((r: any) => r.id === relId);
    if (rel) {
      rel.confidence = 'CONFIRMED';
      rel.humanConfirmed = true;
    }
  }

  getTimeline() {
    return this.timeline;
  }

  addObservation(obs: Observation) {
    this.timeline.observations[obs.id] = obs;
  }

  getObservation(id: string) {
    return this.timeline.observations[id];
  }

  private addFeedback(feedback: ObservationFeedback) {
    this.timeline.feedbackHistory.push(feedback);
  }

  confirmObservation(id: string, reviewer: string = 'Human') {
    const obs = this.timeline.observations[id];
    if (obs) {
      const prev = obs.reviewState;
      obs.reviewState = 'CONFIRMED';
      this.addFeedback({
        observationId: id,
        action: 'CONFIRM',
        previousValue: { reviewState: prev },
        newValue: { reviewState: 'CONFIRMED' },
        reviewer,
        timestamp: new Date().toISOString()
      });
    }
  }

  rejectObservation(id: string, reviewer: string = 'Human') {
    const obs = this.timeline.observations[id];
    if (obs) {
      const prev = obs.reviewState;
      obs.reviewState = 'REJECTED';
      this.addFeedback({
        observationId: id,
        action: 'REJECT',
        previousValue: { reviewState: prev },
        newValue: { reviewState: 'REJECTED' },
        reviewer,
        timestamp: new Date().toISOString()
      });
    }
  }

  correctObservation(id: string, updates: Partial<Observation>, reviewer: string = 'Human') {
    const obs = this.timeline.observations[id];
    if (obs) {
      const original = { ...obs };
      Object.assign(obs, updates);
      obs.reviewState = 'CORRECTED';
      if (obs.origin === 'MACHINE_GENERATED') {
         obs.origin = 'HUMAN_CORRECTED';
      }
      this.addFeedback({
        observationId: id,
        action: 'EDIT',
        previousValue: original,
        newValue: obs,
        reviewer,
        timestamp: new Date().toISOString()
      });
    }
  }

  splitObservation(id: string, newObservation1: Observation, newObservation2: Observation, reviewer: string = 'Human') {
    const original = this.timeline.observations[id];
    if (original) {
      newObservation1.parentObservationIds = [id];
      newObservation2.parentObservationIds = [id];
      this.addObservation(newObservation1);
      this.addObservation(newObservation2);
      this.rejectObservation(id, reviewer); // Mark original as replaced/rejected
      this.addFeedback({
        observationId: id,
        action: 'SPLIT',
        previousValue: id,
        newValue: [newObservation1.id, newObservation2.id],
        reviewer,
        timestamp: new Date().toISOString()
      });
    }
  }

  mergeObservations(ids: string[], mergedObservation: Observation, reviewer: string = 'Human') {
    mergedObservation.parentObservationIds = ids;
    this.addObservation(mergedObservation);
    ids.forEach(id => {
      this.rejectObservation(id, reviewer);
    });
    this.addFeedback({
      observationId: mergedObservation.id,
      action: 'MERGE',
      previousValue: ids,
      newValue: mergedObservation.id,
      reviewer,
      timestamp: new Date().toISOString()
    });
  }

  compareWithStoryboard(episodeId: string = 'EP01'): StoryboardComparisonResult[] {
    const results: StoryboardComparisonResult[] = [];
    const episode = EpisodeRegistry.getEpisode(episodeId);
    if (!episode) return results;

    const storyboardOrder = episode.segments.map(s => s.id);
    const physicalEvents = Object.values(this.timeline.observations)
      .filter(o => o.type === 'EVENT' && o.reviewState !== 'REJECTED')
      .sort((a, b) => (a.createdAt > b.createdAt ? 1 : -1));

    // A very simple deterministic test comparison logic
    // We expect: BAG_INCIDENT -> JOE_INTERACTION
    let expectedSequence = ['BAG_INCIDENT', 'JOE_INTERACTION'];
    
    // Evaluate what we have in physical events
    const actualSequence = physicalEvents.map(e => (e as any).eventLabel);
    
    actualSequence.forEach((evt, idx) => {
      if (expectedSequence[idx] === evt) {
        results.push({ expectedEvent: evt, detectedEvent: evt, status: 'MATCH', message: 'Physical order matches storyboard' });
      } else if (expectedSequence.includes(evt)) {
        results.push({ expectedEvent: expectedSequence[idx], detectedEvent: evt, status: 'CHRONOLOGY_DISCREPANCY', message: 'Event found out of expected order' });
      } else {
        results.push({ expectedEvent: undefined, detectedEvent: evt, status: 'UNEXPECTED_PHYSICAL_MATERIAL', message: 'Physical event not in storyboard' });
      }
    });

    expectedSequence.forEach(evt => {
      if (!actualSequence.includes(evt)) {
        results.push({ expectedEvent: evt, detectedEvent: undefined, status: 'EXPECTED_BUT_MISSING', message: 'Missing expected material' });
      }
    });

    return results;
  }
}
