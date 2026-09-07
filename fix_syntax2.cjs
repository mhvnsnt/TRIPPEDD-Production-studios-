const fs = require('fs');

let content = fs.readFileSync('src/components/ingest/PipelineMonitor.tsx', 'utf8');

content = content.replace(
  '                        }`></div>\n                     ))}',
  '                        }`></div>\n                     );})}'
);
content = content.replace('))}',');})}');

// Fix s.status in first render JobToolStatus
content = content.replace(
  /s\.status === /g,
  'status.status === '
);

content = content.replace(
  'Object.entries(job.tools).map(([name, status]) => {\\n                        const s = status as JobToolStatus;\\n                        return (',
  'Object.entries(job.tools).map(([name, statusRaw]) => { const status = statusRaw as JobToolStatus; return ('
);

fs.writeFileSync('src/components/ingest/PipelineMonitor.tsx', content);
