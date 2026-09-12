/**
 * Detect → version → health-check → (install) → verify → register → persist.
 *
 * The rule this module exists to enforce: a tool is AVAILABLE only after a real
 * process of that tool has run a real health check successfully. Having an
 * adapter, or having `--version` succeed, is never sufficient.
 */
import path from 'path';
import { existsSync } from 'fs';
import { readFile, writeFile, mkdir } from 'fs/promises';
import { executeTool } from '../execution/executor';
import { runnerRoot } from '../execution/runnerRoot';
import { ensureFixtures, type Fixtures } from './fixtures';
import { TOOL_SPECS, AUTO_PROVISION_TIERS, type ToolSpec, type ToolTier } from './specs';
import { ModelArtifactManager, WHISPERX_ALIGN_EN } from './ModelArtifactManager';
import type { ToolStatus } from '../../types';

export const PROVISIONING_UNAVAILABLE =
  'PROVISIONING_UNAVAILABLE — environment does not permit dependency installation';

export interface HealthCheckResult {
  ok: boolean;
  kind: ToolSpec['health']['kind'];
  ranAt: string;
  detail: string;
  exitCode?: number | null;
  durationMs?: number;
}

export interface ProvisionedTool {
  id: string;
  name: string;
  tier: ToolTier;
  category: string;
  license: string;
  sourceRepository: string;
  description: string;
  capabilities: string[];
  runtimeRequirements: ToolSpec['runtimeRequirements'];

  state: ToolStatus;
  version?: string;
  executablePath?: string;
  /** Where it came from: 'system', 'apt:<pkg>', 'pip:<pkg>', or undefined. */
  installSource?: string;
  installError?: string;
  lastHealthCheck?: HealthCheckResult;
  /** True when the tool was installed by us in this process. */
  provisionedByApp?: boolean;
}

export interface EnvironmentCapability {
  canApt: boolean;
  canPip: boolean;
  reason?: string;
}

interface PersistedEntry {
  version?: string;
  executablePath?: string;
  installSource?: string;
  state: ToolStatus;
  healthCheckedAt?: string;
}

export interface ProvisionerOptions {
  root?: string;
  /** Extra tiers to provision beyond CORE/PRIMARY, e.g. ['ENHANCED']. */
  enableTiers?: ToolTier[];
  /** Specific tool ids to provision regardless of tier. */
  enableTools?: string[];
  /** Hard off-switch, used by tests and locked-down deployments. */
  allowInstall?: boolean;
  specs?: ToolSpec[];
  /**
   * Test seam: pretend the environment has (or lacks) install capability, so
   * the PROVISIONING_UNAVAILABLE path is exercisable without a locked-down box.
   */
  forceEnvironment?: EnvironmentCapability;
}

export class ToolProvisioner {
  private tools = new Map<string, ProvisionedTool>();
  private specs: ToolSpec[];
  private root: string;
  private venvPath: string;
  private binDir: string;
  private statePath: string;
  private fixtureDir: string;
  private opts: ProvisionerOptions;
  private env: EnvironmentCapability = { canApt: false, canPip: false };
  private fixtures?: Fixtures;
  private models: ModelArtifactManager;
  private modelPurge?: { removed: string[]; bytesReclaimed: number };

  constructor(opts: ProvisionerOptions = {}) {
    this.opts = opts;
    this.specs = opts.specs ?? TOOL_SPECS;
    this.root = opts.root ?? runnerRoot();
    // Isolated, app-owned locations. Nothing outside these is touched by pip.
    this.venvPath = path.join(this.root, '.trippedd_venv');
    this.binDir = path.join(this.root, '.trippedd_tools', 'bin');
    this.statePath = path.join(this.root, '.trippedd_toolchain.json');
    this.fixtureDir = path.join(this.root, '.trippedd_tools', 'fixtures');
    this.models = new ModelArtifactManager(path.join(this.root, '.trippedd_tools', 'models'));
  }

  getModels(): ModelArtifactManager {
    return this.models;
  }

