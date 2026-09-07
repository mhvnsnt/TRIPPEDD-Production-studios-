const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/__tests__/workOrders.test.ts', 'utf8');

content = content.replace(/\/\/roles:/g, "roles:");
content = content.replace(/roles: \[\],/g, "");

fs.writeFileSync('src/core/pipeline/__tests__/workOrders.test.ts', content);
