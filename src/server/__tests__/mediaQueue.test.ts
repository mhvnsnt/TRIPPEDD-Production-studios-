import { describe, it, expect, beforeEach } from 'vitest';
import { QueueManager } from '../queueManager';
import { MediaJob } from '../../core/types';

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
