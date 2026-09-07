const fs = require('fs');
let content = fs.readFileSync('server.ts', 'utf8');

if (!content.includes('import { toolManager }')) {
  content = content.replace("import { queueManager } from './src/server/queueManager';", "import { queueManager } from './src/server/queueManager';\nimport { toolManager } from './src/server/toolManager';");
}

if (!content.includes('await toolManager.initialize()')) {
  content = content.replace("async function startServer() {", "async function startServer() {\n  try { await toolManager.initialize(); } catch(e) { console.error(e); }");
}

fs.writeFileSync('server.ts', content);
