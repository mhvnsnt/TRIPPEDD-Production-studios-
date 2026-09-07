const fs = require('fs');

let content = fs.readFileSync('src/components/ingest/PipelineMonitor.tsx', 'utf8');

content = content.replace(
  '                        }`></div>\n                     ))}',
  '                        }`></div>\n                        );\n                     })}'
);

fs.writeFileSync('src/components/ingest/PipelineMonitor.tsx', content);
