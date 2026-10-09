import { describe, it, expect } from 'vitest';
import path from 'path';
import os from 'os';
import { mkdtempSync } from 'fs';
import { ToolProvisioner, PROVISIONING_UNAVAILABLE, cmpVersion } from '../ToolProvisioner';
import type { ToolSpec } from '../specs';

const tmpRoot = () => mkdtempSync(path.join(os.tmpdir(), 'trippedd-prov-'));

/** A spec pointing at a binary that genuinely exists on any POSIX box. */
function realSpec(over: Partial<ToolSpec> = {}): ToolSpec {
  return {
    id: 'echo-tool', name: 'Echo', tier: 'CORE', category: 'Test',
    license: 'n/a', sourceRepository: 'n/a', description: 'test',
    capabilities: ['echo'],
    toolCapability: { canLaunch: false, canOpenProject: false, canImportAsset: false, canExportAsset: false, canSubmitJob: true },
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 1, diskMB: 0, resourceClass: 'LIGHT' },
    install: { kind: 'apt', package: 'coreutils' },
    detect: { bin: 'echo', versionArgs: ['1.2.3'], versionPattern: /([\d]+\.[\d]+\.[\d]+)/ },
    health: { kind: 'selftest', args: () => ['health-ok'], expect: (o) => o.includes('health-ok') },
    ...over,
  } as ToolSpec;
}

describe('ToolProvisioner — detection and versioning', () => {
  it('detects a present tool and captures its ACTUAL version from the tool itself', async () => {
    const p = new ToolProvisioner({ root: tmpRoot(), specs: [realSpec()] });
    await p.initialize();
    const t = p.getTool('echo-tool')!;

    expect(t.state).toBe('AVAILABLE');
    // Version came from running the binary, not from the spec.
    expect(t.version).toBe('1.2.3');
    expect(t.executablePath).toBeTruthy();
    expect(t.installSource).toBe('system');
  }, 60_000);

  it('detects a missing tool rather than assuming it exists', async () => {
    const spec = realSpec({
      id: 'ghost-tool',
      detect: { bin: 'definitely_not_a_real_binary_xyz', versionArgs: ['--version'], versionPattern: /(\d+)/ },
      install: { kind: 'manual', reason: 'no automated install path' },
    });
    const p = new ToolProvisioner({ root: tmpRoot(), specs: [spec] });
    await p.initialize();
    const t = p.getTool('ghost-tool')!;

    expect(t.state).not.toBe('AVAILABLE');
    expect(['UNAVAILABLE', 'NOT_INSTALLED', 'INSTALL_FAILED']).toContain(t.state);
    expect(t.version).toBeUndefined();
  }, 60_000);
});

describe('ToolProvisioner — AVAILABLE requires a passing health check', () => {
  it('does NOT report AVAILABLE when the health check fails, even though the tool exists', async () => {
    const spec = realSpec({
      id: 'unhealthy-tool',
      // Detects fine (echo exists, prints a version) but the health run's
      // output is not what the tool is supposed to produce.
      health: { kind: 'selftest', args: () => ['wrong-output'], expect: (o) => o.includes('health-ok') },
    });
    const p = new ToolProvisioner({ root: tmpRoot(), specs: [spec] });
    await p.initialize();
    const t = p.getTool('unhealthy-tool')!;

    expect(t.state).toBe('HEALTH_CHECK_FAILED');
    expect(t.lastHealthCheck?.ok).toBe(false);
    // Adapter exists, tool exists, version resolved — still not AVAILABLE.
    expect(t.version).toBe('1.2.3');
  }, 60_000);

  it('records the health check that justified AVAILABLE', async () => {
    const p = new ToolProvisioner({ root: tmpRoot(), specs: [realSpec()] });
    await p.initialize();
    const hc = p.getTool('echo-tool')!.lastHealthCheck!;

    expect(hc.ok).toBe(true);
    expect(hc.ranAt).toBeTruthy();
    expect(hc.exitCode).toBe(0);
    expect(typeof hc.durationMs).toBe('number');
  }, 60_000);

  it('a non-zero exit health check fails the tool', async () => {
    const spec = realSpec({
      id: 'exit-fail-tool',
      detect: { bin: 'false', versionArgs: [], versionPattern: /(\d+\.\d+\.\d+)/ },
      health: { kind: 'selftest', args: () => [] },
    });
    const p = new ToolProvisioner({ root: tmpRoot(), specs: [spec] });
    await p.initialize();
    expect(p.getTool('exit-fail-tool')!.state).not.toBe('AVAILABLE');
  }, 60_000);
});

