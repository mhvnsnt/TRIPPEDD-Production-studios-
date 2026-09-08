import { describe, it, expect, beforeEach } from 'vitest';
import { QueueManager } from '../queueManager';
import { MediaJob } from '../../core/types';
import os from 'os';
import path from 'path';
import { mkdtempSync, writeFileSync, readFileSync, existsSync } from 'fs';

describe('Media Pipeline Queue', () => {
  let qm: QueueManager;

  beforeEach(() => {
    qm = new QueueManager();
  });

  it('handles automatic folder discovery and deduplication', () => {
    const job1: MediaJob = { fileId: 'f1', state: 'QUEUED', tools: {}, logs: [] } as any;
    const job2: MediaJob = { fileId: 'f2', state: 'QUEUED', tools: {}, logs: [] } as any;
    
    qm.addJob(job1);
    qm.addJob(job2);
    qm.addJob(job1); // Duplicate

    expect(qm.getJobs().length).toBe(2);
  });

  it('handles asynchronous new-file arrival and queues them', () => {
    const job1: MediaJob = { fileId: 'f1', state: 'QUEUED', tools: {}, logs: [] } as any;
    qm.addJob(job1);
    
    // Simulate active processing
    const processingJob = qm.getJob('f1');
    if (processingJob) processingJob.state = 'ANALYZING';

    const job3: MediaJob = { fileId: 'f3', state: 'QUEUED', tools: {}, logs: [] } as any;
    qm.addJob(job3);

    expect(qm.getJobs().length).toBe(2);
    expect(qm.getJob('f3')?.state).toBe('QUEUED');
  });

  it('respects concurrent processing limits', async () => {
    // Override runPipeline to be slow
    qm.runPipeline = async (job) => {
      await new Promise(r => setTimeout(r, 100));
    };

    qm.addJob({ fileId: 'j1', state: 'QUEUED', tools: {} } as any);
    qm.addJob({ fileId: 'j2', state: 'QUEUED', tools: {} } as any);
    qm.addJob({ fileId: 'j3', state: 'QUEUED', tools: {} } as any);

    // Give it a tick to start
    await new Promise(r => setTimeout(r, 10));
    
    const active = qm.getJobs().filter(j => j.state === 'PROBING');
    expect(active.length).toBeLessThanOrEqual(1); // MAX_CONCURRENT is 1
  });

  it('handles retryable failure', () => {
    qm.addJob({ fileId: 'j1', state: 'FAILED', tools: {} } as any);
    qm.updateJob('j1', { state: 'QUEUED' });
    expect(qm.getJob('j1')?.state).toBe('QUEUED');
  });

  it('records optional-tool absence without fabricating data', async () => {
    // Run pipeline for a mock job
    // Actually runPipeline triggers shell commands, so we mock execAsync if needed,
    // but in vitest, testing real tool absence means it hits the catch blocks.
    const job: MediaJob = { fileId: 'test_absence', state: 'QUEUED', tools: {}, logs: [] } as any;
    qm.addJob(job);
    
    await new Promise(r => setTimeout(r, 500)); // wait for pipeline to run/fail
    
    const finishedJob = qm.getJob('test_absence');
    expect(finishedJob).toBeDefined();
    // In CI env, whisper shouldn't be installed
    expect(finishedJob?.tools.whisper?.status).toBe('UNAVAILABLE');
    // FFprobe might be completed or unavailable depending on env, but we shouldn't have fabricated transcripts.
    expect(finishedJob?.tools.whisper?.provenance).toBeUndefined();
  });
});

/**
 * The boot race. A job that starts before tool detection finishes asks about
 * tools that have not been detected, is told NOT_INSTALLED for all of them,
 * skips every analyzer, and then reports itself complete — a clip that was
 * never transcribed becomes indistinguishable from one that was transcribed and
 * found silent. Measured on a real server: 19 clips queued one second after
 * boot, the first two silently emptied.
 */
describe('QueueManager — waits for tool detection before analysing', () => {
  function lateProvisioner() {
    let detected = false;
    let resolve!: () => void;
    const ready = new Promise<void>((r) => { resolve = r; });
    return {
      ready,
      finishDetection: () => { detected = true; resolve(); },
      /** Before detection completes it knows about nothing, exactly like the real one. */
      getTool: (id: string) =>
        detected ? ({ id, state: 'AVAILABLE', version: '1.0' } as any) : undefined,
      sawToolBeforeDetection: () => false,
    };
  }

  it('does not claim a job while detection is still running', async () => {
    const q = new QueueManager();
    const p = lateProvisioner();
    q.setProvisioner(p, p.ready);

    q.addJob({ fileId: 'race1', state: 'QUEUED', tools: {}, logs: [] } as any);
    // Give the event loop room; the job must still be waiting, not finished.
    await new Promise((r) => setTimeout(r, 30));
    expect(q.getJob('race1')!.state).toBe('QUEUED');

    p.finishDetection();
    await new Promise((r) => setTimeout(r, 30));
    // Once detection lands the job is allowed to move on.
    expect(q.getJob('race1')!.state).not.toBe('QUEUED');
  });

  it('records the wait on the job, so a slow boot is visible rather than silent', async () => {
    const q = new QueueManager();
    const p = lateProvisioner();
    q.setProvisioner(p, p.ready);
    q.addJob({ fileId: 'race2', state: 'QUEUED', tools: {}, logs: [] } as any);
    await new Promise((r) => setTimeout(r, 20));
    expect(q.getJob('race2')!.logs.join(' ')).toContain('Waiting for toolchain detection');
    p.finishDetection();
  });

  it('EVERY queued job waits, not just the first', async () => {
    // The first version of this fix cleared the readiness flag before awaiting,
    // so job 1 waited and jobs 2..N found it already gone. Since
    // activeProcessing is only incremented after the await, the concurrency
    // guard did not hold them either — 18 of 19 clips still ran against a
    // half-detected toolchain.
    const q = new QueueManager();
    const p = lateProvisioner();
    q.setProvisioner(p, p.ready);

    for (const id of ['m1', 'm2', 'm3', 'm4']) {
      q.addJob({ fileId: id, state: 'QUEUED', tools: {}, logs: [] } as any);
    }
    await new Promise((r) => setTimeout(r, 40));
    for (const id of ['m1', 'm2', 'm3', 'm4']) {
      expect(q.getJob(id)!.state, `${id} did not wait for detection`).toBe('QUEUED');
    }
    p.finishDetection();
  });

  it('a failed provisioning promise must not wedge the queue forever', async () => {
    const q = new QueueManager();
    const failed = Promise.reject(new Error('apt exploded'));
    q.setProvisioner({ getTool: () => undefined }, failed);
    q.addJob({ fileId: 'race3', state: 'QUEUED', tools: {}, logs: [] } as any);
    await new Promise((r) => setTimeout(r, 40));
    // A broken install degrades the run; it does not stop it starting.
    expect(q.getJob('race3')!.state).not.toBe('QUEUED');
  });
});

