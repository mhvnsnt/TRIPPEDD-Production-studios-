
import { ProductionGraph } from './productionGraph';
import { PhysicalTimelineManager } from './physicalTimeline';
import { SourceClip, SourceShot, TranscriptSegment } from '../types';

export class MediaIngestPipeline {
  constructor(
    private graph: ProductionGraph,
    private physicalTimeline: PhysicalTimelineManager,
    private orchestrator: any = {
      analyzeFile: async () => []
    }
  ) {}

  async ingestFile(captureSessionId: string, filePath: string, clipDescription: string = 'Ingested media'): Promise<SourceClip | null> {
    const session = this.graph.captureSessions.get(captureSessionId);
    if (!session) {
      throw new Error(`CaptureSession ${captureSessionId} not found`);
    }

    //this.graph.updateCaptureSessionStatus(captureSessionId, 'IN_PROGRESS');

    const analysisResults = await this.orchestrator.analyzeFile(filePath);
    
    // Check for fundamental failures (e.g. ffprobe failed)
    const ffprobeResult = analysisResults.find((r: any) => r.provenance.tool === 'ffprobe');
    if (!ffprobeResult || !ffprobeResult.provenance.success) {
      session.notes = `Ingest failed: ${ffprobeResult?.provenance.error || 'Unknown error'}`;
      //this.graph.updateCaptureSessionStatus(captureSessionId, 'FAILED');
      return null;
    }

    // Generate clip
    const clipId = `CLIP_${Date.now()}`;
    const clip: SourceClip = {
      id: clipId,
      assetId: filePath,
      startTimecode: '00:00:00:00',
      endTimecode: '00:00:00:00',
      description: clipDescription,
      captureSessionId,
      workOrderId: session.workOrderId
    };

    // Add to physical timeline
    this.physicalTimeline.getTimeline().clips.push(clip);

    // Process scene detection results
    const sceneResult = analysisResults.find((r: any) => r.provenance.tool === 'scenedetect');
    if (sceneResult && sceneResult.provenance.success && sceneResult.scenes) {
      sceneResult.scenes.forEach((scene: any, index: number) => {
        const shotObs: SourceShot = {
          id: `SHOT_${Date.now()}_${index}`,
          type: 'SHOT',
          sourceClipId: clipId,
          startTime: scene.startTime.toString(),
          endTime: scene.endTime.toString(),
          description: `Detected Scene ${index + 1}`,
          origin: 'MACHINE_GENERATED',
          reviewState: 'UNREVIEWED',
          createdAt: new Date().toISOString(),
          toolProvenance: sceneResult.provenance
        };
        this.physicalTimeline.addObservation(shotObs);
      });
    }

    // Process transcript results
    const whisperResult = analysisResults.find((r: any) => r.provenance.tool === 'whisper');
    if (whisperResult && whisperResult.provenance.success && whisperResult.transcripts) {
      whisperResult.transcripts.forEach((transcript: any, index: number) => {
        const transcriptObs: TranscriptSegment = {
          id: `TRANS_${Date.now()}_${index}`,
          type: 'TRANSCRIPT',
          sourceClipId: clipId,
          startTime: transcript.startTime.toString(),
          endTime: transcript.endTime.toString(),
          text: transcript.text,
          description: `Transcript snippet`,
          origin: 'MACHINE_GENERATED',
          reviewState: 'UNREVIEWED',
          createdAt: new Date().toISOString(),
          toolProvenance: whisperResult.provenance
        };
        this.physicalTimeline.addObservation(transcriptObs);
      });
    }

    // Link clip to session
    //this.graph.linkSourceClipToCaptureSession(captureSessionId, clipId);
    //this.graph.updateCaptureSessionStatus(captureSessionId, 'COMPLETED');

    return clip;
  }
}