describe('ToolProvisioner — provisioning is attempted only when supported', () => {
  it('reports PROVISIONING_UNAVAILABLE when the environment forbids installation', async () => {
    const spec = realSpec({
      id: 'needs-install',
      detect: { bin: 'definitely_not_a_real_binary_xyz', versionArgs: ['-v'], versionPattern: /(\d+)/ },
    });
    const p = new ToolProvisioner({
      root: tmpRoot(), specs: [spec],
      forceEnvironment: { canApt: false, canPip: false, reason: 'sandboxed' },
    });
    await p.initialize();
    const t = p.getTool('needs-install')!;

    expect(t.state).toBe('UNAVAILABLE');
    expect(t.installError).toContain(PROVISIONING_UNAVAILABLE);
    expect(t.provisionedByApp).toBeFalsy();
  }, 60_000);

  it('does not install opt-in tiers just because they are missing', async () => {
    const spec = realSpec({
      id: 'expensive-tool', tier: 'ENHANCED',
      detect: { bin: 'definitely_not_a_real_binary_xyz', versionArgs: ['-v'], versionPattern: /(\d+)/ },
    });
    const p = new ToolProvisioner({
      root: tmpRoot(), specs: [spec],
      forceEnvironment: { canApt: true, canPip: true },
    });
    await p.initialize();
    const t = p.getTool('expensive-tool')!;

    expect(t.state).toBe('NOT_INSTALLED');
    expect(t.installError).toMatch(/opt-in/i);
  }, 60_000);

  it('failed provisioning leaves the tool unavailable, never AVAILABLE', async () => {
    const spec = realSpec({
      id: 'broken-install',
      detect: { bin: 'definitely_not_a_real_binary_xyz', versionArgs: ['-v'], versionPattern: /(\d+)/ },
      // A package that cannot resolve: the install must fail honestly.
      install: { kind: 'apt', package: 'a-package-that-does-not-exist-zzz' },
    });
    const p = new ToolProvisioner({
      root: tmpRoot(), specs: [spec],
      forceEnvironment: { canApt: true, canPip: false },
    });
    await p.initialize();
    const t = p.getTool('broken-install')!;

    expect(t.state).not.toBe('AVAILABLE');
    expect(['INSTALL_FAILED', 'UNAVAILABLE']).toContain(t.state);
    expect(t.installError).toBeTruthy();
  }, 300_000);
});

describe('ToolProvisioner — version gating', () => {
  it('flags a version below the minimum as VERSION_UNSUPPORTED', async () => {
    const p = new ToolProvisioner({
      root: tmpRoot(), specs: [realSpec({ id: 'old-tool', minVersion: '9.9.9' })],
    });
    await p.initialize();
    const t = p.getTool('old-tool')!;

    expect(t.state).toBe('VERSION_UNSUPPORTED');
    expect(t.installError).toContain('9.9.9');
  }, 60_000);

  it('compares versions numerically, not lexically', () => {
    expect(cmpVersion('1.10.0', '1.9.0')).toBe(1);
    expect(cmpVersion('0.7.1', '0.7.1')).toBe(0);
    expect(cmpVersion('5.3.4', '6.1.1')).toBe(-1);
  });
});

describe('ToolProvisioner — health checks use real work, not --version', () => {
  it('every shipped spec health check is more than a version probe', async () => {
    const { TOOL_SPECS } = await import('../specs');
    for (const s of TOOL_SPECS) {
      const args = s.health.args({ video: '/fx/v.mp4', image: '/fx/i.png', audio: '/fx/a.wav' });
      const joined = args.join(' ');
      // A health check that only asks for a version proves nothing about
      // whether the tool can actually process media.
      expect(joined, `${s.id} health check is a bare version probe`).not.toMatch(/^-?-version$/);
      expect(['media', 'image', 'import', 'selftest']).toContain(s.health.kind);
    }
  });

  it('media-kind health checks reference the real media fixture', async () => {
    const { TOOL_SPECS } = await import('../specs');
    const media = TOOL_SPECS.filter((s) => s.health.kind === 'media');
    expect(media.length).toBeGreaterThan(0);
    for (const s of media) {
      const args = s.health.args({ video: '/fx/v.mp4', image: '/fx/i.png', audio: '/fx/a.wav' });
      expect(args.join(' '), `${s.id}`).toContain('/fx/v.mp4');
    }
  });
});
