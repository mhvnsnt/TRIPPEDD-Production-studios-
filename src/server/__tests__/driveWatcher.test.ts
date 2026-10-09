import { describe, it, expect } from 'vitest';
import path from 'path';
import os from 'os';
import { mkdtempSync } from 'fs';
import { DriveWatcher, type DriveFile } from '../driveWatcher';
import { QueueManager } from '../evidenceQueue';

function queue() {
  return new QueueManager({
    provisioner: { getTool: () => undefined }, // nothing available: no work runs
    analyzers: [],
    workRoot: mkdtempSync(path.join(os.tmpdir(), 'dw-')),
  });
}

const vid = (id: string, name = `${id}.mp4`): DriveFile => ({ id, name, mimeType: 'video/mp4', size: '1024' });

describe('DriveWatcher — automatic discovery', () => {
  it('discovers and enqueues everything in the folder without per-file clicks', async () => {
    const qm = queue();
    const w = new DriveWatcher(qm, {
      folderId: 'F', getToken: () => 'tok',
      listFiles: async () => [vid('a'), vid('b'), vid('c')],
    });

    const r = await w.scanOnce();
    expect(r.discovered).toBe(3);
    expect(r.enqueued).toBe(3);
    expect(qm.getJobs().length).toBe(3);
  });

  it('deduplicates by stable Drive id across repeated scans', async () => {
    const qm = queue();
    const w = new DriveWatcher(qm, {
      folderId: 'F', getToken: () => 'tok',
      listFiles: async () => [vid('a'), vid('b')],
    });

    await w.scanOnce();
    const second = await w.scanOnce();

    expect(second.enqueued).toBe(0);
    expect(second.skippedExisting).toBe(2);
    expect(qm.getJobs().length).toBe(2);
  });

  it('picks up files that arrive later without reprocessing the earlier ones', async () => {
    const qm = queue();
    let files = [vid('a')];
    const w = new DriveWatcher(qm, {
      folderId: 'F', getToken: () => 'tok',
      listFiles: async () => files,
    });

    await w.scanOnce();
    const firstJob = qm.getJob('a')!;
    const firstCreatedAt = firstJob.createdAt;

    // Two more uploads finish.
    files = [vid('a'), vid('b'), vid('c')];
    const r = await w.scanOnce();

    expect(r.enqueued).toBe(2);
    expect(qm.getJobs().length).toBe(3);
    // The original job object is untouched: no reprocessing, no lost history.
    expect(qm.getJob('a')).toBe(firstJob);
    expect(qm.getJob('a')!.createdAt).toBe(firstCreatedAt);
  });

  it('ignores non-video files rather than queueing them', async () => {
    const qm = queue();
    const w = new DriveWatcher(qm, {
      folderId: 'F', getToken: () => 'tok',
      listFiles: async () => [
        vid('a'),
        { id: 'doc', name: 'notes.txt', mimeType: 'text/plain' },
        { id: 'sheet', name: 's.gsheet', mimeType: 'application/vnd.google-apps.spreadsheet' },
      ],
    });

    const r = await w.scanOnce();
    expect(r.enqueued).toBe(1);
    expect(r.skippedNonVideo).toBe(2);
  });

  it('reports a missing token instead of inventing files', async () => {
    const qm = queue();
    const w = new DriveWatcher(qm, {
      folderId: 'F', getToken: () => undefined,
      listFiles: async () => [vid('a')],
    });

    const r = await w.scanOnce();
    expect(r.error).toMatch(/not connected/i);
    expect(r.discovered).toBe(0);
    expect(qm.getJobs().length).toBe(0);
  });

  it('surfaces a Drive failure without creating placeholder clips', async () => {
    const qm = queue();
    const w = new DriveWatcher(qm, {
      folderId: 'F', getToken: () => 'tok',
      listFiles: async () => { throw new Error('Drive list failed: 403 Forbidden'); },
    });

    const r = await w.scanOnce();
    // An upload that has not arrived is not evidence that nothing happened.
    expect(r.error).toContain('403');
    expect(qm.getJobs().length).toBe(0);
    expect(w.getStatus().lastResult?.error).toContain('403');
  });

  it('exposes status for the pipeline monitor', async () => {
    const qm = queue();
    const w = new DriveWatcher(qm, {
      folderId: 'FOLDER_X', getToken: () => 'tok', intervalMs: 5000,
      listFiles: async () => [vid('a')],
    });
    await w.scanOnce();
    const s = w.getStatus();

    expect(s.folderId).toBe('FOLDER_X');
    expect(s.intervalMs).toBe(5000);
    expect(s.lastScanAt).toBeTruthy();
    expect(s.lastResult?.enqueued).toBe(1);
  });
});
