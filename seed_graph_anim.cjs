const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

const tmplAnim = `
    const tmplAnim: ProductionTemplate = {
      id: 'tmpl_animation_v1', productionTypeId: ptAnimation.id, name: 'Standard Animation V1', description: 'Default Animation workflow',
      phases: ptAnimation.defaultPhases, requirements: [rtScript], approvalGates: [], workItemTemplates: [],
      departmentAssignments: ptAnimation.defaultDepartments, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), version: 1
    };
    this.productionTemplates.set(tmplAnim.id, tmplAnim);
`;

content = content.replace("this.productionTemplates.set(tmplGenerated.id, tmplGenerated);", "this.productionTemplates.set(tmplGenerated.id, tmplGenerated);\n" + tmplAnim);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
