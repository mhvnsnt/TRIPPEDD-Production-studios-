import { ProductionGraph } from './productionGraph';
import { PhysicalTimelineManager } from './physicalTimeline';
import { MediaIngestPipeline } from './MediaIngestPipeline';

// Global singleton instances for the app UI to share state
export const globalGraph = (ProductionGraph as any).getInstance() as ProductionGraph;
export const globalPhysicalTimeline = new PhysicalTimelineManager();
export const globalMediaIngest = new MediaIngestPipeline(globalGraph, globalPhysicalTimeline, {} as any);
