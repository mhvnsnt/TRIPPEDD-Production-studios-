const fs = require('fs');
let testCode = fs.readFileSync('src/core/pipeline/__tests__/mediaIngest.test.ts', 'utf8');

testCode = testCode.replace(
  "ingestPipeline = new MediaIngestPipeline(graph, physicalTimeline, new ToolchainOrchestrator());",
  "const MockOrch = class { async analyzeFile(filePath: string) { if (filePath === 'corrupted.mp4') { return [{ provenance: { tool: 'ffprobe', success: false, error: 'Invalid data' } }]; } return [ { provenance: { tool: 'ffprobe', success: true, command: 'ffprobe ...' }, metadata: { duration: 120 } }, { provenance: { tool: 'scenedetect', success: true, command: 'scenedetect ...' }, scenes: [ { startTime: 0, endTime: 10 }, { startTime: 10, endTime: 20 } ] }, { provenance: { tool: 'whisper', success: true, command: 'whisper ...' }, transcripts: [ { startTime: 0, endTime: 5, text: 'Hello world' }, { startTime: 5, endTime: 10, text: 'This is a test' } ] } ]; } }; ingestPipeline = new MediaIngestPipeline(graph, physicalTimeline, new MockOrch() as any);"
);

fs.writeFileSync('src/core/pipeline/__tests__/mediaIngest.test.ts', testCode);
