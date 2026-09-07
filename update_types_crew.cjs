const fs = require('fs');

let content = fs.readFileSync('src/core/types.ts', 'utf8');

const crewAssignmentsStr = `
export type CrewAssignmentStatus = 'PLANNED' | 'CONFIRMED' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';

export interface CrewAssignment {
  id: string;
  productionUnitId: string;
  personId: string;
  departmentId: string;
  role: string;
  workItemId?: string;
  startAt?: string;
  endAt?: string;
  status: CrewAssignmentStatus;
  notes?: string;
}

export type WorkOrderStatus = 'DRAFT' | 'READY' | 'SCHEDULED' | 'IN_PROGRESS' | 'BLOCKED' | 'COMPLETED' | 'CANCELLED';

export interface WorkOrder {
  id: string;
  productionUnitId: string;
  workItemId?: string;
  phase: string; // ProductionUnitStatus technically, but keeping it string for flexibility or ProductionUnitStatus
  title: string;
  description: string;
  departmentId: string;
  responsiblePersonId?: string;
  status: WorkOrderStatus;
  priority: WorkItemPriority;
  scheduledStart?: string;
  scheduledEnd?: string;
  locationId?: string;
  dependencies: string[];
  requiredAssets: string[];
  outputRefs: string[];
  evidenceRefs: string[];
  createdAt: string;
  updatedAt: string;
}
`;

// Insert the new types before // --- Production Types & Templates ---
content = content.replace('// --- Production Types & Templates ---', crewAssignmentsStr + '\n// --- Production Types & Templates ---');

// Add departments to Department if they are missing
// Wait, Department is already in there somewhere. Let's see what departments exist.
fs.writeFileSync('src/core/types.ts', content);
