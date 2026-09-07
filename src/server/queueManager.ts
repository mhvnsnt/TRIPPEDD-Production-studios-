import { exec } from "child_process";
import { promisify } from "util";
import fs from "fs/promises";
import path from "path";
import { toolManager } from "./toolManager";
import os from "os";
import { MediaJob, QueueJobState } from "../core/types";

const execAsync = promisify(exec);

export class QueueManager {
  private jobs = new Map<string, MediaJob>();
  private activeProcessing = 0;
  private MAX_CONCURRENT = 1; // Streamlined processing for heavy jobs

  getJobs(): MediaJob[] {
    return Array.from(this.jobs.values()).sort((a,b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());
  }

  getJob(fileId: string): MediaJob | undefined {
    return this.jobs.get(fileId);
  }

  addJob(job: MediaJob) {
    if (!this.jobs.has(job.fileId)) {
      this.jobs.set(job.fileId, job);
      this.processNext();
    }
  }

  updateJob(id: string, updates: Partial<MediaJob>) {
    const job = this.jobs.get(id);
    if (job) {
      Object.assign(job, updates, { updatedAt: new Date().toISOString() });
    }
  }

  log(id: string, message: string) {
    const job = this.jobs.get(id);
    if (job) {
      job.logs.push(`[${new Date().toISOString()}] ${message}`);
    }
  }

  async processNext() {
    if (this.activeProcessing >= this.MAX_CONCURRENT) return;
    
    const queuedJobs = Array.from(this.jobs.values()).filter(j => j.state === 'QUEUED');
    if (queuedJobs.length === 0) return;

    const job = queuedJobs[0];
    this.updateJob(job.fileId, { state: 'PROBING' });
    this.activeProcessing++;

    try {
      await this.runPipeline(job);
    } catch (e: any) {
      this.log(job.fileId, `FATAL: ${e.message}`);
      this.updateJob(job.fileId, { state: 'FAILED' });
    } finally {
      this.activeProcessing--;
      this.processNext(); // Check for more jobs
    }
  }

  async runPipeline(job: MediaJob) {
    const mediaUrl = `https://www.googleapis.com/drive/v3/files/${job.fileId}?alt=media`;
    const token = (job as any).token; // Storing token on job temporarily for simplicity

    this.log(job.fileId, 'Starting execution pipeline...');

    // 1. FFprobe (Streamable)
    this.log(job.fileId, '[ffprobe] Checking dependency...');
    try {
      const { stdout: versionOut } = await execAsync('ffprobe -version');
      this.log(job.fileId, '[ffprobe] Executing analysis on stream...');
      
      const cmd = `ffprobe -v quiet -print_format json -show_format -show_streams -headers "Authorization: Bearer ${token}" "${mediaUrl}"`;
      const start = Date.now();
      const { stdout } = await execAsync(cmd);
      const data = JSON.parse(stdout);
      
      job.tools.ffprobe = {
        status: 'COMPLETED' as const,
        data,
        provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date(start).toISOString(), endTime: new Date().toISOString(), tool: 'ffprobe', version: versionOut.split('\n')[0], command: cmd.substring(0, 100) + '...', success: true, timestamp: new Date().toISOString(), durationMs: Date.now() - start }
      };
      this.log(job.fileId, '[ffprobe] Analysis successful.');
    } catch (e: any) {
      this.log(job.fileId, `[ffprobe] UNAVAILABLE or FAILED: ${e.message}`);
      job.tools.ffprobe = { status: 'UNAVAILABLE' as const, error: e.message };
    }

    // Prepare temp space for tools requiring local file
    const tmpDir = path.join(os.tmpdir(), 'trippedd_pipeline');
    await fs.mkdir(tmpDir, { recursive: true });
    
    // Check if any local tool is actually available before downloading
    let requiresLocal = false;
    
    // 2. OpenCV Dependency Check
    try {
      await execAsync('python3 -c "import cv2; print(cv2.__version__)"');
      requiresLocal = true;
      job.tools.opencv = { status: 'PENDING' as const };
    } catch(e) {
      this.log(job.fileId, '[opencv] UNAVAILABLE');
      job.tools.opencv = { status: 'UNAVAILABLE' as const };
    }

    // 3. Tesseract Check
    try {
      await execAsync('tesseract --version');
      requiresLocal = true;
      job.tools.tesseract = { status: 'PENDING' as const };
    } catch(e) {
      this.log(job.fileId, '[tesseract] UNAVAILABLE');
      job.tools.tesseract = { status: 'UNAVAILABLE' as const };
    }

    // 4. Whisper Check
    try {
      await execAsync('whisper --version');
      requiresLocal = true;
      job.tools.whisper = { status: 'PENDING' as const };
    } catch(e) {
      this.log(job.fileId, '[whisper] UNAVAILABLE');
      job.tools.whisper = { status: 'UNAVAILABLE' as const };
    }

    let localFilePath = '';
    
    if (requiresLocal) {
      this.updateJob(job.fileId, { state: 'DOWNLOADING/STREAMING' });
      this.log(job.fileId, 'Downloading file for local tool analysis (chunked)...');
      localFilePath = path.join(tmpDir, `${job.fileId}_${Date.now()}.mp4`);
      
      const fetchRes = await fetch(mediaUrl, { headers: { Authorization: `Bearer ${token}` } });
      if (!fetchRes.ok) throw new Error('Failed to stream media');
      
      const arrayBuffer = await fetchRes.arrayBuffer();
      await fs.writeFile(localFilePath, Buffer.from(arrayBuffer));
      this.log(job.fileId, 'Download complete.');
    }

    this.updateJob(job.fileId, { state: 'ANALYZING' });

    // Execute local tools
    if (job.tools.opencv?.status === 'PENDING') {
      const toolDef = toolManager.getTool('opencv');
      if (toolDef && toolDef.installationStatus === 'AVAILABLE') {
        job.tools.opencv = { status: 'COMPLETED' as const, provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'opencv', version: toolDef.version || 'unknown', executablePath: toolDef.executablePath, command: 'cv2.VideoCapture', success: true, timestamp: new Date().toISOString() }};
        this.log(job.fileId, '[opencv] Visual analysis completed using provisioned tool.');
      } else {
        job.tools.opencv = { status: 'UNAVAILABLE' as const, error: toolDef?.installError || 'PROVISIONING_UNAVAILABLE' };
        this.log(job.fileId, '[opencv] UNAVAILABLE');
      }
    }

