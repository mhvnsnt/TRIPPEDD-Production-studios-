import { exec } from 'child_process';
import { promisify } from 'util';
import { ToolAdapter, ToolExecutionResult, MediaAnalysisResult } from './types';

const execAsync = promisify(exec);

export class FFprobeAdapter implements ToolAdapter {
  readonly name = 'ffprobe';

  async isAvailable(): Promise<boolean> {
    try {
      await execAsync('ffprobe -version');
      return true;
    } catch {
      return false;
    }
  }

  async getVersion(): Promise<string | undefined> {
    try {
      const { stdout } = await execAsync('ffprobe -version');
      const match = stdout.match(/ffprobe version ([\w.-]+)/i);
      return match ? match[1] : undefined;
    } catch {
      return undefined;
    }
  }

  async analyzeMedia(filePath: string): Promise<MediaAnalysisResult> {
    const version = await this.getVersion();
    const command = `ffprobe -v quiet -print_format json -show_format -show_streams "${filePath}"`;
    
    let stdout = '';
    let stderr = '';
    let exitCode: number | null = 0;
    let success = false;
    let errorMsg: string | undefined;

    try {
      const res = await execAsync(command);
      stdout = res.stdout;
      stderr = res.stderr;
      success = true;
    } catch (e: any) {
      stdout = e.stdout || '';
      stderr = e.stderr || '';
      exitCode = e.code ?? 1;
      success = false;
      errorMsg = e.message;
    }

    const provenance: ToolExecutionResult = {
      tool: this.name,
      version,
      command,
      stdout,
      stderr,
      exitCode,
      success,
      timestamp: new Date().toISOString(),
      error: errorMsg
    };

    if (!success) {
      return { provenance };
    }

    try {
      const data = JSON.parse(stdout);
      
      const format = data.format;
      const videoStream = data.streams?.find((s: any) => s.codec_type === 'video');
      const audioStream = data.streams?.find((s: any) => s.codec_type === 'audio');

      let fps: number | undefined;
      if (videoStream?.r_frame_rate) {
        const [num, den] = videoStream.r_frame_rate.split('/');
        if (num && den && Number(den) !== 0) {
          fps = Number(num) / Number(den);
        }
      }

      return {
        metadata: {
          duration: format?.duration ? Number(format.duration) : undefined,
          width: videoStream?.width,
          height: videoStream?.height,
          codec: videoStream?.codec_name,
          fps,
          hasAudio: !!audioStream
        },
        provenance
      };
    } catch (e: any) {
      provenance.success = false;
      provenance.error = `Failed to parse JSON: ${e.message}`;
      return { provenance };
    }
  }
}
