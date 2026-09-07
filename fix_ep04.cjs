const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/episodes.ts', 'utf8');

const seg04Old = `    {
      id: 'SEG04',
      name: 'Luck of the Irish',
      description: 'Fake commercial gag.',
      formatId: 'TRIPPEDD_ADULT_ANIMATION_PARODY',
      performances: [],
      gags: [
        {
          id: 'GAG_LUCK_IRISH',
          name: 'Luck of the Irish Commercial',
          type: 'FAKE_COMMERCIAL',
          description: 'A completely fictional commercial interrupting the flow.'
        }
      ],
      sourceClips: [],
      assetIds: [],
      jobIds: [],
      provenance: {
        realityStatus: 'FICTIONAL',
        captureStatus: 'NOT_CAPTURED',
        authorship: 'COLLABORATIVE_AUTHORED',
        generationMethods: ['AI_GENERATED', '2D_ANIMATED'],
        assemblyMode: 'PURE_ANIMATION',
        aiContributions: ['AI_CO_GENERATED'],
        aggregate: 'FICTIONAL_CREATION'
      }
    }`;

const seg04New = `    {
      id: 'SEG04',
      name: 'Luck of the Irish',
      description: 'Fake commercial gag. Live action suspense building up to a generative 4th-wall break.',
      formatId: 'TRIPPEDD_ADULT_ANIMATION_PARODY',
      performances: [
        {
          id: 'PERF_MARS_IRISH_BREAK',
          actorId: 'MARS',
          characterId: 'MARS_MASCOT',
          sourceClipIds: ['SC_LOTI_SHOT_C'],
          description: 'Live-action chilling, leading to "LUCK OF THE IRISH!!!" and freeze for generative handoff.'
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
    }`;

content = content.replace(seg04Old, seg04New);
fs.writeFileSync('src/core/pipeline/episodes.ts', content);
