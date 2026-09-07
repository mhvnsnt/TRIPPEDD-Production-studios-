const fs = require('fs');

let content = fs.readFileSync('src/server/queueManager.ts', 'utf8');
if (!content.includes('import { toolManager }')) {
  content = content.replace('import { MediaJob, QueueJobState } from "../core/types";', 'import { MediaJob, QueueJobState } from "../core/types";\nimport { toolManager } from "./toolManager";');
}
fs.writeFileSync('src/server/queueManager.ts', content);
