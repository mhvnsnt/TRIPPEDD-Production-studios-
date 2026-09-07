const fs = require('fs');

// Fix MediaIngestPipeline.ts
let mediaIngest = fs.readFileSync('src/core/pipeline/MediaIngestPipeline.ts', 'utf8');
mediaIngest = mediaIngest.replace(/reviewState: 'PENDING'/g, "reviewState: 'UNREVIEWED'");
fs.writeFileSync('src/core/pipeline/MediaIngestPipeline.ts', mediaIngest);

// Fix chronologyEngine.test.ts
let chronoTest = fs.readFileSync('src/core/pipeline/__tests__/chronologyEngine.test.ts', 'utf8');
chronoTest = chronoTest.replace(/reviewState: 'PENDING'/g, "reviewState: 'UNREVIEWED', description: '', createdAt: new Date().toISOString()");
fs.writeFileSync('src/core/pipeline/__tests__/chronologyEngine.test.ts', chronoTest);

// Fix executionBridge.test.ts
let execBridgeTest = fs.readFileSync('src/core/pipeline/__tests__/executionBridge.test.ts', 'utf8');
execBridgeTest = execBridgeTest.replace(/reviewState: 'PENDING'/g, "reviewState: 'UNREVIEWED'");
execBridgeTest = execBridgeTest.replace(/title: 'Draft Script'/g, "title: 'Draft Script', description: ''");
execBridgeTest = execBridgeTest.replace(/title: 'Shoot Scene 1'/g, "title: 'Shoot Scene 1', description: ''");
execBridgeTest = execBridgeTest.replace(/title: 'Test Order'/g, "title: 'Test Order', description: ''");
fs.writeFileSync('src/core/pipeline/__tests__/executionBridge.test.ts', execBridgeTest);

// Fix seed.ts
let seed = fs.readFileSync('src/core/pipeline/seed.ts', 'utf8');
seed = seed.replace(/title: 'Write Episode 1 Script',/g, "title: 'Write Episode 1 Script', description: 'desc',");
fs.writeFileSync('src/core/pipeline/seed.ts', seed);

console.log("Fixed tests");
