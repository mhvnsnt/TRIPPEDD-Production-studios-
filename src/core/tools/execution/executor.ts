/**
 * THE SANCTIONED EXECUTOR.
 *
 * This module is the ONLY place in the codebase permitted to emit
 * `executionState: 'EXECUTED'`. A tool run is not evidence-producing until a
 * real OS process has actually run against real source media, and the only way
 * to obtain that marker is to come through `executeTool()`, which spawns one.
 *
 * `executionIntegrity.test.ts` scans the source tree and fails the build if any
 * other module constructs that marker. Adapter existence can therefore never
 * masquerade as execution: there is no code path that produces the evidence
 * marker without a process having run.
 */
import { spawn } from 'child_process';
import { createHash } from 'crypto';
import { createReadStream } from 'fs';
import { stat } from 'fs/promises';
import { readFile } from 'fs/promises';
import path from 'path';
import type { ToolRunProvenance, ResourceSampling } from '../../types';
import { runnerRoot } from './runnerRoot';

/** Cap captured stream text so a chatty tool cannot exhaust process memory. */
export const MAX_CAPTURED_STREAM_BYTES = 256 * 1024;

/**
 * How often a live child's RSS is read. Short enough that a ~1s tool yields
 * several samples, long enough that sampling costs nothing measurable.
 */
export const DEFAULT_SAMPLE_INTERVAL_MS = 100;

export interface ExecuteToolRequest {
  /** Registry id of the tool, e.g. 'ffprobe'. */
  tool: string;
  /** Real resolved version string, captured at provisioning time. */
  version: string;
  /** Absolute path of the executable actually invoked. */
  executablePath: string;
  /** Argument vector. Passed to spawn() directly — never shell-interpolated. */
  args: string[];
  /** Drive file id (or other stable id) of the media this run analyses. */
  sourceFileId: string;
  /** Local path of the media, used for hashing and existence checks. */
  sourcePath?: string;
  /** Precomputed source hash, to avoid re-hashing the same file per tool. */
  sourceHash?: string;
  /** Hard wall-clock ceiling. */
  timeoutMs?: number;
  /**
   * Explicit working directory. Defaults to the resolved runner root rather
   * than the caller's ambient cwd, so relative paths resolve predictably no
   * matter who invoked us.
   */
  cwd?: string;
  env?: Record<string, string>;
  /** Override the RSS sampling interval (tests use a tighter one). */
  sampleIntervalMs?: number;
  /** Ids of artifacts this run is expected to produce, filled in by adapters. */
  derivedArtifactIds?: string[];
}

export interface ExecuteToolResult {
  provenance: ToolRunProvenance;
  stdout: string;
  stderr: string;
  timedOut: boolean;
}

function truncate(buf: string): string {
  if (buf.length <= MAX_CAPTURED_STREAM_BYTES) return buf;
  return buf.slice(0, MAX_CAPTURED_STREAM_BYTES) + `\n…[truncated, ${buf.length} bytes total]`;
}

/**
 * Peak RSS for a live pid, sampled from /proc. Node's child_process exposes no
 * rusage, so the only honest way to report memory is to measure it while the
 * process is alive. Returns undefined where /proc is unavailable rather than
 * guessing a number.
 */
function sampleRss(pid: number): Promise<number | undefined> {
  return readFile(`/proc/${pid}/statm`, 'utf8')
    .then((txt) => {
      const pages = Number(txt.split(/\s+/)[1]);
      if (!Number.isFinite(pages)) return undefined;
      return (pages * 4096) / (1024 * 1024); // statm field 2 is resident 4KiB pages
    })
    .catch(() => undefined);
}

/** True where /proc-based sampling can work at all. */
export function samplingSupported(): boolean {
  return process.platform === 'linux';
}

export async function hashFile(filePath: string): Promise<string | undefined> {
  try {
    await stat(filePath);
  } catch {
    return undefined;
  }
  return new Promise((resolve) => {
    const h = createHash('sha256');
    const s = createReadStream(filePath);
    s.on('data', (c) => h.update(c));
    s.on('end', () => resolve(`sha256:${h.digest('hex')}`));
    s.on('error', () => resolve(undefined));
  });
}