/**
 * Evidence has to survive a restart.
 *
 * Transcribing this shoot is ~40 minutes of CPU, and all of it lived in one
 * in-memory Map. A container restart destroyed 237 transcript lines and every
 * observation behind them, and the only recovery was to run the machine again.
 * A pipeline whose output evaporates on a restart is not doing the work, it is
 * redoing it.
 */
describe('QueueManager — evidence survives a restart', () => {
  const dirs: string[] = [];

  /**
   * Held at the toolchain-readiness gate with a promise that never resolves, so
   * a job stays in the state the test set. Without it the pipeline claims the
   * job the moment it is added and the assertion races real work — which is
   * what happened first time and reported PROBING for everything.
   */
  function held(persistPath?: string) {
    const q = new QueueManager();
    q.setProvisioner({ getTool: () => undefined }, new Promise<void>(() => {}));
    if (persistPath) { (q as any).persistPath = persistPath; return q; }
    const dir = mkdtempSync(path.join(os.tmpdir(), 'queue-persist-'));
    dirs.push(dir);
    (q as any).persistPath = path.join(dir, 'queue.json');
    return q;
  }
  const isolated = () => held();

  it('reloads completed work, with its observations intact', async () => {
    const a = isolated();
    a.addJob({ fileId: 'k1', originalName: 'k1.mp4', state: 'QUEUED', tools: {}, logs: [] } as any);
    a.updateJob('k1', {
      state: 'NEEDS_REVIEW',
      observations: [{ id: 'o1', type: 'TRANSCRIPT_SEGMENT', text: 'we are at the cigar store' }],
    } as any);
    await a.persist();

    const b = held((a as any).persistPath);
    const r = await b.restore();
    expect(r.restored).toBe(1);
    const job: any = b.getJob('k1');
    expect(job.state).toBe('NEEDS_REVIEW');
    expect(job.observations[0].text).toBe('we are at the cigar store');
  });

  it('requeues a clip the restart caught mid-analysis instead of trusting it', async () => {
    const a = isolated();
    a.addJob({ fileId: 'k2', originalName: 'k2.mp4', state: 'QUEUED', tools: {}, logs: [] } as any);
    a.updateJob('k2', { state: 'ANALYZING' } as any);
    await a.persist();

    const b = held((a as any).persistPath);
    const r = await b.restore();
    expect(r.requeued).toBe(1);
    expect(b.getJob('k2')!.state).toBe('QUEUED');
    // and it says why, rather than silently reverting
    expect(b.getJob('k2')!.logs.join(' ')).toContain('interrupted');
  });

  it('a resource-blocked clip is retried, not left blocked forever', async () => {
    const a = isolated();
    a.addJob({ fileId: 'k3', originalName: 'k3.mp4', state: 'QUEUED', tools: {}, logs: [] } as any);
    a.updateJob('k3', { state: 'RESOURCE_WAIT' } as any);
    await a.persist();

    const b = held((a as any).persistPath);
    await b.restore();
    expect(b.getJob('k3')!.state).toBe('QUEUED');
  });

  it('a corrupt or missing evidence file is not fatal', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'queue-persist-'));
    dirs.push(dir);
    const q = held(path.join(dir, 'queue.json'));
    await expect(q.restore()).resolves.toEqual({ restored: 0, requeued: 0 });

    writeFileSync(path.join(dir, 'queue.json'), '{ not json');
    await expect(q.restore()).resolves.toEqual({ restored: 0, requeued: 0 });
  });

  it('never leaves a half-written evidence file where a reader could load it', async () => {
    const a = isolated();
    a.addJob({ fileId: 'k4', originalName: 'k4.mp4', state: 'QUEUED', tools: {}, logs: [] } as any);
    await a.persist();
    const dir = path.dirname((a as any).persistPath);
    // The temp file is renamed into place, never left behind.
    expect(existsSync(path.join(dir, 'queue.json.writing'))).toBe(false);
    expect(JSON.parse(readFileSync(path.join(dir, 'queue.json'), 'utf8')).jobs.length).toBe(1);
  });
});
