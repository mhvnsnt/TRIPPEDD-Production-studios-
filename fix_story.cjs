const fs = require('fs');
let content = fs.readFileSync('src/components/StoryWorkspace.tsx', 'utf8');
content = content.replace(/provenance: 'REAL_PRODUCTION'/g, "provenance: { realityStatus: 'FACTUAL', captureStatus: 'DIRECTLY_CAPTURED', authorship: 'USER_AUTHORED', generationMethods: ['LIVE_CAPTURE'], assemblyMode: 'PURE_LIVE_ACTION', aiContributions: ['NONE'], aggregate: 'REAL_PRODUCTION' }");
fs.writeFileSync('src/components/StoryWorkspace.tsx', content);
