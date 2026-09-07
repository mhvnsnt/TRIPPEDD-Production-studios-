const fs = require('fs');

let content = fs.readFileSync('server.ts', 'utf8');
if (!content.includes('import { toolManager }')) {
  content = content.replace('import express from "express";', 'import express from "express";\nimport { toolManager } from "./src/server/toolManager";\nimport { queueManager } from "./src/server/queueManager";');
}
fs.writeFileSync('server.ts', content);
