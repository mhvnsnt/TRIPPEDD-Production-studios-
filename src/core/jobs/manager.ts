import { Job, JobStatus, ProjectContext, ContentProvenance, AggregateClassification } from '../types';
import { ToolRegistry } from '../tools/registry';
import { AssetRegistry } from '../assets/registry';

type JobSubscriber = (jobs: Job[]) => void;

class JobManagerImpl {
  private jobs: Map<string, Job> = new Map();
  private subscribers: Set<JobSubscriber> = new Set();

  subscribe(callback: JobSubscriber) {
    this.subscribers.add(callback);
    callback(Array.from(this.jobs.values()).reverse());
    return () => this.subscribers.delete(callback);
  }

  private notify() {
    const jobList = Array.from(this.jobs.values()).sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    ).reverse();
    this.subscribers.forEach(sub => sub(jobList));
  }

  async submitJob(toolId: string, operation: string, inputs: any, context: ProjectContext): Promise<string> {
    const adapter = ToolRegistry.getAdapter(toolId);
    if (!adapter) throw new Error(`Tool ${toolId} not found in registry`);

    const jobId = `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const job: Job = {
      id: jobId,
      projectId: context.projectId,
      toolId,
      operation,
      inputs,
      status: 'QUEUED',
      progress: 0,
      logs: [`Job ${jobId} queued for ${operation} on ${adapter.definition.name}`],
      createdAt: new Date().toISOString(),
    };

    this.jobs.set(jobId, job);
    this.notify();

    if (adapter.execute) {
      job.startedAt = new Date().toISOString();
      job.status = 'RUNNING';
      this.notify();

      adapter.execute(job, (updates: Partial<Job>) => {
        Object.assign(job, updates);
        
        if (job.status === 'COMPLETED' && job.outputs?.path && !job.outputs?.assetId) {
           job.completedAt = new Date().toISOString();
           
           let derivedProvenance: ContentProvenance = { realityStatus: 'UNKNOWN', captureStatus: 'UNKNOWN', authorship: 'UNKNOWN', generationMethods: [], assemblyMode: 'MIXED_MEDIA', aiContributions: ['NONE'], aggregate: job.toolId === 'ffmpeg' ? 'HYBRID_PRODUCTION' : 'FICTIONAL_CREATION' };
           
           let parentAssets: string[] = [];
           
           if (job.inputs.inputAssetIds && Array.isArray(job.inputs.inputAssetIds)) {
             parentAssets = job.inputs.inputAssetIds;
             const inputAssets = job.inputs.inputAssetIds.map((id: string) => AssetRegistry.getAsset(id)).filter(Boolean);
             if (inputAssets.length > 0) {
               const hasReal = inputAssets.some(a => a?.provenance.aggregate === 'REAL_PRODUCTION');
               const hasFictional = inputAssets.some(a => a?.provenance.aggregate === 'FICTIONAL_CREATION');
               if (hasReal && hasFictional) {
                 derivedProvenance.aggregate = 'HYBRID_PRODUCTION';
               } else if (hasReal) {
                 derivedProvenance.aggregate = 'REAL_PRODUCTION';
               } else if (hasFictional) {
                 derivedProvenance.aggregate = 'FICTIONAL_CREATION';
               }
             }
           }

           const newAsset = AssetRegistry.registerAsset({
            name: `${job.operation}_output_v001`,
            type: job.toolId === 'ffmpeg' && job.operation !== 'extract_frame' ? 'video' : 'image',
            path: job.outputs.path,
            projectId: job.projectId,
            sourceTool: job.toolId,
            producingJobId: job.id,
            version: 1,
            provenance: derivedProvenance,
            verificationState: 'UNVERIFIED',
            contentType: job.operation,
            status: 'AVAILABLE',
            parentAssets: parentAssets
          });
          job.outputs.assetId = newAsset.id;
          job.outputs.provenance = newAsset.provenance;
          job.logs.push(`Job completed successfully.`);
          job.logs.push(`Output registered as Asset: ${job.outputs.assetId}`);
        }
        
        this.notify();
      }).catch(e => {
        job.status = 'FAILED';
        job.logs.push(`Execution Failed: ${e.message}`);
        this.notify();
      });
    } else {
      // Fallback for tools that haven't implemented real execution yet
      this.simulateJobExecution(jobId, adapter);
    }

    return jobId;
  }

  private async simulateJobExecution(jobId: string, adapter: any) {
    const job = this.jobs.get(jobId);
    if (!job) return;

    await new Promise(r => setTimeout(r, 1000));
    job.status = 'RUNNING';
    job.startedAt = new Date().toISOString();
    job.logs.push(`Starting execution via ${adapter.definition.name}...`);
    job.progress = 10;
    this.notify();

    // Simulate progress
    for (let i = 25; i <= 90; i += 25) {
      await new Promise(r => setTimeout(r, 800));
      job.progress = i;
      job.logs.push(`Processing ${job.operation}... ${i}%`);
      this.notify();
    }

    await new Promise(r => setTimeout(r, 800));
    job.status = 'COMPLETED';
    job.progress = 100;
    job.completedAt = new Date().toISOString();
    
    // Actually register the generated asset in the Asset Registry
    const newAsset = AssetRegistry.registerAsset({
      name: `${job.operation}_output_v001`,
      type: job.operation === 'generate_audio' ? 'audio' : 'image',
      fileFormat: job.operation === 'generate_audio' ? 'wav' : 'png',
      path: `/trippedd_project/assets/generated/${job.toolId}/${job.id}_output.${job.operation === 'generate_audio' ? 'wav' : 'png'}`,
      projectId: job.projectId,
      sourceTool: job.toolId,
      producingJobId: job.id,
      version: 1,
      provenance: { realityStatus: 'UNKNOWN', captureStatus: 'UNKNOWN', authorship: 'UNKNOWN', generationMethods: [], assemblyMode: 'MIXED_MEDIA', aiContributions: ['NONE'], aggregate: 'FICTIONAL_CREATION' },
      verificationState: 'UNVERIFIED',
      contentType: job.operation,
      status: 'AVAILABLE'
    });

    job.outputs = {
      assetId: newAsset.id,
      path: newAsset.path,
      provenance: newAsset.provenance,
      contentType: newAsset.contentType
    };
    
    job.logs.push(`Job completed successfully.`);
    job.logs.push(`Output registered as Asset: ${job.outputs.assetId}`);
    this.notify();
  }

  getJobs(): Job[] {
    return Array.from(this.jobs.values()).reverse();
  }

  async waitForJob(jobId: string, timeoutMs: number = 30000): Promise<Job> {
    return new Promise((resolve, reject) => {
      const startTime = Date.now();
      const check = () => {
        const job = this.jobs.get(jobId);
        if (!job) {
          reject(new Error(`Job ${jobId} not found`));
          return;
        }
        if (job.status === 'COMPLETED') {
          resolve(job);
        } else if (job.status === 'FAILED') {
          reject(new Error(job.logs[job.logs.length - 1] || 'Job failed'));
        } else if (Date.now() - startTime > timeoutMs) {
          reject(new Error(`Job ${jobId} timed out after ${timeoutMs}ms`));
        } else {
          setTimeout(check, 500);
        }
      };
      check();
    });
  }
}

export const JobManager = new JobManagerImpl();