  /** What the boot-time model sweep removed, if anything. */
  getModelPurge() {
    return this.modelPurge;
  }

  getTools(): ProvisionedTool[] {
    return Array.from(this.tools.values());
  }
  getTool(id: string): ProvisionedTool | undefined {
    return this.tools.get(id);
  }
  isAvailable(id: string): boolean {
    return this.tools.get(id)?.state === 'AVAILABLE';
  }
  getEnvironment(): EnvironmentCapability {
    return this.env;
  }

  private venvBin(name: string): string {
    return path.join(this.venvPath, 'bin', name);
  }
  private pythonPath(): string {
    const v = this.venvBin('python');
    return existsSync(v) ? v : 'python3';
  }

  /** Which tiers/tools we are permitted to install without being asked again. */
  private shouldAutoProvision(spec: ToolSpec): boolean {
    if (this.opts.allowInstall === false) return false;
    if (this.opts.enableTools?.includes(spec.id)) return true;
    const tiers = [...AUTO_PROVISION_TIERS, ...(this.opts.enableTiers ?? [])];
    return tiers.includes(spec.tier);
  }

  // ---------------------------------------------------------------- discovery

  private async which(bin: string): Promise<string | undefined> {
    const local = this.venvBin(bin);
    if (existsSync(local)) return local;
    const owned = path.join(this.binDir, bin);
    if (existsSync(owned)) return owned;
    const r = await executeTool({
      tool: 'which', version: 'n/a', executablePath: '/usr/bin/which',
      args: [bin], sourceFileId: 'provisioning', timeoutMs: 10_000,
    });
    const p = r.stdout.trim().split('\n')[0];
    return r.provenance.success && p ? p : undefined;
  }

  /**
   * Resolve the executable and its REAL version by running it. Returns
   * undefined when the tool is genuinely not present.
   */
  private async detect(spec: ToolSpec): Promise<{ exe: string; version: string } | undefined> {
    if (spec.detect.bin) {
      const exe = await this.which(spec.detect.bin);
      if (!exe) return undefined;
      const r = await executeTool({
        tool: spec.id, version: 'probing', executablePath: exe,
        args: spec.detect.versionArgs ?? ['--version'],
        sourceFileId: 'provisioning', timeoutMs: 30_000,
      });
      const combined = `${r.stdout}\n${r.stderr}`;
      const m = combined.match(spec.detect.versionPattern);
      // Some tools print version to stderr and exit non-zero; a parsed version
      // is the real signal that the binary is the tool we think it is.
      if (!m) return r.provenance.success ? { exe, version: 'unknown' } : undefined;
      return { exe, version: m[1] };
    }

    if (spec.detect.pythonModule) {
      const py = this.pythonPath();
      const r = await executeTool({
        tool: spec.id, version: 'probing', executablePath: py,
        args: spec.detect.versionArgs!, sourceFileId: 'provisioning', timeoutMs: 120_000,
      });
      if (!r.provenance.success) return undefined;
      const m = `${r.stdout}`.match(spec.detect.versionPattern);
      return { exe: py, version: m ? m[1] : 'unknown' };
    }

    return undefined;
  }

  // ------------------------------------------------------------ health checks

