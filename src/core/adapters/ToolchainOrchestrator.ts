import { FFprobeAdapter } from './FFprobeAdapter';
import { PySceneDetectAdapter } from './PySceneDetectAdapter';
import { WhisperAdapter } from './WhisperAdapter';
import { MediaAnalysisResult } from './types';

export class ToolchainOrchestrator {
  private adapters = [
    new FFprobeAdapter(),
    new PySceneDetectAdapter(),
    new WhisperAdapter()
  ];
  
  async analyzeFile(filePath: string): Promise<MediaAnalysisResult[]> {
    const results: MediaAnalysisResult[] = [];
    
    for (const adapter of this.adapters) {
      const isAvail = await adapter.isAvailable();
      if (isAvail) {
        const res = await adapter.analyzeMedia(filePath);
        results.push(res);
      } else {
        results.push({
          provenance: {
            success: false,
            tool: adapter.name,
            command: '',
            stdout: '',
            stderr: '',
            exitCode: null,
            timestamp: new Date().toISOString(),
            error: 'Tool not installed or available in PATH'
          }
        });
      }
    }
    
    return results;
  }
}
