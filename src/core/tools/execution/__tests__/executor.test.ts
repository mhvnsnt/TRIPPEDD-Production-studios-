import { describe, it, expect } from 'vitest';
import path from 'path';
import { executeTool, adapterDefined, samplingSupported } from '../executor';
import { resolveRunnerRoot, runnerRoot } from '../runnerRoot';

const PROBE = path.join(__dirname, 'fixtures', 'memory_probe.cjs');
const NODE = process.execPath;

describe('Executor — real process execution', () => {
  it('records a real run as EXECUTED with the actual command and exit result', async () => {
    const r = await executeTool({
      tool: 'node', version: process.version, executablePath: NODE,
      args: ['-e', 'process.stdout.write("hello-from-child")'],
      sourceFileId: 'src-1',
    });

    expect(r.provenance.executionState).toBe('EXECUTED');
    expect(r.provenance.success).toBe(true);
    expect(r.provenance.exitCode).toBe(0);
    expect(r.stdout).toContain('hello-from-child');
    // Provenance must carry the actual invocation, not a description of one.
    expect(r.provenance.command).toContain(NODE);
    expect(r.provenance.command).toContain('hello-from-child');
    expect(r.provenance.cwd).toBeTruthy();
    expect(new Date(r.provenance.endTime).getTime()).toBeGreaterThanOrEqual(
      new Date(r.provenance.startTime).getTime()
    );
  });

  it('a tool that starts and exits non-zero is EXECUTED with success=false', async () => {
    const r = await executeTool({
      tool: 'node', version: process.version, executablePath: NODE,
      args: ['-e', 'process.stderr.write("boom"); process.exit(3)'],
      sourceFileId: 'src-1',
    });

    // It ran. A failed run is not an absent tool.
    expect(r.provenance.executionState).toBe('EXECUTED');
    expect(r.provenance.success).toBe(false);
    expect(r.provenance.exitCode).toBe(3);
    expect(r.provenance.stderr).toContain('boom');
  });

  it('distinguishes a missing executable from an executed failure', async () => {
    const missing = await executeTool({
      tool: 'ghost', version: 'n/a',
      executablePath: '/nonexistent/definitely_not_a_real_binary',
      args: [], sourceFileId: 'src-1',
    });

    // Never spawned: no exit code at all, and the spawn error is preserved.
    expect(missing.provenance.success).toBe(false);
    expect(missing.provenance.exitCode).toBeNull();
    expect(missing.provenance.stderr).toMatch(/ENOENT|spawn error/i);

    const ranAndFailed = await executeTool({
      tool: 'node', version: process.version, executablePath: NODE,
      args: ['-e', 'process.exit(1)'], sourceFileId: 'src-1',
    });
    expect(ranAndFailed.provenance.exitCode).toBe(1);

    // The two failures are distinguishable by exit code presence.
    expect(missing.provenance.exitCode).toBeNull();
    expect(ranAndFailed.provenance.exitCode).not.toBeNull();
  });
});

describe('Executor — RSS sampling against a real child pid', () => {
  it('samples a long-running process repeatedly and records a real peak', async () => {
    const allocMB = 200;
    const r = await executeTool({
      tool: 'memory-probe', version: 'test', executablePath: NODE,
      args: [PROBE, String(allocMB), '2000'],
      sourceFileId: 'src-mem',
      sampleIntervalMs: 100,
    });

    expect(r.provenance.success).toBe(true);
    const s = r.provenance.resourceSampling!;
    expect(s).toBeDefined();

    if (!samplingSupported()) {
      expect(s.status).toBe('SAMPLING_UNSUPPORTED');
      return;
    }

    expect(s.status).toBe('SAMPLED');
    // Multiple samples across a ~2s life at a 100ms interval.
    expect(s.sampleCount).toBeGreaterThan(1);
    expect(s.peakRssMB).toBeDefined();
    expect(s.avgRssMB).toBeDefined();

    // Plausibly above a bare interpreter baseline, without asserting it equals
    // the requested allocation — allocator and runtime overhead make that wrong.
    expect(s.peakRssMB!).toBeGreaterThan(allocMB * 0.5);
    expect(r.provenance.resourceUsage?.ramMB).toBe(s.peakRssMB);
  }, 30_000);

  it('a process too short-lived to sample reports no measurement, never zero', async () => {
    const r = await executeTool({
      tool: 'node', version: process.version, executablePath: NODE,
      args: ['-e', '0'],
      sourceFileId: 'src-short',
      // Longer than the process can possibly live, so no tick can fire.
      sampleIntervalMs: 60_000,
    });

    const s = r.provenance.resourceSampling!;
    expect(s.sampleCount).toBe(0);
    expect(s.status).toBe('NO_SAMPLE_CAPTURED');
    expect(s.reason).toBeTruthy();

    // The whole point: absence of measurement is undefined, not 0.
    expect(s.peakRssMB).toBeUndefined();
    expect(s.avgRssMB).toBeUndefined();
    expect(r.provenance.resourceUsage).toBeUndefined();
    expect(s.peakRssMB).not.toBe(0);
  }, 20_000);
});

describe('Executor — explicit working directory', () => {
  it('defaults to the resolved runner root rather than the ambient cwd', async () => {
    const r = await executeTool({
      tool: 'node', version: process.version, executablePath: NODE,
      args: ['-e', 'process.stdout.write(process.cwd())'],
      sourceFileId: 'src-cwd',
    });
    expect(r.stdout.trim()).toBe(runnerRoot());
    expect(r.provenance.cwd).toBe(runnerRoot());
  });

  it('honours an explicit cwd and records it in provenance', async () => {
    const r = await executeTool({
      tool: 'node', version: process.version, executablePath: NODE,
      args: ['-e', 'process.stdout.write(process.cwd())'],
      sourceFileId: 'src-cwd', cwd: '/tmp',
    });
    expect(r.stdout.trim()).toBe('/tmp');
    expect(r.provenance.cwd).toBe('/tmp');
  });

  it('resolves the same root from an unrelated caller directory', () => {
    // The earlier probe failure came from running a script located outside the
    // repo, so its relative imports resolved elsewhere. Root resolution must not
    // depend on where the caller happens to be standing.
    const fromRepo = resolveRunnerRoot(process.cwd());
    const fromNested = resolveRunnerRoot(path.join(process.cwd(), 'src', 'core', 'tools'));
    expect(fromNested).toBe(fromRepo);
  });

  it('a relative script path resolves against the explicit cwd', async () => {
    const rel = path.relative(runnerRoot(), PROBE);
    const r = await executeTool({
      tool: 'memory-probe', version: 'test', executablePath: NODE,
      args: [rel, '5', '10'],
      sourceFileId: 'src-rel',
      cwd: runnerRoot(),
    });
    expect(r.provenance.success).toBe(true);
    expect(r.stdout).toContain('allocated 5MB');
  }, 20_000);
});

describe('Executor — ADAPTER_DEFINED never masquerades as execution', () => {
  it('marks a non-run tool as ADAPTER_DEFINED with no exit code', () => {
    const p = adapterDefined('whisperx', 'src-1', 'NOT_INSTALLED');
    expect(p.executionState).toBe('ADAPTER_DEFINED');
    expect(p.success).toBe(false);
    expect(p.exitCode).toBeUndefined();
    expect(p.command).toBe('');
    expect(p.derivedArtifactIds).toEqual([]);
  });
});
