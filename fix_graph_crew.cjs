const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

// 1. Add Maps
content = content.replace(
  "takes = new Map<string, Take>();",
  "takes = new Map<string, Take>();\n  crewAssignments = new Map<string, CrewAssignment>();\n  workOrders = new Map<string, WorkOrder>();"
);

// 2. Add imports
content = content.replace(
  "import {",
  "import { CrewAssignment, WorkOrder, CrewAssignmentStatus, WorkOrderStatus, Department, "
);

// 3. Add CRUD methods for CrewAssignment and WorkOrder
const crudMethods = `
  // --- Crew Assignment ---
  addCrewAssignment(assignment: CrewAssignment): void {
    this.crewAssignments.set(assignment.id, assignment);
    this.appendEvent({
      type: 'CREW_ASSIGNED',
      productionUnitId: assignment.productionUnitId,
      entityType: 'CREW_ASSIGNED',
      entityId: assignment.id,
      newState: assignment.status,
      description: \`Assigned person \${assignment.personId} to role \${assignment.role}\`
    });
  }

  updateCrewAssignmentStatus(assignmentId: string, status: CrewAssignmentStatus, notes?: string): void {
    const assignment = this.crewAssignments.get(assignmentId);
    if (!assignment) return;
    const oldStatus = assignment.status;
    assignment.status = status;
    if (notes) assignment.notes = notes;
    this.crewAssignments.set(assignmentId, assignment);

    let eventType: any = 'INFO';
    if (status === 'CONFIRMED') eventType = 'CREW_CONFIRMED';
    if (status === 'CANCELLED') eventType = 'CREW_RELEASED'; // Mapping logic
    if (status === 'COMPLETED') eventType = 'CREW_RELEASED';
    if (status === 'ACTIVE') eventType = 'STATE_CHANGE';

    this.appendEvent({
      type: eventType,
      productionUnitId: assignment.productionUnitId,
      entityType: 'CREW_ASSIGNED',
      entityId: assignmentId,
      previousState: oldStatus,
      newState: status,
      description: \`Crew assignment \${assignmentId} status changed to \${status}\`
    });
  }

  // --- Work Order ---
  addWorkOrder(order: WorkOrder): void {
    this.workOrders.set(order.id, order);
    this.appendEvent({
      type: 'WORK_ORDER_CREATED',
      productionUnitId: order.productionUnitId,
      entityType: 'WORK_ORDER',
      entityId: order.id,
      newState: order.status,
      description: \`Created WorkOrder \${order.id} for phase \${order.phase}\`
    });
  }

  updateWorkOrderStatus(orderId: string, status: WorkOrderStatus): void {
    const order = this.workOrders.get(orderId);
    if (!order) return;
    const oldStatus = order.status;
    order.status = status;
    order.updatedAt = new Date().toISOString();
    this.workOrders.set(orderId, order);

    let eventType: any = 'INFO';
    if (status === 'SCHEDULED') eventType = 'WORK_ORDER_SCHEDULED';
    if (status === 'IN_PROGRESS') eventType = 'WORK_ORDER_STARTED';
    if (status === 'BLOCKED') eventType = 'WORK_ORDER_BLOCKED';
    if (status === 'COMPLETED') eventType = 'WORK_ORDER_COMPLETED';
    if (status === 'CANCELLED') eventType = 'WORK_ORDER_CANCELLED';

    this.appendEvent({
      type: eventType,
      productionUnitId: order.productionUnitId,
      entityType: 'WORK_ORDER',
      entityId: orderId,
      previousState: oldStatus,
      newState: status,
      description: \`WorkOrder \${orderId} status changed to \${status}\`
    });
  }

  checkScheduleConflicts(startDate: string, endDate: string): any[] {
    const conflicts: any[] = [];
    const start = new Date(startDate).getTime();
    const end = new Date(endDate).getTime();

    // Check Person overlapping assignments
    const personAssignments = new Map<string, any[]>();
    
    // We check work orders for location overlap, and crew assignments for person overlap
    
    for (const ca of this.crewAssignments.values()) {
       if (ca.status === 'CANCELLED' || !ca.startAt || !ca.endAt) continue;
       const caStart = new Date(ca.startAt).getTime();
       const caEnd = new Date(ca.endAt).getTime();
       if (caStart < end && caEnd > start) {
         if (!personAssignments.has(ca.personId)) personAssignments.set(ca.personId, []);
         personAssignments.get(ca.personId)!.push(ca);
       }
    }
    
    for (const [personId, assignments] of personAssignments.entries()) {
      if (assignments.length > 1) {
         conflicts.push({
           type: 'PERSON_OVERLAP',
           personId,
           description: \`Person \${personId} is assigned to overlapping work\`,
           assignments
         });
         this.appendEvent({
           type: 'SCHEDULE_CONFLICT_DETECTED',
           entityType: 'PERSON',
           entityId: personId,
           description: \`Person \${personId} is assigned to overlapping work\`
         });
      }
    }

    const locOrders = new Map<string, any[]>();
    for (const wo of this.workOrders.values()) {
      if (wo.status === 'CANCELLED' || !wo.scheduledStart || !wo.scheduledEnd || !wo.locationId) continue;
      const woStart = new Date(wo.scheduledStart).getTime();
      const woEnd = new Date(wo.scheduledEnd).getTime();
      if (woStart < end && woEnd > start) {
         if (!locOrders.has(wo.locationId)) locOrders.set(wo.locationId, []);
         locOrders.get(wo.locationId)!.push(wo);
      }
    }

    for (const [locationId, wos] of locOrders.entries()) {
      if (wos.length > 1) {
         conflicts.push({
           type: 'LOCATION_OVERLAP',
           locationId,
           description: \`Location \${locationId} is assigned to overlapping work\`,
           workOrders: wos
         });
         this.appendEvent({
           type: 'SCHEDULE_CONFLICT_DETECTED',
           entityType: 'LOCATION',
           entityId: locationId,
           description: \`Location \${locationId} is assigned to overlapping work\`
         });
      }
    }

    return conflicts;
  }
`;

content = content.replace(
  "// --- Helper Methods ---",
  crudMethods + "\n  // --- Helper Methods ---"
);

// We need to inject WorkOrder logic into the getDependencyChain logic.
let depLogic = `
        if (req.ownerRoleId) {
          chain.push({
             type: 'ROLE',
             id: req.ownerRoleId,
             status: 'PENDING_ASSIGNMENT'
          });
        }
`;

let insertDepLogic = `
        if (req.ownerRoleId) {
          chain.push({
             type: 'ROLE',
             id: req.ownerRoleId,
             status: 'PENDING_ASSIGNMENT'
          });
        }
        
        // Find if any WorkItems exist for this requirement (assuming a mapping convention, for now we will check work orders for dependencies on requirement)
        // More robust: traversing from WorkItems to WorkOrders to Assignments
        for (const wo of this.workOrders.values()) {
           if (wo.productionUnitId === unitId && wo.dependencies.includes(req.id)) {
             chain.push({
               type: 'WORK_ORDER',
               id: wo.id,
               status: wo.status,
               description: wo.title
             });
             if (wo.status === 'BLOCKED') {
               // Check if there are crew assignments for this WO
               for (const ca of this.crewAssignments.values()) {
                  if (ca.workItemId === wo.workItemId || ca.workItemId === wo.id) {
                     chain.push({
                       type: 'CREW_ASSIGNMENT',
                       id: ca.id,
                       status: ca.status,
                       description: ca.role
                     });
                  }
               }
             }
           }
        }
`;

content = content.replace(depLogic, insertDepLogic);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
