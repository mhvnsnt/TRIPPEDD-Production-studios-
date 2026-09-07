const fs = require('fs');

let content = fs.readFileSync('src/server/queueManager.ts', 'utf8');

content = content.replace(/provenance: \{\s*tool: 'ffprobe'[\s\S]*?durationMs: Date.now\(\) - start\s*\}/, `provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date(start).toISOString(), endTime: new Date().toISOString(), tool: 'ffprobe', version: versionOut.split('\\n')[0], command: cmd.substring(0, 100) + '...', success: true, timestamp: new Date().toISOString(), durationMs: Date.now() - start }`);

content = content.replace(/provenance: \{ tool: 'tesseract'[\s\S]*?timestamp: new Date\(\)\.toISOString\(\) \}/, `provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'tesseract', version: stdout.split('\\n')[0], command: 'tesseract', success: true, timestamp: new Date().toISOString() }`);

fs.writeFileSync('src/server/queueManager.ts', content);
