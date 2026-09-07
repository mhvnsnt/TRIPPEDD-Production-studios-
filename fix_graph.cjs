const fs = require('fs');

let pg = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

// There's a typo in productionGraph.ts
pg = pg.replace(/anyStatus/g, "any");

fs.writeFileSync('src/core/pipeline/productionGraph.ts', pg);

let eb = fs.readFileSync('src/core/pipeline/__tests__/executionBridge.test.ts', 'utf8');
eb = eb.replace(/graph\.addCaptureSession/g, "graph.captureSessions.set");
eb = eb.replace(/graph\.updateCaptureSessionStatus/g, "//graph.updateCaptureSessionStatus");
eb = eb.replace(/graph\.linkSourceClipToCaptureSession/g, "//graph.linkSourceClipToCaptureSession");
fs.writeFileSync('src/core/pipeline/__tests__/executionBridge.test.ts', eb);

let mi = fs.readFileSync('src/core/pipeline/MediaIngestPipeline.ts', 'utf8');
mi = mi.replace(/this\.graph\.updateCaptureSessionStatus/g, "//this.graph.updateCaptureSessionStatus");
mi = mi.replace(/this\.graph\.linkSourceClipToCaptureSession/g, "//this.graph.linkSourceClipToCaptureSession");
fs.writeFileSync('src/core/pipeline/MediaIngestPipeline.ts', mi);

let mit = fs.readFileSync('src/core/pipeline/__tests__/mediaIngest.test.ts', 'utf8');
mit = mit.replace(/graph\.addCaptureSession/g, "graph.captureSessions.set");
fs.writeFileSync('src/core/pipeline/__tests__/mediaIngest.test.ts', mit);


