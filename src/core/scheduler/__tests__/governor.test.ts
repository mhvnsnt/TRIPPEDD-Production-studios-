import { describe, it, expect } from 'vitest';
import os from 'os';
import path from 'path';
import { mkdtempSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { ResourceGovernor } from '../ResourceGovernor';
import { ArtifactLifecycle, dirSize } from '../ArtifactLifecycle';

const MB = 1024 * 1024;

describe('ResourceGovernor — measures, never guesses', () => {
  it('reads real free disk and memory from the system', async () => {
    const g = new ResourceGovernor({ workspacePath: process.cwd() });
    const snap = await g.snapshot();

    // Real filesystem numbers, not placeholders.
    expect(snap.diskTotalMB).toBeGreaterThan(0);
    expect(snap.diskFreeMB).toBeGreaterThan(0);
    expect(snap.diskFreeMB).toBeLessThanOrEqual(snap.diskTotalMB);
    expect(snap.memTotalMB).toBeGreaterThan(0);
    expect(snap.memFreeMB).toBeLessThanOrEqual(snap.memTotalMB);
  });

  it('labels an estimate as an estimate and a measurement as measured', () => {
    const g = new ResourceGovernor();
    const before = g.requirementFor('whisperx', { cls: 'HEAVY', diskMB: 100, ramMB: 2048 });
    expect(before.ramSource).toBe('ESTIMATED');
    expect(before.ramMB).toBe(2048);

    // Feed it a real observed peak from an actual run.
    g.recordUsage('whisperx', 900);
    const after = g.requirementFor('whisperx', { cls: 'HEAVY', diskMB: 100, ramMB: 2048 });
    expect(after.ramSource).toBe('MEASURED');
    expect(after.ramMB).toBe(Math.ceil(900 * 1.25));
  });

  it('keeps the high-water mark across runs', () => {
    const g = new ResourceGovernor();
    g.recordUsage('demucs', 500);
    g.recordUsage('demucs', 1400);
    g.recordUsage('demucs', 700);
    expect(g.getObservation('demucs')!.peakRssMB).toBe(1400);
    expect(g.getObservation('demucs')!.samples).toBe(3);
  });

  it('ignores a missing measurement rather than recording zero', () => {
    const g = new ResourceGovernor();
    g.recordUsage('ffprobe', undefined);
    g.recordUsage('ffprobe', 0);
    expect(g.getObservation('ffprobe')).toBeUndefined();
  });
});

describe('ResourceGovernor — admission control', () => {
  it('refuses work that would breach the temp-workspace budget', async () => {
    const g = new ResourceGovernor({ limits: { diskQuotaMB: 500 } });
    expect((await g.reserve('a', 400)).admitted).toBe(true);

    const d = await g.reserve('b', 200);
    expect(d.admitted).toBe(false);
    expect(d.code).toBe('RESOURCE_BLOCKED');
    expect(d.constraint).toBe('QUOTA');
    expect(d.requiredBytes).toBe(200 * MB);
    expect(d.reservedBytes).toBe(400 * MB);
    expect(d.reason).toMatch(/quota/i);
  });

  it('refuses work that would eat the disk floor', async () => {
    // Quota deliberately huge so the FILESYSTEM floor is what binds here,
    // not the workspace budget — otherwise this passes for the wrong reason.
    const g = new ResourceGovernor({ workspacePath: process.cwd(), limits: { diskQuotaMB: 10_000_000 } });
    const free = await g.diskFreeMB();
    // Demand nearly all remaining space; the floor must stop it.
    const d = await g.admit({
      cls: 'HEAVY', diskMB: Math.max(1, free - 100), ramMB: 1,
      diskSource: 'ESTIMATED', ramSource: 'ESTIMATED',
    });
    expect(d.admitted).toBe(false);
    expect(d.constraint).toBe('DISK');
    expect(d.reason).toMatch(/must stay free/);
  });

  it('refuses work that would eat the memory floor', async () => {
    const g = new ResourceGovernor();
    const d = await g.admit({
      cls: 'HEAVY', diskMB: 0, ramMB: g.memTotalMB() * 2,
      diskSource: 'ESTIMATED', ramSource: 'ESTIMATED',
    });
    expect(d.admitted).toBe(false);
    expect(d.constraint).toBe('MEMORY');
    // The refusal says whether the figure was measured or estimated.
    expect(d.reason).toMatch(/estimated|measured/);
  });

  it('a heavy analyzer cannot start just because a slot is free', async () => {
    // Slots available, but the budget is not.
    const g = new ResourceGovernor({ limits: { HEAVY: 4, diskQuotaMB: 10 } });
    const snap = await g.snapshot();
    expect(snap.active.HEAVY).toBe(0); // a slot is free

    const d = await g.admit({
      cls: 'HEAVY', diskMB: 5000, ramMB: 1,
      diskSource: 'ESTIMATED', ramSource: 'ESTIMATED',
    });
    expect(d.admitted).toBe(false);
  });

  it('releases reservations exactly', async () => {
    const g = new ResourceGovernor({ limits: { diskQuotaMB: 1000 } });
    await g.reserve('x', 300);
    expect(g.getReservedMB()).toBe(300);
    expect(g.release('x')).toBe(300);
    expect(g.getReservedMB()).toBe(0);
    // Releasing an unknown key is a no-op, not a negative balance.
    expect(g.release('nope')).toBe(0);
    expect(g.getReservedMB()).toBe(0);
  });
});

describe('ResourceGovernor — concurrency by class', () => {
  it('bounds each class independently', async () => {
    const g = new ResourceGovernor({ limits: { LIGHT: 3, MEDIUM: 2, HEAVY: 1 } });
    let liveHeavy = 0, peakHeavy = 0, liveLight = 0, peakLight = 0;

    const heavy = () => g.withSlot('HEAVY', async () => {
      liveHeavy++; peakHeavy = Math.max(peakHeavy, liveHeavy);
      await new Promise((r) => setTimeout(r, 60));
      liveHeavy--;
    });
    const light = () => g.withSlot('LIGHT', async () => {
      liveLight++; peakLight = Math.max(peakLight, liveLight);
      await new Promise((r) => setTimeout(r, 60));
      liveLight--;
    });

    await Promise.all([heavy(), heavy(), heavy(), light(), light(), light(), light()]);

    expect(peakHeavy).toBe(1);
    expect(peakLight).toBeLessThanOrEqual(3);
    expect((await g.snapshot()).active.HEAVY).toBe(0);
  }, 30_000);

  it('serialises GPU work independently of class', async () => {
    const g = new ResourceGovernor({ limits: { HEAVY: 4, gpu: 1 } });
    let live = 0, peak = 0;
    const run = () => g.withSlot('HEAVY', async () => {
      live++; peak = Math.max(peak, live);
      await new Promise((r) => setTimeout(r, 50));
      live--;
    }, true);

    await Promise.all([run(), run(), run()]);
    expect(peak).toBe(1);
  }, 30_000);

  it('releases the slot when the work throws', async () => {
    const g = new ResourceGovernor({ limits: { HEAVY: 1 } });
    await expect(g.withSlot('HEAVY', async () => { throw new Error('boom'); })).rejects.toThrow('boom');
    // Not wedged: the next acquisition succeeds.
    await g.withSlot('HEAVY', async () => {});
    expect((await g.snapshot()).active.HEAVY).toBe(0);
  });
});

describe('ArtifactLifecycle — ownership and retention', () => {
  function tmpFile(dir: string, name: string, bytes: number) {
    const p = path.join(dir, name);
    writeFileSync(p, Buffer.alloc(bytes, 1));
    return p;
  }

  it('cleans disposable scratch and preserves everything that matters', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'life-'));
    const life = new ArtifactLifecycle();

    const scratch = tmpFile(dir, 'frames.jpg', 4096);
    const source = tmpFile(dir, 'source.mp4', 8192);
    const evidence = tmpFile(dir, 'transcript.json', 2048);
    const project = tmpFile(dir, 'cut.kdenlive', 1024);

    await life.register({ jobId: 'j1', sourceFileId: 'c1', filePath: scratch, purpose: 'ocr frames', retention: 'DISPOSABLE' });
    await life.register({ jobId: 'j1', sourceFileId: 'c1', filePath: source, purpose: 'source media', retention: 'SOURCE_MEDIA' });
    await life.register({ jobId: 'j1', sourceFileId: 'c1', filePath: evidence, purpose: 'transcript', retention: 'EVIDENCE' });
    await life.register({ jobId: 'j1', sourceFileId: 'c1', filePath: project, purpose: 'export', retention: 'EDITORIAL_PROJECT' });

    const res = await life.cleanupJob('j1');

    expect(res.removed).toBe(1);
    expect(res.bytesReclaimed).toBe(4096);
    expect(res.preserved).toBe(3);
    expect(existsSync(scratch)).toBe(false);
    // The three that must survive, do.
    expect(existsSync(source)).toBe(true);
    expect(existsSync(evidence)).toBe(true);
    expect(existsSync(project)).toBe(true);
  });

  it('records size, purpose and owner for every artifact', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'life-'));
    const life = new ArtifactLifecycle();
    const f = tmpFile(dir, 'x.bin', 1234);
    const a = await life.register({ jobId: 'j9', sourceFileId: 'c9', filePath: f, purpose: 'scratch', retention: 'DISPOSABLE' });

    expect(a.sizeBytes).toBe(1234);
    expect(a.jobId).toBe('j9');
    expect(a.sourceFileId).toBe('c9');
    expect(a.createdAt).toBeTruthy();
    expect(life.usage().DISPOSABLE.bytes).toBe(1234);
  });

  it('cleans a failed job the same as a successful one', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'life-'));
    const life = new ArtifactLifecycle();
    const f = tmpFile(dir, 'partial.wav', 5000);
    await life.register({ jobId: 'jfail', sourceFileId: 'c1', filePath: f, purpose: 'stems', retention: 'DISPOSABLE' });

    const res = await life.cleanupJob('jfail');
    expect(res.bytesReclaimed).toBe(5000);
    expect(existsSync(f)).toBe(false);
    // Nothing left registered as live for that job.
    expect(life.forJob('jfail')).toEqual([]);
  });

  it('sweeps orphaned scratch left by a crash', async () => {
    const root = mkdtempSync(path.join(os.tmpdir(), 'sweep-'));
    mkdirSync(path.join(root, 'deadjob'));
    writeFileSync(path.join(root, 'deadjob', 'big.bin'), Buffer.alloc(9000, 1));
    mkdirSync(path.join(root, 'livejob'));
    writeFileSync(path.join(root, 'livejob', 'keep.bin'), Buffer.alloc(100, 1));

    const life = new ArtifactLifecycle();
    const res = await life.sweepOrphans(root, new Set(['livejob']));

    expect(res.removed).toBe(1);
    expect(res.bytesReclaimed).toBe(9000);
    expect(existsSync(path.join(root, 'deadjob'))).toBe(false);
    expect(existsSync(path.join(root, 'livejob'))).toBe(true);
  });

  it('measures directory size recursively', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'dsz-'));
    mkdirSync(path.join(dir, 'a'));
    writeFileSync(path.join(dir, 'a', 'x'), Buffer.alloc(1000, 1));
    writeFileSync(path.join(dir, 'y'), Buffer.alloc(2000, 1));
    expect(await dirSize(dir)).toBe(3000);
  });
});
