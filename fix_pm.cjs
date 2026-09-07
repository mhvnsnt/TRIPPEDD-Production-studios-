const fs = require('fs');
let content = fs.readFileSync('src/components/ingest/PipelineMonitor.tsx', 'utf8');

// The issue is Object.entries(job.tools) gives [string, unknown] because job.tools is defined differently.
// Let's assert it as JobToolStatus.
content = content.replace(
  'Object.entries(job.tools).map(([name, status]) => (',
  'Object.entries(job.tools).map(([name, status]) => {\n                        const s = status as JobToolStatus;\n                        return ('
);

content = content.replace(
  /status\.status === /g,
  's.status === '
);

content = content.replace(
  /}\)`}<\/div>/g,
  '}`}></div>\n                     );})'
);
fs.writeFileSync('src/components/ingest/PipelineMonitor.tsx', content);

// And we need to fix the toolManager.ts constructor invocation
let tm = fs.readFileSync('src/server/toolManager.ts', 'utf8');
tm = tm.replace(/this\.createDef\('opencv', 'OpenCV', 'Computer vision abstraction'\)/, "this.createDef('opencv', 'OpenCV', 'Computer vision abstraction', 'PYTHON')");
fs.writeFileSync('src/server/toolManager.ts', tm);

console.log('Fixed PM and TM');
