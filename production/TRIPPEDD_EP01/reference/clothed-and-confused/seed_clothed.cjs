const fs = require('fs');

let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

const seededClothed = `
    // Add Clothed and Confused Seed and Greenlight it
    const clothedSeed = {
      id: 'seed_clothed',
      title: 'Clothed and Confused',
      logline: 'A survivalist who refuses to get naked tries to survive the wilderness while wearing 14 layers of clothing.',
      premise: 'A parody of survival shows.',
      format: 'Episodic',
      targetProductionType: 'GENERATED_MEDIA',
      characters: ['Survivalist', 'Narrator', 'Field Producer'],
      setting: 'The Woods',
      tone: 'Absurd, deadpan',
      referenceRefs: [],
      sourceEvidenceRefs: [],
      status: 'IDEA',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    this.addSeed(clothedSeed);
    
    // Greenlight it
    const clothedUnit = this.greenlightSeed(clothedSeed.id, 'pu_clothed');
    
    if (clothedUnit) {
      // 1. Characters
      const charSurvivalist = { id: 'char_surv', productionUnitId: clothedUnit.id, name: 'Fictional Survivalist', description: 'Wears 14 layers.', characterType: 'FICTIONAL', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const charNarrator = { id: 'char_narr', productionUnitId: clothedUnit.id, name: 'Fictional Narrator', description: 'Deadpan British narrator.', characterType: 'FICTIONAL', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const charProducer = { id: 'char_prod', productionUnitId: clothedUnit.id, name: 'Fictional Field Producer', description: 'Always stressed.', characterType: 'FICTIONAL', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      
      this.addCharacter(charSurvivalist);
      this.addCharacter(charNarrator);
      this.addCharacter(charProducer);

      // 2. Performances
      const perfRaft = { id: 'perf_raft', productionUnitId: clothedUnit.id, characterId: charSurvivalist.id, performerType: 'GENERATED', status: 'PLANNED', notes: 'survivalist builds an unnecessarily complicated raft', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const perfWater = { id: 'perf_water', productionUnitId: clothedUnit.id, characterId: charSurvivalist.id, performerType: 'GENERATED', status: 'PLANNED', notes: 'survivalist attempts to navigate shallow water', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const perfPig = { id: 'perf_pig', productionUnitId: clothedUnit.id, characterId: charSurvivalist.id, performerType: 'GENERATED', status: 'PLANNED', notes: 'survivalist attempts to catch a fictional pig', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const perfNarrate = { id: 'perf_narrate', productionUnitId: clothedUnit.id, characterId: charNarrator.id, performerType: 'GENERATED', status: 'PLANNED', notes: 'narrator describes the situation with absurd seriousness', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };

      this.addPerformance(perfRaft);
      this.addPerformance(perfWater);
      this.addPerformance(perfPig);
      this.addPerformance(perfNarrate);
    }
`;

content = content.replace(
  "this.productionTemplates.set(tmplAnim.id, tmplAnim);",
  "this.productionTemplates.set(tmplAnim.id, tmplAnim);\n" + seededClothed
);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
console.log("Clothed and Confused seeded");