  /**
   * Run the tool's minimal REAL workload. This is what separates AVAILABLE from
   * "an adapter exists".
   */
  private async healthCheck(
    spec: ToolSpec,
    exe: string,
    version: string
  ): Promise<HealthCheckResult> {
    const ranAt = new Date().toISOString();
    const fx = this.fixtures;

    if (!fx) {
      return { ok: false, kind: spec.health.kind, ranAt, detail: 'fixtures unavailable' };
    }
    // Video/audio fixtures need ffmpeg. Without them a media check cannot run,
    // and saying so is better than silently downgrading to a version check.
    if ((spec.health.kind === 'media') && !fx.hasMedia) {
      return {
        ok: false, kind: spec.health.kind, ranAt,
        detail: 'no media fixture available (ffmpeg missing) — cannot verify against real media',
      };
    }

    const isPython = !!spec.detect.pythonModule;
    const execPath = isPython ? this.pythonPath() : exe;
    const args = spec.health.args({ video: fx.video, image: fx.image, audio: fx.audio });

    const r = await executeTool({
      tool: spec.id, version, executablePath: execPath, args,
      sourceFileId: `healthcheck:${spec.id}`,
      sourcePath: spec.health.kind === 'image' ? fx.image : fx.hasMedia ? fx.video : undefined,
      timeoutMs: 180_000,
    });

    let ok = r.provenance.success;
    let detail = ok ? 'health check passed' : `exit ${r.provenance.exitCode}: ${r.stderr.trim().slice(0, 200)}`;

    // An exit code of 0 is not always proof the tool did the job.
    if (ok && spec.health.expect && !spec.health.expect(r.stdout)) {
      ok = false;
      detail = 'ran successfully but produced unusable output';
    }

    return {
      ok, kind: spec.health.kind, ranAt, detail,
      exitCode: r.provenance.exitCode, durationMs: r.provenance.durationMs,
    };
  }

  // -------------------------------------------------------------- installation

  private async probeEnvironment(): Promise<EnvironmentCapability> {
    const reasons: string[] = [];

    // apt: needs the binary and root. A simulated install proves both without
    // changing anything.
    let canApt = false;
    if (existsSync('/usr/bin/apt-get')) {
      if (typeof process.getuid === 'function' && process.getuid() !== 0) {
        reasons.push('apt-get requires root');
      } else {
        const r = await executeTool({
          tool: 'apt-get', version: 'n/a', executablePath: '/usr/bin/apt-get',
          args: ['-s', 'install', 'ca-certificates'], sourceFileId: 'provisioning',
          timeoutMs: 120_000,
        });
        canApt = r.provenance.success;
        if (!canApt) reasons.push('apt-get simulate failed');
      }
    } else {
      reasons.push('apt-get not present');
    }

    // pip: a venv we can create and write to.
    let canPip = existsSync(this.venvBin('pip'));
    if (!canPip) {
      const r = await executeTool({
        tool: 'venv', version: 'n/a', executablePath: 'python3',
        args: ['-m', 'venv', this.venvPath], sourceFileId: 'provisioning',
        timeoutMs: 180_000,
      });
      canPip = r.provenance.success && existsSync(this.venvBin('pip'));
      if (!canPip) reasons.push('cannot create python venv');
    }

    return { canApt, canPip, reason: reasons.length ? reasons.join('; ') : undefined };
  }

  private async aptInstall(pkg: string): Promise<{ ok: boolean; error?: string }> {
    const run = (args: string[], timeoutMs = 600_000) =>
      executeTool({
        tool: 'apt-get', version: 'n/a', executablePath: '/usr/bin/apt-get',
        args, sourceFileId: 'provisioning', timeoutMs,
        env: { DEBIAN_FRONTEND: 'noninteractive' },
      });

    let r = await run(['install', '-y', '--no-install-recommends', pkg]);
    if (r.provenance.success) return { ok: true };

    // MEASURED: a stale package index 404s on superseded versions, which looks
    // exactly like the package not existing. Refresh once and retry before
    // concluding anything.
    if (/404|Unable to fetch|Failed to fetch|apt-get update/i.test(r.stderr + r.stdout)) {
      const upd = await run(['update'], 300_000);
      if (upd.provenance.success) {
        r = await run(['install', '-y', '--no-install-recommends', pkg]);
        if (r.provenance.success) return { ok: true };
      }
    }
    return { ok: false, error: r.stderr.trim().slice(0, 400) || `exit ${r.provenance.exitCode}` };
  }

