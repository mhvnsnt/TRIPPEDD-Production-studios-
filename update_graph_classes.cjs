const fs = require('fs');

let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

// Update imports
content = content.replace(
  "WorkItemTemplate\n} from '../types';",
  "WorkItemTemplate,\n  CastAssignment, Performance, Take\n} from '../types';"
);

// Add Maps
content = content.replace(
  "public requirements = new Map<string, ProductionRequirement>();",
  "public requirements = new Map<string, ProductionRequirement>();\n  public castAssignments = new Map<string, CastAssignment>();\n  public performances = new Map<string, Performance>();\n  public takes = new Map<string, Take>();"
);

// Add CRUD for new entities
const newCRUD = `
  // --- CRUD for CastAssignments ---
  addCastAssignment(ca: CastAssignment) { this.castAssignments.set(ca.id, ca); }
  updateCastAssignmentStatus(id: string, status: any, notes?: string) {
    const ca = this.castAssignments.get(id);
    if (ca) {
      ca.status = status;
      if (notes) ca.roleNotes = notes;
      this.logEvent({
        description: \`Cast assignment for \${ca.characterId} marked as \${status}\`,
        type: 'CASTING_' + status as any,
        source: 'SYSTEM',
        productionUnitId: ca.productionUnitId,
        entityType: 'CAST_ASSIGNMENT',
        entityId: ca.id,
      });
    }
  }

  // --- CRUD for Performances ---
  addPerformance(perf: Performance) { this.performances.set(perf.id, perf); }
  updatePerformanceStatus(id: string, status: any, notes?: string) {
    const perf = this.performances.get(id);
    if (perf) {
      perf.status = status;
      if (notes) perf.notes = notes;
      this.logEvent({
        description: \`Performance \${perf.id} marked as \${status}\`,
        type: 'PERFORMANCE_' + status as any,
        source: 'SYSTEM',
        productionUnitId: perf.productionUnitId,
        entityType: 'PERFORMANCE',
        entityId: perf.id,
      });
    }
  }

  // --- CRUD for Takes ---
  addTake(take: Take) {
    this.takes.set(take.id, take);
    const perf = this.performances.get(take.performanceId);
    this.logEvent({
      description: \`Take \${take.takeNumber} created for performance \${take.performanceId}\`,
      type: 'TAKE_CREATED',
      source: 'SYSTEM',
      productionUnitId: perf?.productionUnitId,
      entityType: 'TAKE',
      entityId: take.id,
    });
  }
`;

content = content.replace(
  "// --- CRUD for Characters ---",
  newCRUD + "\n  // --- CRUD for Characters ---"
);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
console.log("Graph classes updated");
