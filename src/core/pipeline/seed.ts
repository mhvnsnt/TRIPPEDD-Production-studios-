
import { globalGraph, globalPhysicalTimeline } from './state';
import { WorkOrder, CaptureSession, SourceClip } from '../types';

export function seedPhysicalEvidence() {
  // Clear existing if any (for hot reloads)
  globalPhysicalTimeline.getTimeline().clips = [];
  globalPhysicalTimeline.getTimeline().observations = {};
  (globalPhysicalTimeline.getTimeline() as any).chronologyRelationships = [];

  const wo: WorkOrder = {
    id: 'WO_SCENE_1',
    productionUnitId: 'TRIPPEDD_PROD',
    phase: 'SHOOTING',
    status: 'IN_PROGRESS',
    title: 'Scene 1: Bag Incident', description: 'desc',
    departmentId: 'CAMERA',
    priority: 'HIGH',
    dependencies: [],
    requiredAssets: [],
    outputRefs: [],
    evidenceRefs: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  globalGraph.addWorkOrder(wo);

  // We leave the clips empty because we haven't actually ingested the real Drive files yet.
  // The system must NOT fabricate clips that haven't been truly ingested.
}
