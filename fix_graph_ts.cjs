const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

content = content.replace("status: 'IDEA',", "status: 'IDEA' as any,");
content = content.replace("characterType: 'FICTIONAL',", "characterType: 'FICTIONAL' as any,");
content = content.replace("characterType: 'FICTIONAL',", "characterType: 'FICTIONAL' as any,");
content = content.replace("characterType: 'FICTIONAL',", "characterType: 'FICTIONAL' as any,");
content = content.replace("performerType: 'GENERATED',", "performerType: 'GENERATED' as any,");
content = content.replace("performerType: 'GENERATED',", "performerType: 'GENERATED' as any,");
content = content.replace("performerType: 'GENERATED',", "performerType: 'GENERATED' as any,");
content = content.replace("performerType: 'GENERATED',", "performerType: 'GENERATED' as any,");
content = content.replace("status: 'PLANNED',", "status: 'PLANNED' as any,");
content = content.replace("status: 'PLANNED',", "status: 'PLANNED' as any,");
content = content.replace("status: 'PLANNED',", "status: 'PLANNED' as any,");
content = content.replace("status: 'PLANNED',", "status: 'PLANNED' as any,");

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
