# Goodville Gag Family — extracted from src/core/pipeline/episodes.ts

Source: `src/core/pipeline/episodes.ts` (origin/main)

```
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

```
