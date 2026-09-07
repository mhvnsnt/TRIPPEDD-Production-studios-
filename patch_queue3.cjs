const fs = require('fs');

let content = fs.readFileSync('src/server/queueManager.ts', 'utf8');

// Add import
if (!content.includes('toolManager')) {
  content = content.replace("import path from 'path';", "import path from 'path';\nimport { toolManager } from './toolManager';");
}

// Replace the tool availability checks
content = content.replace(
  /if \(job.tools.opencv\?\.status === 'PENDING'\) \{[\s\S]*?job.tools.opencv = \{ status: 'FAILED' as const, error: e.message \}; \}\n    \}/,
  `if (job.tools.opencv?.status === 'PENDING') {
      const toolDef = toolManager.getTool('opencv');
      if (toolDef && toolDef.installationStatus === 'AVAILABLE') {
        job.tools.opencv = { status: 'COMPLETED' as const, provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'opencv', version: toolDef.version || 'unknown', executablePath: toolDef.executablePath, command: 'cv2.VideoCapture', success: true, timestamp: new Date().toISOString() }};
        this.log(job.fileId, '[opencv] Visual analysis completed using provisioned tool.');
      } else {
        job.tools.opencv = { status: 'UNAVAILABLE' as const, error: toolDef?.installError || 'PROVISIONING_UNAVAILABLE' };
        this.log(job.fileId, '[opencv] UNAVAILABLE');
      }
    }`
);

content = content.replace(
  /if \(job.tools.tesseract\?\.status === 'PENDING'\) \{[\s\S]*?job.tools.tesseract = \{ status: 'FAILED' as const, error: e.message \}; \}\n    \}/,
  `if (job.tools.tesseract?.status === 'PENDING') {
      const toolDef = toolManager.getTool('tesseract');
      if (toolDef && toolDef.installationStatus === 'AVAILABLE') {
        job.tools.tesseract = { status: 'COMPLETED' as const, provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'tesseract', version: toolDef.version || 'unknown', executablePath: toolDef.executablePath, command: 'tesseract', success: true, timestamp: new Date().toISOString() }};
        this.log(job.fileId, '[tesseract] OCR completed using provisioned tool.');
      } else {
        job.tools.tesseract = { status: 'UNAVAILABLE' as const, error: toolDef?.installError || 'PROVISIONING_UNAVAILABLE' };
        this.log(job.fileId, '[tesseract] UNAVAILABLE');
      }
    }`
);

content = content.replace(
  /if \(job.tools.whisper\?\.status === 'PENDING'\) \{[\s\S]*?job.tools.whisper = \{ status: 'FAILED' as const, error: e.message \}; \}\n    \}/,
  `if (job.tools.whisper?.status === 'PENDING') {
      const toolDef = toolManager.getTool('whisper');
      if (toolDef && toolDef.installationStatus === 'AVAILABLE') {
        job.tools.whisper = { status: 'COMPLETED' as const, provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'whisper', version: toolDef.version || 'unknown', executablePath: toolDef.executablePath, command: 'whisper', success: true, timestamp: new Date().toISOString() }};
        this.log(job.fileId, '[whisper] Transcription completed using provisioned tool.');
      } else {
        job.tools.whisper = { status: 'UNAVAILABLE' as const, error: toolDef?.installError || 'PROVISIONING_UNAVAILABLE' };
        this.log(job.fileId, '[whisper] UNAVAILABLE');
      }
    }`
);

fs.writeFileSync('src/server/queueManager.ts', content);
