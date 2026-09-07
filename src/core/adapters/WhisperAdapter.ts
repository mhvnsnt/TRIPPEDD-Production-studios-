import { exec } from 'child_process';
import { promisify } from 'util';
import { ToolAdapter, ToolExecutionResult, MediaAnalysisResult } from './types';
import * as fs from 'fs';
import * as path from 'path';

const execAsync = promisify(exec);
const readFileAsync = promisify(fs.readFile);
const unlinkAsync = promisify(fs.unlink);

export class WhisperAdapter implements ToolAdapter {
  readonly name = 'whisper';

  async isAvailable(): Promise<boolean> {
    try {
      // faster-whisper or whisper CLI
      await execAsync('whisper --help');
      return true;
    } catch {
      return false;
    }
  }

  async getVersion(): Promise<string | undefined> {
    return '1.0';
  }

  async analyzeMedia(filePath: string): Promise<MediaAnalysisResult> {
    const tempFileName = `transcript_${Date.now()}`;
    const command = `whisper "${filePath}" --output_format json --output_dir /tmp --output_name ${tempFileName}`;
    
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
      version: '1.0',
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

    let transcripts: { startTime: number; endTime: number; text: string }[] = [];
    
    try {
      const jsonFullPath = path.join('/tmp', `${tempFileName}.json`);
      if (fs.existsSync(jsonFullPath)) {
        const jsonContent = await readFileAsync(jsonFullPath, 'utf8');
        const data = JSON.parse(jsonContent);
        if (data.segments) {
          transcripts = data.segments.map((seg: any) => ({
            startTime: seg.start,
            endTime: seg.end,
            text: seg.text.trim()
          }));
        }
        await unlinkAsync(jsonFullPath).catch(() => {});
      }
    } catch (e: any) {
       provenance.error = `Failed to parse whisper JSON: ${e.message}`;
    }

    return {
      transcripts,
      provenance
    };
  }
}