  private async pipInstall(pkg: string): Promise<{ ok: boolean; error?: string }> {
    const r = await executeTool({
      tool: 'pip', version: 'n/a', executablePath: this.venvBin('pip'),
      args: ['install', '--disable-pip-version-check', pkg],
      sourceFileId: 'provisioning', timeoutMs: 1_800_000,
    });
    return r.provenance.success
      ? { ok: true }
      : { ok: false, error: r.stderr.trim().slice(0, 400) || `exit ${r.provenance.exitCode}` };
  }

  // ------------------------------------------------------------- persistence

  private async loadState(): Promise<Record<string, PersistedEntry>> {
    try {
      return JSON.parse(await readFile(this.statePath, 'utf8'));
    } catch {
      return {};
    }
  }

  private async saveState(): Promise<void> {
    const out: Record<string, PersistedEntry> = {};
    for (const t of this.tools.values()) {
      out[t.id] = {
        version: t.version, executablePath: t.executablePath,
        installSource: t.installSource, state: t.state,
        healthCheckedAt: t.lastHealthCheck?.ranAt,
      };
    }
    try {
      await mkdir(path.dirname(this.statePath), { recursive: true });
      await writeFile(this.statePath, JSON.stringify(out, null, 2));
    } catch {
      /* persistence is an optimisation; failing to write must not break boot */
    }
  }

  // ------------------------------------------------------------------ driver

  async initialize(): Promise<ProvisionedTool[]> {
    this.env = this.opts.forceEnvironment ?? (await this.probeEnvironment());

    // ffmpeg has to exist before media fixtures can be generated, so resolve it
    // up front and use it if present.
    const ffmpegExe = await this.which('ffmpeg');
    this.fixtures = await ensureFixtures(this.fixtureDir, async (args) => {
      if (!ffmpegExe) return false;
      const r = await executeTool({
        tool: 'ffmpeg', version: 'fixture', executablePath: ffmpegExe,
        args, sourceFileId: 'fixture-gen', timeoutMs: 120_000,
      });
      return r.provenance.success;
    });

    // Sweep corrupt or half-downloaded model artifacts BEFORE any tool is
    // declared available. A truncated model surfaces here, as a named artifact
    // problem, instead of as an opaque loader error minutes into a real job.
    this.modelPurge = await this.models.purgeInvalid([WHISPERX_ALIGN_EN]);
    if (this.modelPurge.removed.length) {
      console.log(`[toolchain] purged ${this.modelPurge.removed.length} invalid model artifact(s), reclaimed ${(this.modelPurge.bytesReclaimed / 1048576).toFixed(0)}MB`);
    }

    // Sweep model repos nothing asks for any more. purgeInvalid above only
    // catches CORRUPT files; a perfectly valid model that is simply never
    // requested again is invisible to it, and those are what fill the disk.
    // A stale 1.2 GB Korean alignment model — pulled once by a
    // language-detection miss that has since been fixed — is what starved the
    // longest clip in the shoot of the 800 MB it needed.
    const keepModel = process.env.TRIPPEDD_WHISPER_MODEL
      || 'Systran/faster-distil-whisper-large-v3';
    const repoSweep = await this.models.purgeUnusedModelRepos({ keepRepoIds: [keepModel] });
    if (repoSweep.removed.length) {
      console.log(`[toolchain] removed ${repoSweep.removed.length} unused model repo(s), reclaimed ${(repoSweep.bytesReclaimed / 1048576).toFixed(0)}MB: ${repoSweep.removed.join(', ')}`);
    }

    const persisted = await this.loadState();

    for (const spec of this.specs) {
      this.tools.set(spec.id, {
        id: spec.id, name: spec.name, tier: spec.tier, category: spec.category,
        license: spec.license, sourceRepository: spec.sourceRepository,
        description: spec.description, capabilities: spec.capabilities,
        runtimeRequirements: spec.runtimeRequirements,
        state: 'NOT_INSTALLED',
      });
      await this.provisionOne(spec, persisted[spec.id]);
    }

    // Media fixtures may only become possible after ffmpeg is installed, so a
    // second pass re-checks tools whose health check could not run before.
    if (!this.fixtures.hasMedia && this.isAvailable('ffmpeg')) {
      const exe = this.tools.get('ffmpeg')!.executablePath!;
      this.fixtures = await ensureFixtures(this.fixtureDir, async (args) => {
        const r = await executeTool({
          tool: 'ffmpeg', version: 'fixture', executablePath: exe,
          args, sourceFileId: 'fixture-gen', timeoutMs: 120_000,
        });
        return r.provenance.success;
      });
      for (const spec of this.specs) {
        const t = this.tools.get(spec.id)!;
        if (t.state === 'HEALTH_CHECK_FAILED' && t.executablePath) {
          const hc = await this.healthCheck(spec, t.executablePath, t.version ?? 'unknown');
          t.lastHealthCheck = hc;
          if (hc.ok) { t.state = 'AVAILABLE'; t.installError = undefined; }
        }
      }
    }

    await this.saveState();
    return this.getTools();
  }

