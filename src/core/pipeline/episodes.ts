import { Episode, Segment, ContentProvenance } from '../types';
import { FormatRegistry } from './formats';
import { reconcileEpisode01 } from './episode01Reconcile';

export class EpisodeRegistry {
  private static episodes = new Map<string, Episode>();

  static registerEpisode(episode: Episode) {
    this.episodes.set(episode.id, episode);
  }

  static getEpisode(id: string): Episode | undefined {
    return this.episodes.get(id);
  }

  static getAllEpisodes(): Episode[] {
    return Array.from(this.episodes.values());
  }
}

// Register Gags Formats (as per directives)
FormatRegistry.registerFormat({
  id: 'DOCUMENTARY_GAG',
  name: 'Documentary Gag',
  description: 'Recurring gag based on real captured interviews acting as factual source material, reused inside fictionalized contexts.',
  ipMode: 'DOCUMENTARY',
  guidelines: [
    'Ingest real captured interview clips as factual source material',
    'Preserve original reality status (FACTUAL) of the clips even if the presentation becomes fictionalized',
    'Allow reuse inside fictionalized/animated segments'
  ],
  defaultProvenance: {
    realityStatus: 'FACTUAL',
    captureStatus: 'DIRECTLY_CAPTURED',
    authorship: 'USER_AUTHORED',
    generationMethods: ['LIVE_CAPTURE'],
    assemblyMode: 'LIVE_ACTION_WITH_GENERATED_ELEMENTS',
    aiContributions: ['NONE'],
    aggregate: 'HYBRID_PRODUCTION'
  }
});

/**
 * The segments that were actually authored for EP01. This list is NOT the
 * episode — it predates the locked blueprint and puts Joe second and the Luck
 * of the Irish commercial fourth, which the creator has corrected. It is the
 * production work that exists; reconcileEpisode01 puts it in canon order and
 * fills the gaps with visible placeholders.
 */
