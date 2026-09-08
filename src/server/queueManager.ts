import { execFile } from "child_process";
import { promisify } from "util";
import fs from "fs/promises";
import path from "path";
import os from "os";
import { MediaJob } from "../core/types";
import { toolManager } from "./toolManager";
import { analyzeMedia, downloadToFile } from "./mediaPipeline";

const execFileAsync = promisify(execFile);

export class QueueManager {
  private jobs = new Map<string, MediaJob>();
  private activeProcessing = 0;
  private MAX_CONCURRENT = Math.max(1, Number(process.env.MEDIA_MAX_CONCURRENT || 1));

  getJobs(): MediaJob[] {
    return Array.from(this.jobs.values()).sort((a, b) =>
      new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
    );
  }

  getJob(fileId: string): MediaJob | undefined {
    return this.jobs.get(fileId);
  }

  addJob(job: MediaJob) {
    if (!this.jobs.has(job.fileId)) {
      this.jobs.set(job.fileId, job);
      void this.processNext();
    }
  }

  updateJob(id: string, updates: Partial<MediaJob>) {
    const job = this.jobs.get(id);
    if (job) Object.assign(job, updates, { updatedAt: new Date().toISOString() });
  }

  log(id: string, message: string) {
    const job = this.jobs.get(id);
    if (job) job.logs.push(`[${new Date().toISOString()}] ${message}`);
  }

  async processNext() {
    while (this.activeProcessing < this.MAX_CONCURRENT) {
      const job = Array.from(this.jobs.values()).find(j => j.state === 'QUEUED');
      if (!job) return;

      this.updateJob(job.fileId, { state: 'PROBING', progress: 1 });
      this.activeProcessing++;
      void this.processJob(job).finally(() => {
        this.activeProcessing--;
        void this.processNext();
      });
    }
  }

  private async processJob(job: MediaJob) {
    try {
      await this.runPipeline(job);
    } catch (e: any) {
      this.log(job.fileId, `FATAL: ${e?.message || String(e)}`);
      this.updateJob(job.fileId, { state: 'FAILED', progress: 100 });
    }
  }

  async runPipeline(job: MediaJob) {
    const mediaUrl = `https://www.googleapis.com/drive/v3/files/${encodeURIComponent(job.fileId)}?alt=media`;
    const token = (job as any).token as string | undefined;
    if (!token) throw new Error('No Drive access token is attached to this ingest job.');

    this.log(job.fileId, 'Starting production media analysis pipeline.');
    this.updateJob(job.fileId, { state: 'PROBING', progress: 5 });

    const available = (id: string) => toolManager.getTool(id)?.installationStatus === 'AVAILABLE';
    const tools = {
      ffprobe: available('ffprobe'),
      pyscenedetect: available('pyscenedetect'),
      opencv: available('opencv'),
      tesseract: available('tesseract'),
      whisper: available('whisper'),
    };

    if (!tools.ffprobe) {
      throw new Error('ffprobe is required for ingest and is unavailable.');
    }

    const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-ingest-'));
    const extension = path.extname(job.originalName || '') || '.media';
    const localFilePath = path.join(tmpDir, `source${extension}`);

    try {
      this.log(job.fileId, '[download] Streaming source media from Google Drive.');
      this.updateJob(job.fileId, { state: 'DOWNLOADING/STREAMING', progress: 8 });
      await downloadToFile(mediaUrl, token, localFilePath);
      this.log(job.fileId, '[download] Source media is locally available.');

      this.updateJob(job.fileId, { state: 'ANALYZING', progress: 10 });
      const result = await analyzeMedia(localFilePath, tools, ({ stage, progress, message }) => {
        this.log(job.fileId, `[${stage}] ${message}`);
        this.updateJob(job.fileId, { state: stage === 'complete' ? 'ANALYZING' : 'ANALYZING', progress });
      });

      if (result.ffprobe) {
        job.tools.ffprobe = {
          status: 'COMPLETED' as const,
          data: result.ffprobe,
          provenance: {
            executionState: 'EXECUTED', sourceFileId: job.fileId,
            startTime: new Date().toISOString(), endTime: new Date().toISOString(),
            tool: 'ffprobe', version: toolManager.getTool('ffprobe')?.version || 'unknown',
            executablePath: toolManager.getTool('ffprobe')?.executablePath,
            command: 'ffprobe -print_format json -show_format -show_streams <local-source>',
            success: true, timestamp: new Date().toISOString(), durationMs: 0,
          },
        } as any;
      }

      if (result.scenes) {
        job.tools.pyscenedetect = {
          status: 'COMPLETED' as const,
          data: result.scenes,
          provenance: {
            executionState: 'EXECUTED', sourceFileId: job.fileId,
            startTime: new Date().toISOString(), endTime: new Date().toISOString(),
            tool: 'pyscenedetect', version: toolManager.getTool('pyscenedetect')?.version || 'unknown',
            executablePath: toolManager.getTool('pyscenedetect')?.executablePath,
            command: 'scenedetect detect-content list-scenes <local-source>',
            success: true, timestamp: new Date().toISOString(), durationMs: 0,
          },
        } as any;
      }

      if (result.visual) {
        job.tools.opencv = {
          status: 'COMPLETED' as const,
          data: result.visual,
          provenance: {
            executionState: 'EXECUTED', sourceFileId: job.fileId,
            startTime: new Date().toISOString(), endTime: new Date().toISOString(),
            tool: 'opencv', version: toolManager.getTool('opencv')?.version || 'unknown',
            executablePath: toolManager.getTool('opencv')?.executablePath,
            command: 'cv2.VideoCapture frame sampling',
            success: true, timestamp: new Date().toISOString(), durationMs: 0,
          },
        } as any;
      }

      if (result.ocr !== undefined) {
        job.tools.tesseract = {
          status: 'COMPLETED' as const,
          data: { text: result.ocr },
          provenance: {
            executionState: 'EXECUTED', sourceFileId: job.fileId,
            startTime: new Date().toISOString(), endTime: new Date().toISOString(),
            tool: 'tesseract', version: toolManager.getTool('tesseract')?.version || 'unknown',
            executablePath: toolManager.getTool('tesseract')?.executablePath,
            command: 'tesseract <sampled-frame> stdout',
            success: true, timestamp: new Date().toISOString(), durationMs: 0,
          },
        } as any;
      }

      if (result.transcript !== undefined) {
        job.tools.whisper = {
          status: result.transcript ? 'COMPLETED' as const : 'FAILED' as const,
          data: result.transcript,
          provenance: {
            executionState: 'EXECUTED', sourceFileId: job.fileId,
            startTime: new Date().toISOString(), endTime: new Date().toISOString(),
            tool: 'whisper', version: toolManager.getTool('whisper')?.version || 'unknown',
            executablePath: toolManager.getTool('whisper')?.executablePath,
            command: `whisper <local-source> --model ${process.env.WHISPER_MODEL || 'tiny'} --output_format json`,
            success: Boolean(result.transcript), timestamp: new Date().toISOString(), durationMs: 0,
          },
        } as any;
      }

      const completedTools = Object.values(tools).filter(Boolean).length;
      this.log(job.fileId, `Analysis complete. ${completedTools}/${Object.keys(tools).length} analysis tools available.`);
      this.updateJob(job.fileId, { state: 'NEEDS_REVIEW', progress: 100 });
      this.log(job.fileId, 'Pipeline completed with real tool outputs.');
    } finally {
      await fs.rm(tmpDir, { recursive: true, force: true });
    }
  }
}

export const queueManager = new QueueManager();
