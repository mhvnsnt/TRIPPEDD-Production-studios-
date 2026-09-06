import { JobManager } from '../jobs/manager';
import { AssetRegistry } from '../assets/registry';

export type GagTrigger = 'MANUAL' | 'SCRIPTED' | 'RANDOM' | 'EVENT';

export interface GagDefinition {
  id: string;
  name: string;
  description: string;
  trigger: GagTrigger;
  eligibleShotTypes: string[]; // e.g., ['LIVE_ACTION', 'WATERCOLOR']
  toolRequirements: string[];
  execute: (inputAssetId: string, projectId: string, params?: any) => Promise<string>;
}

export class TrippeddGagRegistry {
  private static gags = new Map<string, GagDefinition>();

  static registerGag(gag: GagDefinition) {
    this.gags.set(gag.id, gag);
  }

  static getGag(id: string): GagDefinition | undefined {
    return this.gags.get(id);
  }

  static getAllGags(): GagDefinition[] {
    return Array.from(this.gags.values());
  }

  static async executeGag(id: string, inputAssetId: string, projectId: string, params?: any) {
    const gag = this.gags.get(id);
    if (!gag) throw new Error(`Gag ${id} not found in registry`);

    console.log(`Executing TRIPPEDD Gag: ${gag.name}`);
    return gag.execute(inputAssetId, projectId, params);
  }
}

// Register basic gags
TrippeddGagRegistry.registerGag({
  id: 'WILHELM_SCREAM',
  name: 'Wilhelm Scream',
  description: 'The classic canned scream.',
  trigger: 'RANDOM',
  eligibleShotTypes: ['ALL'],
  toolRequirements: ['ffmpeg'],
  execute: async (inputAssetId, projectId) => {
    // Overlays the Wilhelm scream audio
    const jobId = await JobManager.submitJob('ffmpeg', 'overlay_audio', {
      inputAssetId,
      audioFile: '/assets/sfx/wilhelm.wav'
    }, { projectId });
    const job = await JobManager.waitForJob(jobId);
    return job.outputs!.assetId;
  }
});

TrippeddGagRegistry.registerGag({
  id: 'TRIPPEDD_SCREAM',
  name: 'TRIPPEDD Scream',
  description: 'The recurring TRIPPEDD scream.',
  trigger: 'RANDOM',
  eligibleShotTypes: ['ALL'],
  toolRequirements: ['ffmpeg'],
  execute: async (inputAssetId, projectId) => {
    const jobId = await JobManager.submitJob('ffmpeg', 'overlay_audio', {
      inputAssetId,
      audioFile: '/assets/sfx/trippedd_scream.wav'
    }, { projectId });
    const job = await JobManager.waitForJob(jobId);
    return job.outputs!.assetId;
  }
});

TrippeddGagRegistry.registerGag({
  id: 'FREEZE_FRAME',
  name: 'Freeze Frame',
  description: 'Freezes the final frame for a set duration.',
  trigger: 'SCRIPTED',
  eligibleShotTypes: ['ALL'],
  toolRequirements: ['ffmpeg'],
  execute: async (inputAssetId, projectId, params = { duration: 3 }) => {
    const jobId = await JobManager.submitJob('ffmpeg', 'freeze_frame', {
      inputAssetId,
      duration: params.duration
    }, { projectId });
    const job = await JobManager.waitForJob(jobId);
    return job.outputs!.assetId;
  }
});

// We can move Luck of the Irish here, or keep it in EffectOrchestrator and register it.
