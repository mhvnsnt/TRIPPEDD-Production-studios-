const fs = require('fs');
let graph = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

graph = graph.replace(
  "import { CrewAssignment, WorkOrder, CrewAssignmentStatus, WorkOrderStatus, Department, Person, PersonRole, ",
  "import { CaptureSession, CaptureSessionStatus, CrewAssignment, WorkOrder, CrewAssignmentStatus, WorkOrderStatus, Department, Person, PersonRole, "
);

graph = graph.replace(
  "public workOrders = new Map<string, WorkOrder>();",
  "public workOrders = new Map<string, WorkOrder>();\n  public captureSessions = new Map<string, CaptureSession>();"
);

const captureCrud = `
  // --- Capture Sessions ---
  addCaptureSession(session: CaptureSession): void {
    this.captureSessions.set(session.id, session);
    this.events.push({ id: crypto.randomUUID(), 
      type: 'CAPTURE_SESSION_CREATED' as any,
      productionUnitId: session.productionUnitId,
      entityType: 'CAPTURE_SESSION',
      entityId: session.id,
      newState: session.status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: \`Created Capture Session \${session.id} for WorkOrder \${session.workOrderId}\`
    });
  }

  updateCaptureSessionStatus(sessionId: string, status: CaptureSessionStatus): void {
    const session = this.captureSessions.get(sessionId);
    if (!session) return;
    const oldStatus = session.status;
    session.status = status;
    session.updatedAt = new Date().toISOString();
    this.captureSessions.set(sessionId, session);
    
    this.events.push({ id: crypto.randomUUID(), 
      type: 'STATE_CHANGE',
      productionUnitId: session.productionUnitId,
      entityType: 'CAPTURE_SESSION',
      entityId: sessionId,
      previousState: oldStatus,
      newState: status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: \`Capture Session \${sessionId} status changed to \${status}\`
    });
  }
  
  linkSourceClipToCaptureSession(sessionId: string, clipId: string): void {
    const session = this.captureSessions.get(sessionId);
    if (!session) return;
    if (!session.sourceClipIds.includes(clipId)) {
      session.sourceClipIds.push(clipId);
      session.mediaReceived = true;
      session.updatedAt = new Date().toISOString();
      this.captureSessions.set(sessionId, session);
      
      this.events.push({ id: crypto.randomUUID(), 
        type: 'MEDIA_INGESTED' as any,
        productionUnitId: session.productionUnitId,
        entityType: 'CAPTURE_SESSION',
        entityId: sessionId,
        source: 'SYSTEM',
        createdAt: new Date().toISOString(),
        timestamp: new Date().toISOString(),
        description: \`SourceClip \${clipId} linked to CaptureSession \${sessionId}\`
      });
    }
  }
`;

graph = graph.replace(
  "// --- Events ---",
  captureCrud + "\n  // --- Events ---"
);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', graph);
console.log("Graph updated with capture sessions.");