  private async provisionOne(spec: ToolSpec, prior?: PersistedEntry): Promise<void> {
    const tool = this.tools.get(spec.id)!;

    // 1. Detect + real version.
    let found = await this.detect(spec);

    // 2. Install if missing and we are allowed to.
    if (!found) {
      if (!this.shouldAutoProvision(spec)) {
        tool.state = 'NOT_INSTALLED';
        tool.installError =
          `not installed; ${spec.tier} tier is opt-in (enable explicitly to provision)`;
        return;
      }

      const plan = spec.install;
      const permitted =
        plan.kind === 'apt' ? this.env.canApt : plan.kind === 'pip' ? this.env.canPip : false;

      if (!permitted) {
        tool.state = 'UNAVAILABLE';
        tool.installError =
          plan.kind === 'manual'
            ? plan.reason
            : `${PROVISIONING_UNAVAILABLE}${this.env.reason ? ` (${this.env.reason})` : ''}`;
        return;
      }

      tool.state = 'INSTALLING';
      const res =
        plan.kind === 'apt' ? await this.aptInstall(plan.package)
        : plan.kind === 'pip' ? await this.pipInstall(plan.package)
        : { ok: false, error: 'no install plan' };

      if (!res.ok) {
        tool.state = 'INSTALL_FAILED';
        tool.installError = res.error;
        return;
      }

      // 3. Verify the install actually produced a working executable.
      found = await this.detect(spec);
      if (!found) {
        tool.state = 'INSTALL_FAILED';
        tool.installError = 'install reported success but the tool is still not detectable';
        return;
      }
      tool.provisionedByApp = true;
      tool.installSource = `${plan.kind}:${(plan as any).package}`;
    } else {
      tool.installSource = prior?.installSource ?? 'system';
    }

    tool.executablePath = found.exe;
    tool.version = found.version;

    // 4. Minimum version gate.
    if (spec.minVersion && found.version !== 'unknown' && cmpVersion(found.version, spec.minVersion) < 0) {
      tool.state = 'VERSION_UNSUPPORTED';
      tool.installError = `found ${found.version}, need >= ${spec.minVersion}`;
      return;
    }

    // 5. AVAILABLE only after a real health check passes.
    const hc = await this.healthCheck(spec, found.exe, found.version);
    tool.lastHealthCheck = hc;
    if (!hc.ok) {
      tool.state = 'HEALTH_CHECK_FAILED';
      tool.installError = hc.detail;
      return;
    }

    tool.state = 'AVAILABLE';
    tool.installError = undefined;
  }
}

/** Numeric-segment version comparison; non-numeric suffixes are ignored. */
export function cmpVersion(a: string, b: string): number {
  const pa = a.split(/[.\-+]/).map((x) => parseInt(x, 10));
  const pb = b.split(/[.\-+]/).map((x) => parseInt(x, 10));
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const x = Number.isFinite(pa[i]) ? pa[i] : 0;
    const y = Number.isFinite(pb[i]) ? pb[i] : 0;
    if (x !== y) return x < y ? -1 : 1;
  }
  return 0;
}
