import { ContentProvenance } from '../types';
import { JobManager } from '../jobs/manager';

export interface PerformanceRecording {
  id: string;
  takeId: string;
  actor: string;
  sourceAssetId: string; // The asset representing the video/audio
  dialogue: string;
  timing: { start: number, end: number }; // Relative to the source asset
  blocking?: string;
  eyeline?: string;
  framing?: string;
  status: 'SELECTED' | 'REJECTED' | 'ALTERNATE';
  provenance: ContentProvenance;
}

export class PerformanceCaptureManager {
  private static recordings = new Map<string, PerformanceRecording[]>();

  static addRecording(shotId: string, recording: PerformanceRecording) {
    if (!this.recordings.has(shotId)) {
      this.recordings.set(shotId, []);
    }
    this.recordings.get(shotId)!.push(recording);
  }

  static getSelectedRecordings(shotId: string): PerformanceRecording[] {
    return (this.recordings.get(shotId) || []).filter(r => r.status === 'SELECTED');
  }

  static async extractPerformanceTiming(recording: PerformanceRecording): Promise<{ duration: number, audioFeatureExtractionAssetId?: string }> {
    // In a real system, this would analyze the audio/video to find the exact duration, phonemes, etc.
    const duration = recording.timing.end - recording.timing.start;
    
    // Simulate analyzing the performance to serve as authoritative input for generated characters
    return {
      duration,
      audioFeatureExtractionAssetId: 'simulated_audio_features_' + recording.id
    };
  }
}