/**
 * Run a real tool process and return provenance describing what actually
 * happened. Never throws for tool failure — a non-zero exit is a recorded
 * result, not an exception. Throws only for programmer error (empty argv).
 */
export async function executeTool(req: ExecuteToolRequest): Promise<ExecuteToolResult> {
  if (!req.executablePath) {
    throw new Error(`executeTool: no executablePath for ${req.tool}`);
  }

  const startedAt = new Date();
  const startMs = Date.now();
  const timeoutMs = req.timeoutMs ?? 15 * 60 * 1000;

  const sourceHash =
    req.sourceHash ?? (req.sourcePath ? await hashFile(req.sourcePath) : undefined);

  const cwd = req.cwd ?? runnerRoot();
  const sampleIntervalMs = req.sampleIntervalMs ?? DEFAULT_SAMPLE_INTERVAL_MS;

  let stdout = '';
  let stderr = '';
  let exitCode: number | null = null;
  let timedOut = false;
  let spawnError: string | undefined;

  // Memory telemetry. rssSamples stays empty when the child outlives no tick.
  const rssSamples: number[] = [];
  let spawned = false;

  await new Promise<void>((resolve) => {
    let child;
    try {
      child = spawn(req.executablePath, req.args, {
        cwd,
        env: req.env ? { ...process.env, ...req.env } : process.env,
        stdio: ['ignore', 'pipe', 'pipe'],
      });
    } catch (e: any) {
      spawnError = e?.message || String(e);
      return resolve();
    }

    let settled = false;
    const done = () => {
      if (settled) return;
      settled = true;
      clearInterval(sampler);
      clearTimeout(killer);
      resolve();
    };

    spawned = true;
    const sampler = setInterval(async () => {
      if (child.pid == null) return;
      const rss = await sampleRss(child.pid);
      if (rss !== undefined) rssSamples.push(rss);
    }, sampleIntervalMs);

    const killer = setTimeout(() => {
      timedOut = true;
      child.kill('SIGKILL');
    }, timeoutMs);

    child.stdout?.on('data', (d) => {
      if (stdout.length < MAX_CAPTURED_STREAM_BYTES * 2) stdout += d.toString();
    });
    child.stderr?.on('data', (d) => {
      if (stderr.length < MAX_CAPTURED_STREAM_BYTES * 2) stderr += d.toString();
    });

    child.on('error', (e: any) => {
      spawnError = e?.message || String(e);
      done();
    });
    child.on('close', (code) => {
      exitCode = code;
      done();
    });
  });

  const endedAt = new Date();
  const success = !spawnError && !timedOut && exitCode === 0;

  const peakRssMB = rssSamples.length ? Math.max(...rssSamples) : undefined;
  const avgRssMB = rssSamples.length
    ? rssSamples.reduce((a, b) => a + b, 0) / rssSamples.length
    : undefined;

  const resourceSampling: ResourceSampling = !samplingSupported()
    ? {
        sampleCount: 0,
        samplingIntervalMs: sampleIntervalMs,
        status: 'SAMPLING_UNSUPPORTED',
        reason: `/proc RSS sampling is not available on ${process.platform}`,
      }
    : rssSamples.length === 0
      ? {
          sampleCount: 0,
          samplingIntervalMs: sampleIntervalMs,
          status: 'NO_SAMPLE_CAPTURED',
          // Missing measurement is reported as missing. Never coerced to 0.
          reason: spawned
            ? `process exited in ${Date.now() - startMs}ms, before the first ${sampleIntervalMs}ms sampling tick`
            : 'process was never spawned',
        }
      : {
          sampleCount: rssSamples.length,
          samplingIntervalMs: sampleIntervalMs,
          status: 'SAMPLED',
          peakRssMB: Math.round(peakRssMB!),
          avgRssMB: Math.round(avgRssMB!),
        };

  const provenance: ToolRunProvenance = {
    // The one sanctioned construction site for this marker in the codebase.
    executionState: 'EXECUTED',
    tool: req.tool,
    version: req.version,
    executablePath: req.executablePath,
    command: [req.executablePath, ...req.args].join(' '),
    sourceFileId: req.sourceFileId,
    sourceHash,
    success,
    startTime: startedAt.toISOString(),
    endTime: endedAt.toISOString(),
    timestamp: endedAt.toISOString(),
    stdout: truncate(stdout),
    stderr: truncate(
      spawnError ? `${stderr}\n[spawn error] ${spawnError}` : timedOut ? `${stderr}\n[timeout] killed after ${timeoutMs}ms` : stderr
    ),
    exitCode,
    durationMs: Date.now() - startMs,
    derivedArtifactIds: req.derivedArtifactIds ?? [],
    resourceUsage: peakRssMB !== undefined ? { ramMB: Math.round(peakRssMB) } : undefined,
    cwd,
    resourceSampling,
  };

  return { provenance, stdout, stderr, timedOut };
}

