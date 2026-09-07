const fs = require('fs');

let seed = fs.readFileSync('src/core/pipeline/seed.ts', 'utf8');
seed = seed.replace(/title: 'Draft Series Bible',/g, "title: 'Draft Series Bible', description: 'desc',");
fs.writeFileSync('src/core/pipeline/seed.ts', seed);
