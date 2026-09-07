const fs = require('fs');
let types = fs.readFileSync('src/core/types.ts', 'utf8');

const captureSessionStr = `
export type CaptureSessionStatus = 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'CANCELLED';

export interface CaptureSession {
  id: string;
  workOrderId?: string;
  productionUnitId: string;
  performanceId?: string;
  takeId?: string;
  workItemId?: string;
  status: CaptureSessionStatus;
  startTime?: string;
  endTime?: string;
  mediaReceived: boolean;
  sourceClipIds: string[];
  notes?: string;
  createdAt: string;
  updatedAt: string;
}
`;

if (!types.includes("export interface CaptureSession")) {
  types = types + '\n' + captureSessionStr;
}

types = types.replace(
  "export interface SourceClip {\n  id: string;",
  "export interface SourceClip {\n  id: string;\n  captureSessionId?: string;\n  workOrderId?: string;"
);

fs.writeFileSync('src/core/types.ts', types);
console.log("Types updated.");
