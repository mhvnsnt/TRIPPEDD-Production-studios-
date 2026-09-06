import { JobManager } from '../jobs/manager';
import { AssetRegistry } from '../assets/registry';
import { PerformanceCaptureManager } from './performance';

export interface PerformanceAsset {
  actorId: string;
  sourceType: 'REAL_AUDIO' | 'REAL_VIDEO' | 'GENERATED_VOICE' | 'GENERATED_ANIMATION';
  assetId?: string; // Optional if not yet recorded/generated
}

export interface ShotPerformanceNode {
  mars?: PerformanceAsset;
  tyneshia?: PerformanceAsset;
  joe?: PerformanceAsset;
}

export interface MixedMediaShot {
  id: string;
  description: string;
  performances: ShotPerformanceNode;
  environment: 'REAL_FOOTAGE' | 'GENERATED_FROM_REFERENCE' | 'GENERATED';
  style: 'REALITY' | 'TRIPPEDD_WATERCOLOR_REALITY' | 'WATERCOLOR_REALITY_TRANSITION' | 'REALITY_WATERCOLOR_TRANSITION';
  baseAssetId?: string; // Real footage reference
}

export const WATERCOLOR_STYLE_PARAMS = {
  STYLE: 'WATERCOLOUR_ON_PAPER',
  REALISM: 'SEMI_REALISTIC',
  MOTION: 'LIMITED / STOP_MOTION_FEEL',
  PAPER_TEXTURE: 'ENABLED',
  PAINT_VARIATION: 'SUBTLE',
  FRAME_IMPERFECTION: 'SUBTLE',
  LINEWORK: 'MINIMAL',
  LIGHTING: 'SOURCE_MATCHED',
  CAMERA: 'SOURCE_MATCHED'
};

export class MixedMediaOrchestrator {
  static async generateMixedMediaShot(projectId: string, shot: MixedMediaShot, characterMasterId?: string) {
    console.log(`Processing Shot [${shot.id}]: ${shot.description}`);
    
    // 1. Gather Real Performances (Authoritative Timing)
    const hasMarsReal = shot.performances.mars?.sourceType === 'REAL_AUDIO' || shot.performances.mars?.sourceType === 'REAL_VIDEO';
    const hasTyneshiaReal = shot.performances.tyneshia?.sourceType === 'REAL_AUDIO' || shot.performances.tyneshia?.sourceType === 'REAL_VIDEO';
    
    let authoritativeTimingData = null;
    let authoritativeDuration = 0;

    const realRecordings = PerformanceCaptureManager.getSelectedRecordings(shot.id);
    if (realRecordings.length > 0) {
       // We use the real recordings to drive the timing of the generated characters
       console.log(`Found ${realRecordings.length} real performance recording(s) for shot ${shot.id}`);
       const mainRecording = realRecordings[0];
       authoritativeTimingData = await PerformanceCaptureManager.extractPerformanceTiming(mainRecording);
       authoritativeDuration = authoritativeTimingData.duration;
    }
    
    // 2. Generate Missing Character Performances
    let joeAssetId = null;
    if (shot.performances.joe?.sourceType.startsWith('GENERATED')) {
      const joeJobId = await JobManager.submitJob('comfyui', 'generate_character_performance', {
        prompt: "Joe performance generation based on real actor timing and dialogue",
        characterMasterId: characterMasterId,
        timingReference: shot.baseAssetId || 'SCENE_TIMING',
        authoritativeTimingData: authoritativeTimingData,
        targetDuration: authoritativeDuration
      }, { projectId });
      const joeJob = await JobManager.waitForJob(joeJobId);
      joeAssetId = joeJob.outputs!.assetId;
    }

    // 3. Apply Visual Treatment / Environment
    let finalShotAssetId = null;
    let finalShotPath = null;
    if (shot.style === 'TRIPPEDD_WATERCOLOR_REALITY') {
      const renderJobId = await JobManager.submitJob('comfyui', 'apply_watercolor_treatment', {
        styleParams: WATERCOLOR_STYLE_PARAMS,
        inputAssetIds: [joeAssetId, shot.baseAssetId].filter(Boolean) as string[]
      }, { projectId });
      const renderJob = await JobManager.waitForJob(renderJobId);
      finalShotAssetId = renderJob.outputs!.assetId;
      finalShotPath = renderJob.outputs!.path;
    } else if (shot.style.includes('TRANSITION')) {
      const transJobId = await JobManager.submitJob('comfyui', 'watercolor_bleed_transition', {
        direction: shot.style === 'REALITY_WATERCOLOR_TRANSITION' ? 'TO_WATERCOLOR' : 'TO_REALITY',
        inputAssetIds: [shot.baseAssetId].filter(Boolean) as string[]
      }, { projectId });
      const transJob = await JobManager.waitForJob(transJobId);
      finalShotAssetId = transJob.outputs!.assetId;
      finalShotPath = transJob.outputs!.path;
    } else {
      // REALITY
      finalShotAssetId = shot.baseAssetId;
      finalShotPath = AssetRegistry.getAsset(shot.baseAssetId!)?.path;
    }

    // 4. Composite (If Hybrid)
    // For now, if we have a generated part and a real part, composite them.
    if ((hasMarsReal || hasTyneshiaReal) && joeAssetId && shot.style === 'TRIPPEDD_WATERCOLOR_REALITY') {
       const compJobId = await JobManager.submitJob('ffmpeg', 'composite_mixed_media', {
          videoPath: finalShotPath,
          inputAssetIds: [finalShotAssetId]
       }, { projectId });
       const compJob = await JobManager.waitForJob(compJobId);
       finalShotAssetId = compJob.outputs!.assetId;
       finalShotPath = compJob.outputs!.path;
    }

    return {
      assetId: finalShotAssetId,
      path: finalShotPath
    };
  }

  static async assembleScene(projectId: string, sceneId: string, shotAssetIds: string[]) {
    const concatJobId = await JobManager.submitJob('ffmpeg', 'concatenate_sequence', {
      segments: shotAssetIds, // Simulated paths logic inside adapter
      inputAssetIds: shotAssetIds
    }, { projectId });
    const concatJob = await JobManager.waitForJob(concatJobId);
    return concatJob.outputs!.assetId;
  }
}
