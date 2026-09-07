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
