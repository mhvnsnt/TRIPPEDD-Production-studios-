const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

const oldGreenlight = `  greenlightSeed(seedId: string, productionId?: string): ProductionUnit | null {
    const seed = this.seeds.get(seedId);
    if (!seed) return null;

    this.updateSeedStatus(seedId, 'GREENLIT');

    const unit: ProductionUnit = {
      id: productionId || \`pu_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
      type: seed.targetProductionType as any || 'OTHER',
      name: seed.title,
      description: seed.logline || seed.premise,
      status: 'DEVELOPMENT',
      concept: seed.premise
    };

    this.addProductionUnit(unit);

    this.addRelationship({
      id: \`rel_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
      sourceId: unit.id,
      sourceType: 'PRODUCTION_UNIT',
      targetId: seedId,
      targetType: 'DEVELOPMENT_SEED',
      relationshipType: 'PRODUCTION_CREATED_FROM_SEED'
    });

    this.logEvent({
      description: \`Production '\${unit.name}' created from seed\`,
      type: 'PRODUCTION_CREATED_FROM_SEED',
      source: 'SYSTEM',
      entityType: 'PRODUCTION_UNIT',
      entityId: unit.id,
      metadata: { seedId }
    });

    return unit;
  }`;

const newGreenlight = `  greenlightSeed(seedId: string, productionId?: string): ProductionUnit | null {
    const seed = this.seeds.get(seedId);
    if (!seed) return null;

    this.updateSeedStatus(seedId, 'GREENLIT');

    // 1. Determine target ProductionType
    const typeCode = seed.targetProductionType;
    const prodType = Array.from(this.productionTypes.values()).find(pt => pt.code === typeCode) || this.productionTypes.get('pt_live_action_sketch');
    
    // 2. Select applicable ProductionTemplate
    const template = Array.from(this.productionTemplates.values()).find(t => t.productionTypeId === prodType?.id);

    const unit: ProductionUnit = {
      id: productionId || \`pu_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
      type: (prodType ? prodType.code : 'OTHER') as any,
      templateId: template?.id,
      name: seed.title,
      description: seed.logline || seed.premise,
      status: 'DEVELOPMENT',
      concept: seed.premise
    };

    this.addProductionUnit(unit);

    // 4. Instantiate applicable requirements from template
    if (template) {
      template.requirements.forEach(reqTmpl => {
        const req: any = {
          id: \`req_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
          productionUnitId: unit.id,
          type: reqTmpl.code as any, // Using code as type for now
          description: reqTmpl.description,
          status: 'OPEN',
          requiredByStage: reqTmpl.applicablePhases[0] || 'SHOOTING',
          blocking: reqTmpl.blocking,
        };
        this.addRequirement(req);
      });
    }

    this.addRelationship({
      id: \`rel_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
      sourceId: unit.id,
      sourceType: 'PRODUCTION_UNIT',
      targetId: seedId,
      targetType: 'DEVELOPMENT_SEED',
      relationshipType: 'PRODUCTION_CREATED_FROM_SEED'
    });

    this.logEvent({
      description: \`Production '\${unit.name}' created from seed using template \${template?.name || 'none'}\`,
      type: 'PRODUCTION_CREATED_FROM_SEED',
      source: 'SYSTEM',
      entityType: 'PRODUCTION_UNIT',
      entityId: unit.id,
      metadata: { seedId, templateId: template?.id }
    });

    return unit;
  }`;

content = content.replace(oldGreenlight, newGreenlight);
fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
console.log("Greenlight updated.");
