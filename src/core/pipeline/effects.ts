import { JobManager } from '../jobs/manager';
import { AssetRegistry } from '../assets/registry';

export interface LuckOfTheIrishParams {
  irisColor?: string;
  irisThickness?: number;
  openingClosingDirection?: 'in' | 'out';
  centerPosition?: { x: number, y: number };
  timing?: number;
  easing?: string;
  freezeFrameTiming?: number;
  optionalSparkleGlow?: boolean;
  optionalCommercialTitleReveal?: boolean;
  characterPrompt?: string;
}

export interface CommercialPackageParams {
  sceneAssetId: string;
  luckParams?: LuckOfTheIrishParams;
  titlePrompt?: string;
  disclaimerPrompt?: string;
  projectId: string;
}

export class EffectOrchestrator {
  static async runLuckOfTheIrish(basePlateId: string, projectId: string, parameters: LuckOfTheIrishParams = {}) {
    console.log("Starting LUCK OF THE IRISH Pipeline for Asset:", basePlateId);
    
    const plate = AssetRegistry.getAsset(basePlateId);
    if (!plate) throw new Error(`Base plate ${basePlateId} not found in registry`);

    try {
      // 1. Extract Frame
      const extJobId = await JobManager.submitJob('ffmpeg', 'extract_frame', {
        videoPath: plate.path,
        inputAssetIds: [plate.id]
      }, { projectId });
      const extJob = await JobManager.waitForJob(extJobId);
      const frameAssetId = extJob.outputs!.assetId;

      // 2. Transform Frame (ComfyUI)
      const transformJobId = await JobManager.submitJob('comfyui', 'transform_character', {
        prompt: parameters.characterPrompt || "Hood Leprechaun, 8k, photorealistic, glowing green iris",
        inputAssetIds: [frameAssetId]
      }, { projectId });
      const transformJob = await JobManager.waitForJob(transformJobId);
      const charAssetId = transformJob.outputs!.assetId;
      const charPath = transformJob.outputs!.path;

      // 3. Green Iris & Freeze (FFmpeg)
      const irisJobId = await JobManager.submitJob('ffmpeg', 'green_iris_freeze', {
        videoPath: plate.path,
        characterPath: charPath,
        inputAssetIds: [plate.id, charAssetId],
        ...parameters // pass down the visual parameters
      }, { projectId });
      const irisJob = await JobManager.waitForJob(irisJobId);
      
      return {
        assetId: irisJob.outputs!.assetId,
        path: irisJob.outputs!.path
      };
    } catch (e: any) {
      console.error("Pipeline execution failed:", e);
      throw e;
    }
  }

  static async generateCommercialPackage(params: CommercialPackageParams) {
    console.log("Generating Commercial Package for Asset:", params.sceneAssetId);

    try {
      // 1. NORMAL SCENE -> LUCK OF THE IRISH!!! -> TRANSFORMATION -> GREEN IRIS -> FREEZE FRAME
      const irisResult = await this.runLuckOfTheIrish(params.sceneAssetId, params.projectId, params.luckParams);

      // 2. Generate Title Card (ComfyUI): LUCK OF THE IRISH™
      const titleJobId = await JobManager.submitJob('comfyui', 'generate_title_card', {
        prompt: params.titlePrompt || "Commercial title card: LUCK OF THE IRISH, bold green typography, 4k",
        inputAssetIds: []
      }, { projectId: params.projectId });
      const titleJob = await JobManager.waitForJob(titleJobId);
      const titleAssetId = titleJob.outputs!.assetId;
      const titlePath = titleJob.outputs!.path;

      // 3. Generate Disclaimer (ComfyUI)
      const disclaimerJobId = await JobManager.submitJob('comfyui', 'generate_disclaimer', {
        prompt: params.disclaimerPrompt || "Legal disclaimer screen, white text on black background, fine print",
        inputAssetIds: []
      }, { projectId: params.projectId });
      const disclaimerJob = await JobManager.waitForJob(disclaimerJobId);
      const disclaimerAssetId = disclaimerJob.outputs!.assetId;
      const disclaimerPath = disclaimerJob.outputs!.path;

      // 4. Concatenate Final Package (FFmpeg): CUT BACK TO STORY (assumed to be a composite or just ending the commercial)
      const finalJobId = await JobManager.submitJob('ffmpeg', 'concatenate_sequence', {
        segments: [irisResult.path, titlePath, disclaimerPath],
        inputAssetIds: [irisResult.assetId, titleAssetId, disclaimerAssetId]
      }, { projectId: params.projectId });
      const finalJob = await JobManager.waitForJob(finalJobId);

      return finalJob.outputs!.assetId;
    } catch (e: any) {
      console.error("Commercial Package generation failed:", e);
      throw e;
    }
  }
}
