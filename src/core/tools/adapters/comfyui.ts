import { ToolAdapter, ToolStatus, ToolDefinition, Job } from '../../types';

export class ComfyUIAdapter implements ToolAdapter {
  id = 'comfyui';
  definition: ToolDefinition = {
    id: 'comfyui',
    name: 'ComfyUI',
    category: 'AI',
    description: 'AI image/video generation and node-based AI pipelines',
    license: 'GPLv3',
    installationStatus: 'NOT_CHECKED' as ToolStatus,
    integrationType: 'LOCAL_SERVICE' as const,
    capabilities: {
      canLaunch: false,
      canOpenProject: true,
      canImportAsset: true,
      canExportAsset: true,
      canSubmitJob: true
    },
    healthStatus: 'NOT_CHECKED' as ToolStatus
  };

  async detect(): Promise<ToolStatus> {
    try {
      const res = await fetch('/api/tools/comfyui/detect');
      if (res.ok) {
        const data = await res.json();
        if (data.installed) {
          return 'CONNECTED';
        }
      }
      return 'NOT_INSTALLED';
    } catch (e) {
      return 'NOT_INSTALLED';
    }
  }

  async healthCheck(): Promise<ToolStatus> {
    return this.detect();
  }

  async execute(job: Job, onUpdate: (update: Partial<Job>) => void): Promise<void> {
    const outputPath = `/trippedd_project/assets/generated/comfyui/${job.id}_out.png`;
    
    // Construct fake workflow based on inputs (or use a real one if provided)
    const workflow = job.inputs.workflow || {
      "3": {
        "class_type": "KSampler",
        "inputs": {
          "seed": Math.floor(Math.random() * 1000000),
          "prompt": job.inputs.prompt || "default prompt"
        }
      }
    };

    try {
      const res = await fetch('/api/jobs/comfyui', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workflow, output_path: outputPath })
      });
      const { jobId } = await res.json();
      
      // Polling loop
      while (true) {
        await new Promise(r => setTimeout(r, 500));
        const statusRes = await fetch(`/api/jobs/${jobId}`);
        const data = await statusRes.json();
        
        const update: Partial<Job> = {
          status: data.status,
          progress: data.progress,
          logs: data.logs || []
        };
        
        if (data.result) {
          update.outputs = { path: data.result.path };
        }
        
        onUpdate(update);
        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          break;
        }
      }
    } catch (e: any) {
      onUpdate({ status: 'FAILED', logs: [...(job.logs || []), `Error: ${e.message}`] });
    }
  }
}
