const fs = require('fs');

let srv = fs.readFileSync('server.ts', 'utf8');
srv = srv.replace('toolManager.getAllTools()', 'toolManager.getTools()');
fs.writeFileSync('server.ts', srv);

let toolsRoute = fs.readFileSync('src/server/toolsRoute.ts', 'utf8');
toolsRoute = toolsRoute.replace('toolManager.getAllTools()', 'toolManager.getTools()');
fs.writeFileSync('src/server/toolsRoute.ts', toolsRoute);