/**
 * Provenance for a tool that is registered but has NOT run. Anything that has
 * not been through executeTool() must be described with this, so the
 * distinction between "we have an adapter" and "it produced evidence" is
 * carried in the data rather than assumed by the reader.
 */
/**
 * The measured facts a caller must produce before this module will mint EXECUTED.
 *
 * A second lane (src/server/mediaPipeline.ts) spawns its analyzers through
 * execFileAsync rather than through executeTool. It genuinely runs them — but
 * it used to hand queueManager a provenance record it had written by hand, with
 * success hardcoded true, durationMs 0, identical start and end stamps and a
 * command string containing the literal placeholder '<local-source>'. That
 * record reads the same whether the process ran or never ran.
 *
 * Rather than weaken the structural rule (the EXECUTED marker is constructible
 * in exactly one module, this one), that lane now RECORDS what it observed and
 * asks here for the marker. No observation, no marker.
 */
export interface MeasuredRun {
  tool: string;
  command: string;
  startedAt: string;
  endedAt: string;
  durationMs: number;
  success: boolean;
  exitCode: number | null;
  error?: string;
}

/** Mint EXECUTED from facts measured around a real spawn. */
export function executedFromMeasuredRun(
  run: MeasuredRun,
  sourceFileId: string,
  version = 'unknown',
  executablePath?: string
): ToolRunProvenance {
  return {
    executionState: 'EXECUTED',
    tool: run.tool,
    version,
    executablePath,
    command: run.command,
    sourceFileId,
    success: run.success,
    exitCode: run.exitCode ?? undefined,
    startTime: run.startedAt,
    endTime: run.endedAt,
    timestamp: run.endedAt,
    durationMs: run.durationMs,
    ...(run.error ? { stderr: run.error } : {}),
    derivedArtifactIds: [],
  } as ToolRunProvenance;
}

/**
 * The honest answer when nothing was observed.
 *
 * NOT the same as a tool that ran and found nothing — conflating those two is
 * the single most expensive bug this project has hit, and it has hit it four
 * separate times.
 */
export function notAttempted(
  tool: string,
  sourceFileId: string,
  reason: string,
  version = 'unknown'
): ToolRunProvenance {
  const now = new Date().toISOString();
  return {
    executionState: 'NOT_ATTEMPTED',
    tool, version, command: '', sourceFileId,
    success: false, startTime: now, endTime: now, timestamp: now,
    stderr: reason, exitCode: undefined, derivedArtifactIds: [],
  } as unknown as ToolRunProvenance;
}

export function adapterDefined(
  tool: string,
  sourceFileId: string,
  reason: string,
  version = 'unknown'
): ToolRunProvenance {
  const now = new Date().toISOString();
  return {
    executionState: 'ADAPTER_DEFINED',
    tool,
    version,
    command: '',
    sourceFileId,
    success: false,
    startTime: now,
    endTime: now,
    timestamp: now,
    stderr: reason,
    exitCode: undefined,
    derivedArtifactIds: [],
  };
}
