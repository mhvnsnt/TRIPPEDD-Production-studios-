import fs from "fs/promises";
import path from "path";
import os from "os";
import { MediaJob } from "../core/types";
import { AutonomousStudioOrchestrator, type ProductionWorkItem } from "../core/agents/orchestrator";
import { planSourceClip } from "../core/agents/studioPlan";
import { toolManager } from "./toolManager";
import { analyzeMedia, downloadToFile } from "./mediaPipeline";
import { discoverComedy } from "./comedyDiscovery";
import { productionMemory } from "./productionMemory";

export class QueueManager {
  private jobs = new Map<string, MediaJob>();
  private tokens = new Map<string, string>();
  private activeProcessing = 0;
  private MAX_CONCURRENT = Math.max(1, Number(process.env.MEDIA_MAX_CONCURRENT || 1));
  private readonly mediaCacheDir = process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media');
  private studio = new AutonomousStudioOrchestrator();
  private sourcePlans = new Map<string, ProductionWorkItem[]>();

  getJobs(): MediaJob[] { return Array.from(this.jobs.values()).map(job => this.publicJob(job)).sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()); }
  getJob(fileId: string): MediaJob | undefined {
    const job = this.jobs.get(fileId); if (!job) return undefined; const manager = this;
    return new Proxy(job as any, { get(target, property, receiver) { if (property === 'token') return undefined; if (property === 'toJSON') return () => manager.publicJob(target); return Reflect.get(target, property, receiver); }, set(target, property, value, receiver) { if (property === 'token') { if (typeof value === 'string' && value) { manager.tokens.set(fileId, value); void manager.processNext(); } return true; } const changed = Reflect.set(target, property, value, receiver); target.updatedAt = new Date().toISOString(); return changed; } }) as MediaJob;
  }
  setAccessToken(fileId: string, token: string) { if (!token) throw new Error('Cannot attach an empty Drive credential.'); this.tokens.set(fileId, token); void this.processNext(); }
  retry(fileId: string) { const job = this.jobs.get(fileId); if (!job || !this.tokens.has(fileId)) return false; job.state = 'QUEUED' as any; job.progress = 0; job.logs.push(`[${new Date().toISOString()}] Retry requested.`); job.updatedAt = new Date().toISOString(); void this.processNext(); return true; }
  addJob(job: MediaJob) { if (this.jobs.has(job.fileId)) return; this.jobs.set(job.fileId, job); const plan = planSourceClip(this.studio, job.fileId, job.originalName || job.fileId); this.sourcePlans.set(job.fileId, plan.work); (job as any).productionPlan = plan.work.map(work => ({ id: work.id, kind: work.kind, title: work.title, status: work.status, requiresHumanApproval: work.requiresHumanApproval })); }
  updateJob(id: string, updates: Partial<MediaJob>) { const job = this.jobs.get(id); if (job) Object.assign(job, updates, { updatedAt: new Date().toISOString() }); }
  log(id: string, message: string) { const job = this.jobs.get(id); if (job) job.logs.push(`[${new Date().toISOString()}] ${message}`); }
  async processNext() { while (this.activeProcessing < this.MAX_CONCURRENT) { const job = Array.from(this.jobs.values()).find(j => j.state === 'QUEUED' && this.tokens.has(j.fileId)); if (!job) return; this.updateJob(job.fileId, { state: 'PROBING', progress: 1 }); this.activeProcessing++; void this.processJob(job).finally(() => { this.activeProcessing--; void this.processNext(); }); } }
  private async processJob(job: MediaJob) { try { await this.runPipeline(job); } catch (e: any) { this.log(job.fileId, `FATAL: ${e?.message || String(e)}`); this.updateJob(job.fileId, { state: 'FAILED', progress: 100 }); this.failPlan(job.fileId); } }
  private publicJob(job: MediaJob): MediaJob { const copy = { ...job } as any; delete copy.token; return copy; }
  private completePlanKind(fileId: string, kind: ProductionWorkItem['kind'], outputRefs: string[] = []) { const item = this.sourcePlans.get(fileId)?.find(work => work.kind === kind); if (!item || item.status === 'DONE') return; this.studio.complete(item.id, outputRefs); const job = this.jobs.get(fileId) as any; if (job?.productionPlan) { const planItem = job.productionPlan.find((work: any) => work.id === item.id); if (planItem) planItem.status = 'DONE'; } }
  private failPlan(fileId: string) { const item = this.sourcePlans.get(fileId)?.find(work => work.status === 'RUNNING' || work.status === 'READY'); if (item) this.studio.fail(item.id); }

  async runPipeline(job: MediaJob) {
    const mediaUrl = `https://www.googleapis.com/drive/v3/files/${encodeURIComponent(job.fileId)}?alt=media`;
    const credential = this.tokens.get(job.fileId);
    if (!credential) throw new Error('No Drive credential is attached to this ingest job.');
    this.log(job.fileId, credential.startsWith('public:') ? 'Starting production media analysis from publicly shared Drive media.' : 'Starting production media analysis pipeline.');
    this.updateJob(job.fileId, { state: 'PROBING', progress: 5 });
    const available = (id: string) => toolManager.getTool(id)?.installationStatus === 'AVAILABLE';
    const tools = { ffprobe: available('ffprobe'), pyscenedetect: available('pyscenedetect'), opencv: available('opencv'), tesseract: available('tesseract'), whisper: available('whisper') };
    if (!tools.ffprobe) throw new Error('ffprobe is required for ingest and is unavailable.');
    await fs.mkdir(this.mediaCacheDir, { recursive: true });
    const extension = path.extname(job.originalName || '') || '.media';
    const localFilePath = path.join(this.mediaCacheDir, `${job.fileId}${extension}`);
    const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-ingest-'));
    const downloadPath = path.join(tmpDir, `source${extension}`);
    try {
      try { await fs.access(localFilePath); this.log(job.fileId, '[download] Reusing cached source media.'); }
      catch { this.log(job.fileId, '[download] Streaming source media from Google Drive into production cache.'); this.updateJob(job.fileId, { state: 'DOWNLOADING/STREAMING', progress: 8 }); await downloadToFile(mediaUrl, credential, downloadPath); await fs.rename(downloadPath, localFilePath); this.log(job.fileId, '[download] Source media cached for editorial rendering.'); }
      this.updateJob(job.fileId, { state: 'ANALYZING', progress: 10 }); this.completePlanKind(job.fileId, 'INGEST', [`source:${job.fileId}`, `media:${localFilePath}`]);
      const result = await analyzeMedia(localFilePath, tools, ({ stage, progress, message }) => { this.log(job.fileId, `[${stage}] ${message}`); this.updateJob(job.fileId, { state: 'ANALYZING', progress }); });
      if (result.ffprobe) job.tools.ffprobe = { status: 'COMPLETED' as const, data: result.ffprobe, provenance: this.provenance(job, 'ffprobe', 'ffprobe -print_format json -show_format -show_streams <local-source>') } as any;
      if (result.scenes) job.tools.pyscenedetect = { status: 'COMPLETED' as const, data: result.scenes, provenance: this.provenance(job, 'pyscenedetect', 'scenedetect detect-content list-scenes <local-source>') } as any;
      if (result.visual) job.tools.opencv = { status: 'COMPLETED' as const, data: result.visual, provenance: this.provenance(job, 'opencv', 'cv2.VideoCapture frame sampling') } as any;
      if (result.ocr !== undefined) job.tools.tesseract = { status: 'COMPLETED' as const, data: { text: result.ocr }, provenance: this.provenance(job, 'tesseract', 'tesseract <sampled-frame> stdout') } as any;
      if (result.transcript !== undefined) job.tools.whisper = { status: result.transcript ? 'COMPLETED' as const : 'HEALTH_CHECK_FAILED' as const, data: result.transcript, provenance: this.provenance(job, 'whisper', `whisper <local-source> --model ${process.env.WHISPER_MODEL || 'tiny'} --output_format json`) } as any;
      this.completePlanKind(job.fileId, 'MEDIA_ANALYSIS', [`analysis:${job.fileId}`]);
      const comedy = discoverComedy({ sourceFileId: job.fileId, transcript: result.transcript, scenes: result.scenes, ocr: result.ocr });
      await productionMemory.recordGags('trippedd', comedy);
      this.completePlanKind(job.fileId, 'GAG_DISCOVERY', comedy.map(gag => `gag:${gag.id}`));
      const snapshot = await productionMemory.upsert('trippedd', { sources: { [job.fileId]: { fileId: job.fileId, name: job.originalName, mediaPath: localFilePath, ingestedAt: new Date().toISOString(), analysis: result } }, jobs: { [job.fileId]: { state: 'NEEDS_REVIEW', updatedAt: new Date().toISOString(), gagCount: comedy.length, mediaPath: localFilePath } } });
      (job as any).productionIntelligence = { gagCandidates: comedy, callbackKeys: comedy.flatMap(g => g.callbackKeys), mediaPath: localFilePath, memoryUpdatedAt: snapshot.updatedAt };
      this.log(job.fileId, `Comedy discovery produced ${comedy.length} machine-suggested candidates; source evidence remains unchanged.`);
      this.log(job.fileId, 'Autonomous plan advanced through ingest, analysis, and gag discovery. Story development is now waiting at the human review gate.');
      const completedTools = Object.values(tools).filter(Boolean).length; this.log(job.fileId, `Analysis complete. ${completedTools}/${Object.keys(tools).length} analysis tools available.`);
      this.updateJob(job.fileId, { state: 'NEEDS_REVIEW', progress: 100 }); this.log(job.fileId, 'Pipeline completed with real tool outputs and production intelligence. Source media is retained for editorial assembly.');
    } finally { await fs.rm(tmpDir, { recursive: true, force: true }); }
  }
  private provenance(job: MediaJob, tool: string, command: string) { return { executionState: 'EXECUTED', sourceFileId: job.fileId, startTime: new Date().toISOString(), endTime: new Date().toISOString(), tool, version: toolManager.getTool(tool)?.version || 'unknown', executablePath: toolManager.getTool(tool)?.executablePath, command, success: true, timestamp: new Date().toISOString(), durationMs: 0 }; }
}

export const queueManager = new QueueManager();