const EP01_AUTHORED_SEGMENTS: Segment[] = [
  {
      id: 'SEG01',
      name: 'Motel Reality',
      canonSegmentId: 'EP01_MOTEL',
      productionState: 'BUILT',
      description: 'Raw live action footage of Mars and Tyneshia at the actual motel location.',
      formatId: 'REAL_EVENT_RECONSTRUCTION',
      locationId: 'REAL_MOTEL', // Will need to define REAL_MOTEL in formats/locations if not done
      performances: [],
      gags: [],
      sourceClips: [
        {
          id: 'SC_MOTEL_RAW_001',
          assetId: 'RAW_MOTEL_VID_001',
          startTimecode: '00:00:00:00',
          endTimecode: '00:05:23:00',
          description: 'Original capture of the scene without Joe.'
        }
      ],
      assetIds: ['RAW_MOTEL_VID_001'],
      jobIds: [],
      provenance: {
        realityStatus: 'FACTUAL',
        captureStatus: 'DIRECTLY_CAPTURED',
        authorship: 'USER_AUTHORED',
        generationMethods: ['LIVE_CAPTURE'],
        assemblyMode: 'PURE_LIVE_ACTION',
        aiContributions: ['NONE'],
        aggregate: 'REAL_PRODUCTION'
      }
    },
    {
      id: 'SEG02',
      name: 'Joe Reconstruction',
      canonSegmentId: 'EP01_JOE',
      productionState: 'IN_PROGRESS',
      description: 'Reconstructed scene where Joe is generated via ComfyUI based on Tyneshia performance timing.',
      formatId: 'REAL_EVENT_RECONSTRUCTION',
      locationId: 'REAL_MOTEL',
      performances: [
        {
          id: 'PERF_TYNESHIA_JOE_TIMING',
          productionUnitId: 'u1',
          characterId: 'JOE',
          performerType: 'MIXED',
          personId: 'TYNESHIA' as any,
          status: 'CAPTURED',
          notes: 'Tyneshia establishing blocking and timing for Joe.',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      ],
      gags: [],
      sourceClips: [],
      assetIds: ['ASSET_JOE_COMPOSITED_001'],
      jobIds: ['JOB_COMFYUI_JOE_001', 'JOB_FFMPEG_COMP_001'],
      provenance: {
        realityStatus: 'FACTUAL',
        captureStatus: 'RECONSTRUCTED',
        authorship: 'COLLABORATIVE_AUTHORED',
        generationMethods: ['MIXED'],
        assemblyMode: 'RECONSTRUCTED_REAL_EVENT',
        aiContributions: ['AI_CO_GENERATED'],
        aggregate: 'HYBRID_PRODUCTION'
      }
    },
    {
      id: 'SEG03',
      name: 'Goodville Geography',
      // Goodville is a gag FAMILY whose placement the creator has not locked.
      // No canonSegmentId: it belongs to the episode, not to the locked spine.
      productionState: 'IN_PROGRESS',
      description: 'Documentary gag where a real interview introduces the elastic distance to Nashville.',
      formatId: 'DOCUMENTARY_GAG',
      locationId: 'GOODVILLE_TN',
      performances: [],
      gags: [
        {
          id: 'GAG_GG_001',
          name: 'Goodville Geography (45 min)',
          type: 'RECURRING',
          description: 'Interviewee claims Nashville is 45 minutes away.',
          formatId: 'DOCUMENTARY_GAG',
          sourceMaterial: [
            {
              id: 'SC_GG_INT_001',
              assetId: 'RAW_INT_001',
              startTimecode: '00:00:10:00',
              endTimecode: '00:00:15:00',
              description: 'Real person answering distance question.',
              originalProvenance: {
                realityStatus: 'FACTUAL',
                captureStatus: 'DIRECTLY_CAPTURED',
                authorship: 'USER_AUTHORED',
                generationMethods: ['LIVE_CAPTURE'],
                assemblyMode: 'PURE_LIVE_ACTION',
                aiContributions: ['NONE'],
                aggregate: 'REAL_PRODUCTION'
              }
            }
          ]
        }
      ],
      sourceClips: [],
      assetIds: [],
      jobIds: [],
      provenance: {
        realityStatus: 'FACTUAL',
        captureStatus: 'DIRECTLY_CAPTURED',
        authorship: 'USER_AUTHORED',
        generationMethods: ['LIVE_CAPTURE'],
        assemblyMode: 'LIVE_ACTION_WITH_GENERATED_ELEMENTS',
        aiContributions: ['NONE'],
        aggregate: 'HYBRID_PRODUCTION'
      }
    },
    {
      id: 'SEG04',
      name: 'Luck of the Irish',
      canonSegmentId: 'EP01_LUCK_OF_THE_IRISH',
      productionState: 'IN_PROGRESS',
      description: 'Fake commercial gag. Live action suspense building up to a generative 4th-wall break.',
      formatId: 'TRIPPEDD_ADULT_ANIMATION_PARODY',
      performances: [
        {
          id: 'PERF_MARS_IRISH_BREAK',
          productionUnitId: 'u1',
          characterId: 'MARS_MASCOT',
          performerType: 'HUMAN',
          personId: 'MARS' as any,
          status: 'PLANNED',
          notes: 'Live-action chilling, leading to "LUCK OF THE IRISH!!!" and freeze for generative handoff.',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      ],
      gags: [
        {
          id: 'GAG_LUCK_IRISH',
          name: 'Luck of the Irish Commercial',
          type: 'FAKE_COMMERCIAL',
          description: 'A completely fictional commercial interrupting the flow. Uses canonical disclaimer #001 for its first appearance.'
        }
      ],
      sourceClips: [
        {
          id: 'SC_LOTI_SHOT_A',
          assetId: 'PENDING_LOTI_WIDE',
          startTimecode: 'TBD',
          endTimecode: 'TBD',
          description: 'Shot A: Far away, slow zoom in, suspense-building, chilling.'
        },
        {
          id: 'SC_LOTI_SHOT_B',
          assetId: 'PENDING_LOTI_CLOSEUP',
          startTimecode: 'TBD',
          endTimecode: 'TBD',
          description: 'Shot B: Different angle, closer, up near the subject, suspense-building.'
        },
        {
          id: 'SC_LOTI_SHOT_C',
          assetId: 'PENDING_LOTI_ACTION',
          startTimecode: 'TBD',
          endTimecode: 'TBD',
          description: 'Shot C: Back to wide. Fourth wall break "LUCK OF THE IRISH!!!". Generative handoff.'
        }
      ],
      assetIds: ['ASSET_LOTI_GENERATED_TRANSFORMATION'],
      jobIds: ['JOB_COMFYUI_LOTI_TRANSFORMATION'],
      provenance: {
        realityStatus: 'FICTIONAL',
        captureStatus: 'PARTIALLY_CAPTURED',
        authorship: 'COLLABORATIVE_AUTHORED',
        generationMethods: ['LIVE_CAPTURE', 'AI_GENERATED'],
        assemblyMode: 'LIVE_ACTION_WITH_GENERATED_ELEMENTS',
        aiContributions: ['AI_CO_GENERATED'],
        aggregate: 'HYBRID_PRODUCTION'
      }
    },
    {
      id: 'SEG05',
      name: 'Goodville Cartoon',
      productionState: 'NOT_STARTED',
      description: 'Animated cutaway happening in Goodville TN.',
      formatId: 'TRIPPEDD_ADULT_ANIMATION_PARODY',
      locationId: 'GOODVILLE_TN',
      performances: [],
      gags: [],
      sourceClips: [],
      assetIds: [],
      jobIds: [],
      provenance: {
        realityStatus: 'FICTIONAL',
        captureStatus: 'NOT_CAPTURED',
        authorship: 'COLLABORATIVE_AUTHORED',
        generationMethods: ['AI_GENERATED', '2D_ANIMATED'],
        assemblyMode: 'PURE_ANIMATION',
        aiContributions: ['AI_CO_GENERATED', 'AI_CO_ANIMATED'],
        aggregate: 'FICTIONAL_CREATION'
      }
    }
];

/**
 * The episode as the creator locked it: canon order, every locked segment
 * present, unbuilt ones marked NOT_STARTED rather than left out.
 */
const ep01 = reconcileEpisode01(EP01_AUTHORED_SEGMENTS);

const episode1: Episode = {
  id: 'EP01',
  name: 'The Walk',
  number: 1,
  description:
    'The pilot. Ordered by docs/creative/EP01-THE-WALK-CANON.md, not by the order the footage was shot ' +
    'and not by the order these segments were authored.',
  status: 'PRODUCTION',
  segments: ep01.segments,
};

/** What is built, what is only planned, and what has no locked position. */
export const EP01_RECONCILIATION = ep01.report;
export { EP01_AUTHORED_SEGMENTS };

EpisodeRegistry.registerEpisode(episode1);
