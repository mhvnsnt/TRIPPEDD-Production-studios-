import { describe, it, expect } from 'vitest';
import path from 'path';
import os from 'os';
import { mkdtempSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { QueueManager } from '../queueManager';
import { ResourceGovernor } from '../../core/scheduler/ResourceGovernor';
import { ArtifactLifecycle } from '../../core/scheduler/ArtifactLifecycle';
import type { Analyzer, AnalysisContext, AnalyzerResult, ToolHandle } from '../../core/analysis/analyzers';
import { adapterDefined, executeTool } from '../../core/tools/execution/executor';
import type { MediaJob } from '../../core/types';

function job(fileId: string, over: Partial<MediaJob> = {}): MediaJob {
  return {
    id: fileId, fileId, originalName: `${fileId}.mp4`, mimeType: 'video/mp4',
    size: '1048576', state: 'QUEUED', progress: 0, logs: [],
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
    tools: {}, evidenceRefs: [], ...over,
  } as MediaJob;
}

/** A registry we control, so tool availability is deterministic. */
function registry(states: Record<string, string>) {
  return {
    getTool(id: string): ToolHandle | undefined {
      const state = states[id];
      if (!state) return undefined;
      return { id, state, version: state === 'AVAILABLE' ? '1.0.0-test' : undefined, executablePath: '/bin/echo' };
    },
  };
}

/** An analyzer that genuinely runs a process, so provenance is real. */
function realAnalyzer(toolId: string, opts: Partial<Analyzer> = {}): Analyzer {
  return {
    id: toolId, requiresTool: toolId, resourceClass: 'LIGHT', requiresLocalFile: false,
    async run(ctx: AnalysisContext): Promise<AnalyzerResult> {
      const t = ctx.getTool(toolId);
      if (t?.state !== 'AVAILABLE') {
        return {
          tool: toolId, status: 'UNAVAILABLE',
          provenance: adapterDefined(toolId, ctx.fileId, `${toolId} ${t?.state ?? 'NOT_INSTALLED'}`),
          observations: [], derivedArtifacts: [],
        };
      }
      const r = await executeTool({
        tool: toolId, version: t.version!, executablePath: '/bin/echo',
        args: ['analysed'], sourceFileId: ctx.fileId,
      });
      return {
        tool: toolId, status: 'COMPLETED', provenance: r.provenance, derivedArtifacts: [],
        observations: [{
          id: `${toolId}_obs_1`, type: 'TEST_OBSERVATION', origin: 'MACHINE_GENERATED',
          reviewState: 'UNREVIEWED', tool: toolId, toolVersion: t.version!,
        }],
      };
    },
    ...opts,
  } as Analyzer;
}

describe('Pipeline — unavailable tools never produce evidence', () => {
  it('records UNAVAILABLE with ADAPTER_DEFINED provenance and zero observations', async () => {
    const qm = new QueueManager({
      provisioner: registry({ ffprobe: 'AVAILABLE', opencv: 'NOT_INSTALLED' }),
      analyzers: [realAnalyzer('ffprobe'), realAnalyzer('opencv')],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const j = job('f_unavail');
    qm.addJob(j);
    await qm.runPipeline(j);

    const cv = (j.tools as any).opencv;
    expect(cv.status).toBe('UNAVAILABLE');
    // No provenance claiming execution, and no observations attributed to it.
    expect(j.evidenceRefs.every((id) => !id.startsWith('opencv'))).toBe(true);

    const fp = (j.tools as any).ffprobe;
    expect(fp.status).toBe('COMPLETED');
    expect(fp.provenance.executionState).toBe('EXECUTED');
    expect(fp.provenance.exitCode).toBe(0);
  }, 30_000);

  it('a job where nothing could run ends UNAVAILABLE with no evidence', async () => {
    const qm = new QueueManager({
      provisioner: registry({ ffprobe: 'NOT_INSTALLED' }),
      analyzers: [realAnalyzer('ffprobe')],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });
    const j = job('f_none');
    qm.addJob(j);
    await qm.runPipeline(j);

    expect(j.state).toBe('UNAVAILABLE');
    expect(j.evidenceRefs).toEqual([]);
  }, 30_000);
});

describe('Pipeline — adapter existence is not execution', () => {
  it('an adapter that exists but whose tool is missing yields ADAPTER_DEFINED', async () => {
    const a = realAnalyzer('whisperx');
    const res = await a.run({
      fileId: 'f1', workDir: '/tmp', getTool: () => ({ id: 'whisperx', state: 'NOT_INSTALLED' }),
      pythonPath: () => 'python3',
    } as AnalysisContext);

    expect(res.status).toBe('UNAVAILABLE');
    expect(res.provenance.executionState).toBe('ADAPTER_DEFINED');
    expect(res.provenance.exitCode).toBeUndefined();
    expect(res.observations).toEqual([]);
  });
});

describe('Pipeline — newly provisioned capabilities are picked up', () => {
  it('the same queue uses a tool that becomes AVAILABLE after boot', async () => {
    const states: Record<string, string> = { opencv: 'NOT_INSTALLED' };
    const qm = new QueueManager({
      provisioner: registry(states),
      analyzers: [realAnalyzer('opencv')],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const before = job('f_before');
    qm.addJob(before);
    await qm.runPipeline(before);
    expect((before.tools as any).opencv.status).toBe('UNAVAILABLE');

    // Provisioning completes later; no queue restart.
    states.opencv = 'AVAILABLE';

    const after = job('f_after');
    qm.addJob(after);
    await qm.runPipeline(after);

    expect((after.tools as any).opencv.status).toBe('COMPLETED');
    expect((after.tools as any).opencv.provenance.executionState).toBe('EXECUTED');
    expect(after.evidenceRefs.length).toBeGreaterThan(0);
  }, 30_000);
});

describe('Pipeline — resource limits bound concurrent analysis', () => {
  it('never runs more CPU-heavy analyzers at once than the limit allows', async () => {
    const scheduler = new ResourceGovernor({ limits: { HEAVY: 2, LIGHT: 8 } });
    let live = 0, peak = 0;

    const heavy = (id: string): Analyzer => ({
      id, requiresTool: id, resourceClass: 'HEAVY', requiresLocalFile: false,
      async run(ctx) {
        live++; peak = Math.max(peak, live);
        await new Promise((r) => setTimeout(r, 120));
        live--;
        return {
          tool: id, status: 'COMPLETED',
          provenance: adapterDefined(id, ctx.fileId, 'test'),
          observations: [], derivedArtifacts: [],
        } as AnalyzerResult;
      },
    });

    const ids = ['a', 'b', 'c', 'd', 'e', 'f'];
    const qm = new QueueManager({
      provisioner: registry(Object.fromEntries(ids.map((i) => [i, 'AVAILABLE']))),
      analyzers: ids.map(heavy), governor: scheduler,
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const j = job('f_heavy');
    qm.addJob(j);
    await qm.runPipeline(j);

    expect(peak).toBeLessThanOrEqual(2);
    expect(peak).toBeGreaterThan(0);
  }, 30_000);

  it('enforces a hard temp-disk quota instead of filling the volume', async () => {
    const g = new ResourceGovernor({ limits: { diskQuotaMB: 100 } });
    expect((await g.reserve('a', 60)).admitted).toBe(true);

    const refused = await g.reserve('b', 60); // would breach the budget
    expect(refused.admitted).toBe(false);
    expect(refused.code).toBe('RESOURCE_BLOCKED');
    expect(refused.constraint).toBe('QUOTA');
    // The refusal states the actual numbers, not just "no".
    expect(refused.requiredBytes).toBe(60 * 1024 * 1024);
    expect(refused.reservedBytes).toBe(60 * 1024 * 1024);

    g.release('a');
    expect((await g.reserve('b', 60)).admitted).toBe(true);
  });

  it('releases the slot when an analyzer throws, so the queue cannot wedge', async () => {
    const scheduler = new ResourceGovernor({ limits: { HEAVY: 1 } });
    const boom: Analyzer = {
      id: 'boom', requiresTool: 'boom', resourceClass: 'HEAVY', requiresLocalFile: false,
      async run() { throw new Error('analyzer exploded'); },
    };
    const qm = new QueueManager({
      provisioner: registry({ boom: 'AVAILABLE', ok: 'AVAILABLE' }),
      analyzers: [boom, { ...realAnalyzer('ok'), resourceClass: 'HEAVY' } as Analyzer],
      governor: scheduler, workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const j = job('f_boom');
    qm.addJob(j);
    await qm.runPipeline(j);

    expect((j.tools as any).boom.status).toBe('FAILED');
    // The healthy analyzer still got a slot afterwards.
    expect((j.tools as any).ok.status).toBe('COMPLETED');
    expect((await scheduler.snapshot()).active.HEAVY).toBe(0);
  }, 30_000);
});

describe('Pipeline — temporary media handling', () => {
  it('cleans up the job work directory after processing', async () => {
    const workRoot = mkdtempSync(path.join(os.tmpdir(), 'q-'));
    const local = mkdtempSync(path.join(os.tmpdir(), 'src-'));
    const srcFile = path.join(local, 'media.mp4');
    writeFileSync(srcFile, Buffer.alloc(2048, 7));

    const qm = new QueueManager({
      provisioner: registry({ ffprobe: 'AVAILABLE' }),
      analyzers: [{ ...realAnalyzer('ffprobe'), requiresLocalFile: true } as Analyzer],
      workRoot,
      downloadMedia: async (_j, dest) => {
        writeFileSync(dest, Buffer.alloc(2048, 7));
        return 2048;
      },
    });

    const j = job('f_tmp');
    qm.addJob(j);
    await qm.runPipeline(j);

    expect((j.tools as any).ffprobe.status).toBe('COMPLETED');
    // Nothing left behind for this job.
    expect(existsSync(path.join(workRoot, 'f_tmp'))).toBe(false);
    expect(qm.getGovernor().getReservedMB()).toBe(0);
  }, 30_000);

  it('defers rather than exceeding the disk quota', async () => {
    const qm = new QueueManager({
      provisioner: registry({ ffprobe: 'AVAILABLE' }),
      analyzers: [{ ...realAnalyzer('ffprobe'), requiresLocalFile: true } as Analyzer],
      governor: new ResourceGovernor({ limits: { diskQuotaMB: 1 } }),
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
      downloadMedia: async () => { throw new Error('should not download'); },
    });

    const j = job('f_big', { size: String(500 * 1024 * 1024) });
    qm.addJob(j);
    await qm.runPipeline(j);

    // Short on space is a WAIT, not a failure: the media is fine, the box is
    // busy. The job parks and the governor retries it.
    expect(j.state).toBe('RESOURCE_WAIT');
    expect(j.logs.some((l) => /RESOURCE_BLOCKED/.test(l))).toBe(true);
    // The log states the actual numbers rather than just refusing.
    expect(j.logs.some((l) => /required .*MB, available .*MB, reserved .*MB/.test(l))).toBe(true);
    expect(qm.getResourceWaits()['f_big']).toBe(1);
    // Nothing was downloaded, so nothing needs cleaning up.
    expect(qm.getGovernor().getReservedMB()).toBe(0);
  }, 30_000);
});

describe('Pipeline — derived artifacts are owned, not orphaned', () => {
  it('registers every file an analyzer wrote, so cleanup reports real bytes', async () => {
    const workRoot = mkdtempSync(path.join(os.tmpdir(), 'q-'));

    // An analyzer that genuinely writes a file, like the real ones do.
    const writer: Analyzer = {
      id: 'pyscenedetect', requiresTool: 'pyscenedetect', resourceClass: 'MEDIUM',
      requiresLocalFile: false,
      async run(ctx) {
        const f = path.join(ctx.workDir, 'scenes.csv');
        writeFileSync(f, Buffer.alloc(4096, 1));
        return {
          tool: 'pyscenedetect', status: 'COMPLETED',
          provenance: adapterDefined('pyscenedetect', ctx.fileId, 't'),
          observations: [], derivedArtifacts: [f],
        } as AnalyzerResult;
      },
    };

    const lifecycle = new ArtifactLifecycle();
    const qm = new QueueManager({
      provisioner: registry({ pyscenedetect: 'AVAILABLE' }),
      analyzers: [writer], lifecycle, workRoot,
    });

    const j = job('f_art');
    qm.addJob(j);
    await qm.runPipeline(j);

    // The lifecycle must have SEEN the file. Before this was wired, the
    // registry was permanently empty and every cleanup number read zero.
    const seen = lifecycle.all();
    expect(seen.length).toBeGreaterThan(0);
    const csv = seen.find((a) => a.filePath.endsWith('scenes.csv'))!;
    expect(csv, 'the analyzer output should be registered').toBeTruthy();
    expect(csv.sizeBytes).toBe(4096);
    expect(csv.jobId).toBe('f_art');
    expect(csv.purpose).toContain('pyscenedetect');
    expect(csv.retention).toBe('DISPOSABLE');
    // And it was actually cleaned.
    expect(csv.releasedAt).toBeTruthy();
    expect(j.logs.some((l) => /Scratch cleaned: [1-9]/.test(l))).toBe(true);
  }, 30_000);

  it('registers retained source media as SOURCE_MEDIA and never deletes it', async () => {
    const workRoot = mkdtempSync(path.join(os.tmpdir(), 'q-'));
    const mediaDir = mkdtempSync(path.join(os.tmpdir(), 'lib-'));
    const lifecycle = new ArtifactLifecycle();

    const qm = new QueueManager({
      provisioner: registry({ ffprobe: 'AVAILABLE' }),
      analyzers: [{ ...realAnalyzer('ffprobe'), requiresLocalFile: true } as Analyzer],
      lifecycle, workRoot, retainMedia: true, mediaLibraryDir: mediaDir,
      downloadMedia: async (_j, dest) => { writeFileSync(dest, Buffer.alloc(2048, 9)); return 2048; },
    });

    const j = job('f_src');
    qm.addJob(j);
    await qm.runPipeline(j);

    const src = lifecycle.all().find((a) => a.retention === 'SOURCE_MEDIA');
    expect(src, 'retained media should be registered').toBeTruthy();
    // Preserved through cleanup, because deleting the source is never cleanup.
    expect(src!.releasedAt).toBeUndefined();
    expect(existsSync(src!.filePath)).toBe(true);
    expect((j as any).localMediaPath).toBe(src!.filePath);
  }, 30_000);
});

describe('Pipeline — resource pressure degrades rather than crashes', () => {
  it('blocks a heavy analyzer that does not fit, and says so on the job', async () => {
    // Big enough for light scratch (16MB), too small for heavy (256MB), so the
    // run degrades selectively instead of stopping altogether.
    const governor = new ResourceGovernor({ limits: { diskQuotaMB: 64, HEAVY: 4 } });
    const heavy: Analyzer = {
      id: 'whisper', requiresTool: 'faster-whisper', resourceClass: 'HEAVY',
      requiresLocalFile: false,
      async run() { throw new Error('should never run — it was not affordable'); },
    };

    const qm = new QueueManager({
      provisioner: registry({ 'faster-whisper': 'AVAILABLE', ffprobe: 'AVAILABLE' }),
      analyzers: [realAnalyzer('ffprobe'), heavy],
      governor,
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const j = job('f_pressure');
    qm.addJob(j);
    await qm.runPipeline(j);

    const w = (j.tools as any).whisper;
    expect(w.status).toBe('UNAVAILABLE');
    expect(w.error).toMatch(/RESOURCE_BLOCKED/);
    // The cheap analyzer still ran: pressure degrades the run, it does not stop it.
    expect((j.tools as any).ffprobe.status).toBe('COMPLETED');
    expect(j.state).toBe('NEEDS_REVIEW');
    // And the blocked tool is recorded for the editorial layer to declare.
    expect((j as any).resourceBlockedTools).toContain('faster-whisper');
  }, 30_000);

  it('an affordable heavy analyzer is admitted', async () => {
    const governor = new ResourceGovernor({ limits: { diskQuotaMB: 4096, HEAVY: 2 } });
    const qm = new QueueManager({
      provisioner: registry({ 'faster-whisper': 'AVAILABLE' }),
      analyzers: [{ ...realAnalyzer('faster-whisper'), resourceClass: 'HEAVY' } as Analyzer],
      governor,
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const j = job('f_ok');
    qm.addJob(j);
    await qm.runPipeline(j);

    expect((j.tools as any).whisper.status).toBe('COMPLETED');
    expect((j as any).resourceBlockedTools ?? []).toEqual([]);
  }, 30_000);

  it('feeds measured RSS back so the next decision is not a guess', async () => {
    const governor = new ResourceGovernor({ limits: { diskQuotaMB: 4096 } });
    const qm = new QueueManager({
      provisioner: registry({ ffprobe: 'AVAILABLE' }),
      analyzers: [realAnalyzer('ffprobe')],
      governor,
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const before = governor.requirementFor('ffprobe', { cls: 'LIGHT', diskMB: 1, ramMB: 999 });
    expect(before.ramSource).toBe('ESTIMATED');

    const j = job('f_meas');
    qm.addJob(j);
    await qm.runPipeline(j);

    // /bin/echo may exit before a sample lands; when it does, the figure must
    // stay honestly ESTIMATED rather than becoming a fabricated measurement.
    const after = governor.requirementFor('ffprobe', { cls: 'LIGHT', diskMB: 1, ramMB: 999 });
    const obs = governor.getObservation('ffprobe');
    if (obs) {
      expect(after.ramSource).toBe('MEASURED');
      expect(obs.peakRssMB).toBeGreaterThan(0);
    } else {
      expect(after.ramSource).toBe('ESTIMATED');
      expect(after.ramMB).toBe(999);
    }
  }, 30_000);
});

describe('Pipeline — analyzers run in dependency order', () => {
  it('an analyzer waits for the one it depends on', async () => {
    const order: string[] = [];
    const mk = (id: string, dependsOn?: string[]): Analyzer => ({
      id, requiresTool: id, resourceClass: 'LIGHT', requiresLocalFile: false, dependsOn,
      async run(ctx) {
        order.push(`${id}:start`);
        await new Promise((r) => setTimeout(r, 60));
        order.push(`${id}:end`);
        return { tool: id, status: 'COMPLETED', provenance: adapterDefined(id, ctx.fileId, 't'), observations: [], derivedArtifacts: [] } as AnalyzerResult;
      },
    });

    const qm = new QueueManager({
      provisioner: registry({ 'faster-whisper': 'AVAILABLE', whisperx: 'AVAILABLE' }),
      analyzers: [mk('whisperx', ['faster-whisper']), mk('faster-whisper')],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const j = job('f_dep');
    qm.addJob(j);
    await qm.runPipeline(j);

    // Alignment must not begin before the transcript pass has finished.
    expect(order.indexOf('whisperx:start')).toBeGreaterThan(order.indexOf('faster-whisper:end'));
  }, 30_000);

  it('marks a dependent analyzer UNAVAILABLE when its prerequisite never completes', async () => {
    const dependent: Analyzer = {
      id: 'whisperx', requiresTool: 'whisperx', resourceClass: 'LIGHT',
      requiresLocalFile: false, dependsOn: ['faster-whisper'],
      async run() { throw new Error('should never run'); },
    };
    const qm = new QueueManager({
      // The prerequisite's tool is missing, so it can never complete.
      provisioner: registry({ whisperx: 'AVAILABLE' }),
      analyzers: [dependent],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });

    const j = job('f_dep2');
    qm.addJob(j);
    await qm.runPipeline(j);

    const wx = (j.tools as any).whisperx;
    expect(wx.status).toBe('UNAVAILABLE');
    expect(wx.error).toMatch(/prerequisite/i);
    expect(j.evidenceRefs).toEqual([]);
  }, 30_000);
});

describe('Pipeline — a job never runs twice concurrently', () => {
  it('a second runPipeline call joins the in-flight run instead of racing it', async () => {
    let runs = 0;
    const slow: Analyzer = {
      id: 'slow', requiresTool: 'slow', resourceClass: 'LIGHT', requiresLocalFile: true,
      async run(ctx) {
        runs++;
        await new Promise((r) => setTimeout(r, 150));
        return {
          tool: 'slow', status: 'COMPLETED',
          provenance: adapterDefined('slow', ctx.fileId, 'test'),
          observations: [], derivedArtifacts: [],
        } as AnalyzerResult;
      },
    };

    let downloads = 0;
    const qm = new QueueManager({
      provisioner: registry({ slow: 'AVAILABLE' }),
      analyzers: [slow],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
      downloadMedia: async (_j, dest) => { downloads++; writeFileSync(dest, Buffer.alloc(16)); return 16; },
    });

    const j = job('f_race');
    // addJob already kicks off processing; awaiting runPipeline must not start
    // a second concurrent run that deletes the media out from under the first.
    qm.addJob(j);
    await Promise.all([qm.runPipeline(j), qm.runPipeline(j)]);

    expect(runs).toBe(1);
    expect(downloads).toBe(1);
    expect((j.tools as any).slow.status).toBe('COMPLETED');
  }, 30_000);
});

describe('Pipeline — counts come from the real queue', () => {
  it('derives counts from actual job states', async () => {
    const qm = new QueueManager({
      provisioner: registry({}), analyzers: [],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });
    qm.addJob(job('c1', { state: 'NEEDS_REVIEW' }));
    qm.addJob(job('c2', { state: 'QUEUED' }));
    qm.addJob(job('c3', { state: 'ANALYZING' }));
    qm.addJob(job('c4', { state: 'FAILED' }));

    const c = qm.getCounts();
    expect(c.discovered).toBe(4);
    expect(c.processed).toBe(1);
    expect(c.failed).toBe(1);
    // Adding a QUEUED job starts it immediately, so c2 has already moved to
    // PROBING alongside c3's ANALYZING. Counts track the live queue, which is
    // the point: they are derived, not declared.
    expect(c.processing).toBe(2);
    expect(c.queued).toBe(0);
    expect(c.discovered).toBe(
      c.processed + c.failed + c.processing + c.queued + c.unavailable
    );
  });
});

describe('Pipeline — provenance integrity', () => {
  it('a completed run carries command, exit code, timings and source id', async () => {
    const qm = new QueueManager({
      provisioner: registry({ ffprobe: 'AVAILABLE' }),
      analyzers: [realAnalyzer('ffprobe')],
      workRoot: mkdtempSync(path.join(os.tmpdir(), 'q-')),
    });
    const j = job('f_prov');
    qm.addJob(j);
    await qm.runPipeline(j);

    const p = (j.tools as any).ffprobe.provenance;
    expect(p.executionState).toBe('EXECUTED');
    expect(p.tool).toBe('ffprobe');
    expect(p.version).toBe('1.0.0-test');
    expect(p.command).toContain('/bin/echo');
    expect(p.sourceFileId).toBe('f_prov');
    expect(p.exitCode).toBe(0);
    expect(p.startTime).toBeTruthy();
    expect(p.endTime).toBeTruthy();
    expect(typeof p.durationMs).toBe('number');
    expect(p.cwd).toBeTruthy();
    expect(p.resourceSampling).toBeDefined();
  }, 30_000);
});
