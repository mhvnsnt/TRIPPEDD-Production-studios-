const fs = require('fs');

let content = fs.readFileSync('src/server/queueManager.ts', 'utf8');

// The ffprobe block (line 85)
content = content.replace(
  /provenance: \{\s*tool: 'ffprobe',\s*version: versionOut.split\('\\n'\)\[0\],\s*command: cmd.substring\(0, 100\) \+ '\.\.\.',\s*success: true,\s*timestamp: new Date\(\)\.toISOString\(\),\s*durationMs: Date.now\(\) - start\s*\}/,
  `provenance: {
          executionState: 'EXECUTED',
          sourceFileId: job.fileId,
          startTime: new Date(start).toISOString(),
          endTime: new Date().toISOString(),
          tool: 'ffprobe',
          version: versionOut.split('\\n')[0],
          command: cmd.substring(0, 100) + '...',
          success: true,
          timestamp: new Date().toISOString(),
          durationMs: Date.now() - start
        }`
);

// OpenCV block (line 159)
content = content.replace(
  /provenance: \{ tool: 'opencv', version: stdout\.trim\(\), command: 'cv2\.VideoCapture', success: true, timestamp: new Date\(\)\.toISOString\(\) \}/,
  `provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'opencv', version: stdout.trim(), command: 'cv2.VideoCapture', success: true, timestamp: new Date().toISOString() }`
);

// Tesseract block (line 167)
content = content.replace(
  /provenance: \{ tool: 'tesseract', version: stdout\.split\('\\n'\)\[0\], command: 'tesseract', success: true, timestamp: new Date\(\)\.toISOString\(\) \}/,
  `provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'tesseract', version: stdout.split('\\n')[0], command: 'tesseract', success: true, timestamp: new Date().toISOString() }`
);

// Whisper block (line 175)
content = content.replace(
  /provenance: \{ tool: 'whisper', version: stdout\.trim\(\), command: 'whisper', success: true, timestamp: new Date\(\)\.toISOString\(\) \}/,
  `provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'whisper', version: stdout.trim(), command: 'whisper', success: true, timestamp: new Date().toISOString() }`
);

fs.writeFileSync('src/server/queueManager.ts', content);
console.log('Patched queueManager provenance');
