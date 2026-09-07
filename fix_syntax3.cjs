const fs = require('fs');

let content = fs.readFileSync('src/components/ingest/PipelineMonitor.tsx', 'utf8');

content = content.replace(
  'Object.entries(job.tools).map(([name, status]) => {\n                        const s = status as JobToolStatus;\n                        return (\n                        <div key={name} title={name} className={`w-2 h-2 rounded-full ${\n                          status.status === \'COMPLETED\' ? \'bg-green-500\' :\n                          status.status === \'UNAVAILABLE\' ? \'bg-neutral-700\' :\n                          status.status === \'FAILED\' ? \'bg-red-500\' : \'bg-yellow-500 animate-pulse\'\n                        }`}></div>\n                     );})}',
  'Object.entries(job.tools).map(([name, statusRaw]) => { const status = statusRaw as JobToolStatus; return (\n                        <div key={name} title={name} className={`w-2 h-2 rounded-full ${\n                          status.status === \'COMPLETED\' ? \'bg-green-500\' :\n                          status.status === \'UNAVAILABLE\' ? \'bg-neutral-700\' :\n                          status.status === \'FAILED\' ? \'bg-red-500\' : \'bg-yellow-500 animate-pulse\'\n                        }`}></div>\n                     );})}'
);

fs.writeFileSync('src/components/ingest/PipelineMonitor.tsx', content);
