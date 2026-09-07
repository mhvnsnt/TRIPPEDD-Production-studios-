/**
 * Automatic Drive ingestion.
 *
 * Polls the configured folder, dedupes against the queue by stable Drive file
 * id, and enqueues anything new. This is what turns the pipeline from "click
 * Run Analysis on each clip" into "drop footage in Drive and walk away".
 *
 * Files still uploading are tolerated: an incomplete upload simply is not
 * discovered yet, and the next poll picks it up. Nothing is placeheld — an
 * absent upload is not evidence of anything.
 */
import type { MediaJob } from '../core/types';
import type { QueueManager } from './queueManager';

export interface DriveFile {
  id: string;
  name: string;
  mimeType: string;
  size?: string;
  md5Checksum?: string;
  thumbnailLink?: string;
}

export interface WatcherOptions {
  folderId: string;
  /** Supplies a currently valid OAuth token, or undefined if not connected. */
  getToken: () => string | undefined;
  intervalMs?: number;
  /** Injectable for tests; defaults to the real Drive list call. */
  listFiles?: (folderId: string, token: string) => Promise<DriveFile[]>;
  onError?: (e: Error) => void;
}

const VIDEO_RE = /^(video\/|application\/(mp4|x-matroska))/i;

export async function listDriveFiles(folderId: string, token: string): Promise<DriveFile[]> {
  const fields = 'files(id,name,mimeType,size,md5Checksum,thumbnailLink)';
  const q = encodeURIComponent(`'${folderId}' in parents and trashed=false`);
  const url = `https://www.googleapis.com/drive/v3/files?q=${q}&fields=${encodeURIComponent(fields)}&pageSize=1000`;
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error(`Drive list failed: ${res.status} ${res.statusText}`);
  const data = await res.json();
  return (data.files ?? []) as DriveFile[];
}

export interface ScanResult {
  discovered: number;
  enqueued: number;
  skippedExisting: number;
  skippedNonVideo: number;
  error?: string;
}

export class DriveWatcher {
  private timer: NodeJS.Timeout | undefined;
  private opts: WatcherOptions;
  private queue: QueueManager;
  private lastScanAt: string | undefined;
  private lastResult: ScanResult | undefined;
  private scanning = false;

  constructor(queue: QueueManager, opts: WatcherOptions) {
    this.queue = queue;
    this.opts = opts;
  }

  getStatus() {
    return {
      running: !!this.timer,
      folderId: this.opts.folderId,
      intervalMs: this.opts.intervalMs ?? 60_000,
      lastScanAt: this.lastScanAt,
      lastResult: this.lastResult,
    };
  }

  /** One pass. Safe to call manually as a "Process New Media" action. */
  async scanOnce(): Promise<ScanResult> {
    if (this.scanning) {
      return this.lastResult ?? { discovered: 0, enqueued: 0, skippedExisting: 0, skippedNonVideo: 0 };
    }
    this.scanning = true;
    try {
      const token = this.opts.getToken();
      if (!token) {
        const r: ScanResult = { discovered: 0, enqueued: 0, skippedExisting: 0, skippedNonVideo: 0, error: 'Drive not connected (no token)' };
        this.lastResult = r;
        this.lastScanAt = new Date().toISOString();
        return r;
      }

      const lister = this.opts.listFiles ?? listDriveFiles;
      const files = await lister(this.opts.folderId, token);

      let enqueued = 0, skippedExisting = 0, skippedNonVideo = 0;
      for (const f of files) {
        if (!VIDEO_RE.test(f.mimeType ?? '')) { skippedNonVideo++; continue; }
        // Stable Drive id is the dedup key; re-scanning never duplicates.
        if (this.queue.getJob(f.id)) { skippedExisting++; continue; }

        const job: MediaJob = {
          id: `JOB_${f.id}`,
          fileId: f.id,
          originalName: f.name,
          mimeType: f.mimeType,
          size: f.size,
          hash: f.md5Checksum,
          thumbnailLink: f.thumbnailLink,
          state: 'QUEUED',
          progress: 0,
          logs: [`Discovered automatically in Drive folder ${this.opts.folderId}.`],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          tools: {},
          evidenceRefs: [],
        };
        (job as any).token = token;
        this.queue.addJob(job);
        enqueued++;
      }

      const r: ScanResult = { discovered: files.length, enqueued, skippedExisting, skippedNonVideo };
      this.lastResult = r;
      this.lastScanAt = new Date().toISOString();
      return r;
    } catch (e: any) {
      const r: ScanResult = { discovered: 0, enqueued: 0, skippedExisting: 0, skippedNonVideo: 0, error: e?.message ?? String(e) };
      this.lastResult = r;
      this.lastScanAt = new Date().toISOString();
      this.opts.onError?.(e);
      return r;
    } finally {
      this.scanning = false;
    }
  }

  start(): void {
    if (this.timer) return;
    const every = this.opts.intervalMs ?? 60_000;
    void this.scanOnce();
    this.timer = setInterval(() => void this.scanOnce(), every);
    // Never hold the process open just to poll.
    this.timer.unref?.();
  }

  stop(): void {
    if (this.timer) clearInterval(this.timer);
    this.timer = undefined;
  }
}
