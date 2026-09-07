import { exec } from 'child_process';
import { promisify } from 'util';
import { ToolAdapter, ToolExecutionResult, MediaAnalysisResult } from './types';
import * as fs from 'fs';
import * as path from 'path';

const execAsync = promisify(exec);
const readFileAsync = promisify(fs.readFile);
const unlinkAsync = promisify(fs.unlink);

export class PySceneDetectAdapter implements ToolAdapter {
  readonly name = 'scenedetect';

  async isAvailable(): Promise<boolean> {
    try {
      await execAsync('scenedetect version');
      return true;
    } catch {
      return false;
    }
  }

  async getVersion(): Promise<string | undefined> {
    try {
      const { stdout } = await execAsync('scenedetect version');
      const match = stdout.match(/scenedetect v([\w.-]+)/i) || stdout.match(/PySceneDetect v([\w.-]+)/i);
      return match ? match[1] : undefined;
    } catch {
      return undefined;
    }
  }

  async analyzeMedia(filePath: string): Promise<MediaAnalysisResult> {
    const version = await this.getVersion();
    const tempFileName = `scene_${Date.now()}`;
    const command = `scenedetect -i "${filePath}" detect-content list-scenes -o /tmp -f ${tempFileName}.csv`;
    
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

    let scenes: { startTime: number; endTime: number }[] = [];
    
    try {
      const csvFullPath = path.join('/tmp', `${tempFileName}.csv`);
      if (fs.existsSync(csvFullPath)) {
        const csvContent = await readFileAsync(csvFullPath, 'utf8');
        const lines = csvContent.split('\n');
        let inData = false;
        for (const line of lines) {
           if (line.startsWith('Scene Number')) {
             inData = true;
             continue;
           }
           if (inData && line.trim()) {
             const parts = line.split(',');
             if (parts.length >= 7) {
               scenes.push({
                 startTime: parseFloat(parts[3]),
                 endTime: parseFloat(parts[6])
               });
             }
           }
        }
        await unlinkAsync(csvFullPath).catch(() => {});
      }
    } catch (e: any) {
       provenance.error = `Failed to parse scenes CSV: ${e.message}`;
    }

    return {
      scenes,
      provenance
    };
  }
}