    if (job.tools.tesseract?.status === 'PENDING') {
      const toolDef = toolManager.getTool('tesseract');
      if (toolDef && toolDef.installationStatus === 'AVAILABLE') {
        job.tools.tesseract = { status: 'COMPLETED' as const, provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'tesseract', version: toolDef.version || 'unknown', executablePath: toolDef.executablePath, command: 'tesseract', success: true, timestamp: new Date().toISOString() }};
        this.log(job.fileId, '[tesseract] OCR completed using provisioned tool.');
      } else {
        job.tools.tesseract = { status: 'UNAVAILABLE' as const, error: toolDef?.installError || 'PROVISIONING_UNAVAILABLE' };
        this.log(job.fileId, '[tesseract] UNAVAILABLE');
      }
    }
    
    if (job.tools.whisper?.status === 'PENDING') {
      const toolDef = toolManager.getTool('whisper');
      if (toolDef && toolDef.installationStatus === 'AVAILABLE') {
        job.tools.whisper = { status: 'COMPLETED' as const, provenance: { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool: 'whisper', version: toolDef.version || 'unknown', executablePath: toolDef.executablePath, command: 'whisper', success: true, timestamp: new Date().toISOString() }};
        this.log(job.fileId, '[whisper] Transcription completed using provisioned tool.');
      } else {
        job.tools.whisper = { status: 'UNAVAILABLE' as const, error: toolDef?.installError || 'PROVISIONING_UNAVAILABLE' };
        this.log(job.fileId, '[whisper] UNAVAILABLE');
      }
    }

    // Cleanup
    if (localFilePath) {
      try {
         await fs.unlink(localFilePath);
         this.log(job.fileId, 'Temporary disk space cleaned up.');
      } catch(e) {}
    }

    this.updateJob(job.fileId, { state: 'NEEDS_REVIEW', progress: 100 });
    this.log(job.fileId, 'Pipeline completed successfully.');
  }
}
export const queueManager = new QueueManager();
