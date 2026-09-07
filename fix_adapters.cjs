const fs = require('fs');

// Create a dummy orchestrator for the UI so it doesn't import child_process
let pipelineCode = fs.readFileSync('src/core/pipeline/MediaIngestPipeline.ts', 'utf8');
pipelineCode = pipelineCode.replace("import { ToolchainOrchestrator } from '../adapters/ToolchainOrchestrator';", "");
pipelineCode = pipelineCode.replace("private orchestrator: ToolchainOrchestrator = new ToolchainOrchestrator()", "private orchestrator: any = {}");

fs.writeFileSync('src/core/pipeline/MediaIngestPipeline.ts', pipelineCode);

let stateCode = fs.readFileSync('src/core/pipeline/state.ts', 'utf8');
stateCode = stateCode.replace("new MediaIngestPipeline(globalGraph, globalPhysicalTimeline);", "new MediaIngestPipeline(globalGraph, globalPhysicalTimeline, {} as any);");
fs.writeFileSync('src/core/pipeline/state.ts', stateCode);
console.log("Removed ToolchainOrchestrator from frontend imports");
