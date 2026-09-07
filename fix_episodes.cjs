const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/episodes.ts', 'utf8');

content = content.replace(
  `        {
          id: 'PERF_TYNESHIA_JOE_TIMING',
          actorId: 'TYNESHIA',
          characterId: 'JOE',
          sourceClipIds: ['SC_MOTEL_RAW_001'],
          description: 'Tyneshia establishing blocking and timing for Joe.'
        }`,
  `        {
          id: 'PERF_TYNESHIA_JOE_TIMING',
          productionUnitId: 'u1',
          characterId: 'JOE',
          performerType: 'MIXED',
          personId: 'TYNESHIA',
          status: 'CAPTURED',
          notes: 'Tyneshia establishing blocking and timing for Joe.',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }`
);

content = content.replace(
  `        {
          id: 'PERF_MARS_IRISH_BREAK',
          actorId: 'MARS',
          characterId: 'MARS_MASCOT',
          sourceClipIds: ['SC_LOTI_SHOT_C'],
          description: 'Live-action chilling, leading to "LUCK OF THE IRISH!!!" and freeze for generative handoff.'
        }`,
  `        {
          id: 'PERF_MARS_IRISH_BREAK',
          productionUnitId: 'u1',
          characterId: 'MARS_MASCOT',
          performerType: 'HUMAN',
          personId: 'MARS',
          status: 'PLANNED',
          notes: 'Live-action chilling, leading to "LUCK OF THE IRISH!!!" and freeze for generative handoff.',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }`
);

fs.writeFileSync('src/core/pipeline/episodes.ts', content);
