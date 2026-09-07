const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

// Imports
content = content.replace(
  "Approval, ApprovalStatus, EventSource\n} from '../types';",
  "Approval, ApprovalStatus, EventSource,\n  CreativeDiscovery, DiscoveryStatus, DevelopmentSeed, SeedStatus,\n  CreativeDocument, DocumentVersion, DocumentType, DocumentStatus\n} from '../types';"
);

// Maps
content = content.replace(
  "public events = new Array<ProductionEvent>();\n  public approvals = new Map<string, Approval>();",
  "public events = new Array<ProductionEvent>();\n  public approvals = new Map<string, Approval>();\n  public discoveries = new Map<string, CreativeDiscovery>();\n  public seeds = new Map<string, DevelopmentSeed>();\n  public documents = new Map<string, CreativeDocument>();\n  public documentVersions = new Map<string, DocumentVersion>();"
);

// Add dev methods
const devMethods = `

  // --- CRUD for Development & Writers Room ---
  addDiscovery(discovery: CreativeDiscovery) {
    this.discoveries.set(discovery.id, discovery);
    this.logEvent({
      description: \`Discovery '\${discovery.title}' captured\`,
      type: 'INFO',
      source: 'SYSTEM',
      entityType: 'CREATIVE_DISCOVERY',
      entityId: discovery.id
    });
  }

  updateDiscoveryStatus(id: string, status: DiscoveryStatus) {
    const discovery = this.discoveries.get(id);
    if (!discovery) return;
    const prevState = discovery.status;
    discovery.status = status;
    discovery.updatedAt = new Date().toISOString();
    this.logEvent({
      description: \`Discovery '\${discovery.title}' status changed to \${status}\`,
      type: 'STATE_CHANGE',
      source: 'SYSTEM',
      entityType: 'CREATIVE_DISCOVERY',
      entityId: id,
      previousState: prevState,
      newState: status
    });
  }

  addSeed(seed: DevelopmentSeed) {
    this.seeds.set(seed.id, seed);
    this.logEvent({
      description: \`Development seed '\${seed.title}' created\`,
      type: 'INFO',
      source: 'SYSTEM',
      entityType: 'DEVELOPMENT_SEED',
      entityId: seed.id
    });
    if (seed.discoveryId) {
      this.addRelationship({
        id: \`rel_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
        sourceId: seed.id,
        sourceType: 'DEVELOPMENT_SEED',
        targetId: seed.discoveryId,
        targetType: 'CREATIVE_DISCOVERY',
        relationshipType: 'DEVELOPMENT_SEED_FROM_DISCOVERY'
      });
    }
  }

  updateSeedStatus(id: string, status: SeedStatus) {
    const seed = this.seeds.get(id);
    if (!seed) return;
    const prevState = seed.status;
    seed.status = status;
    seed.updatedAt = new Date().toISOString();
    this.logEvent({
      description: \`Seed '\${seed.title}' status changed to \${status}\`,
      type: 'STATE_CHANGE',
      source: 'SYSTEM',
      entityType: 'DEVELOPMENT_SEED',
      entityId: id,
      previousState: prevState,
      newState: status
    });
  }

  addDocument(doc: CreativeDocument) {
    this.documents.set(doc.id, doc);
  }

  addDocumentVersion(version: DocumentVersion) {
    this.documentVersions.set(version.id, version);
    const doc = this.documents.get(version.documentId);
    if (doc) {
      doc.updatedAt = version.createdAt;
      this.addRelationship({
        id: \`rel_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
        sourceId: version.id,
        sourceType: 'DOCUMENT_VERSION',
        targetId: doc.seedId,
        targetType: 'DEVELOPMENT_SEED',
        relationshipType: 'DOCUMENT_VERSION_OF_SEED'
      });
    }
  }

  getVersionsForDocument(documentId: string) {
    return Array.from(this.documentVersions.values())
      .filter(v => v.documentId === documentId)
      .sort((a, b) => b.versionNumber - a.versionNumber);
  }

  greenlightSeed(seedId: string, productionId?: string): ProductionUnit | null {
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
  }
`;

content = content.replace("  // --- CRUD for People ---", devMethods + "\n  // --- CRUD for People ---");
fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
