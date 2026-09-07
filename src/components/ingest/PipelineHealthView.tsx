import React, { useState, useEffect, useCallback } from 'react';
import {
  Activity, CheckCircle2, AlertTriangle, XCircle, RefreshCw, Download,
  HardDrive, Cpu, Radio, PauseCircle, PlayCircle, Clock,
} from 'lucide-react';

/**
 * Pipeline health.
 *
 * Every number here is read from /api/pipeline/health, which derives it from
 * the live queue and the real tool registry. Nothing on this screen is a
 * placeholder or a demo value — if the server has not reported yet, the view
 * says so rather than showing a plausible-looking zero.
 */

type ToolState =
  | 'AVAILABLE' | 'INSTALLING' | 'NOT_INSTALLED' | 'UNAVAILABLE'
  | 'INSTALL_FAILED' | 'VERSION_UNSUPPORTED' | 'HEALTH_CHECK_FAILED';

interface HealthCheck {
  ok: boolean; kind: string; ranAt: string; detail: string;
  exitCode?: number | null; durationMs?: number;
}

interface ToolRow {
  id: string; name: string; tier: string; state: ToolState;
  version: string | null; executablePath: string | null;
  installSource: string | null; installError: string | null;
  capabilities: string[];
  runtimeRequirements: { cpu: boolean; gpu: boolean; ramMB: number; diskMB: number; resourceClass: string };
  lastHealthCheck: HealthCheck | null;
  provisionedByApp: boolean;
}

interface Health {
  tools: ToolRow[];
  environment: { canApt: boolean; canPip: boolean; reason?: string };
  counts: {
    discovered: number; queued: number; processing: number;
    processed: number; failed: number; unavailable: number;
  };
  scheduler: {
    active: Record<string, number>;
    limits: { light: number; cpuHeavy: number; gpu: number; diskQuotaMB: number };
    queuedWaiters: number; diskUsedMB: number; diskQuotaMB: number;
  };
  watcher: { running: boolean; folderId?: string; intervalMs?: number; lastScanAt?: string; lastResult?: any };
}

const STATE_STYLE: Record<ToolState, { cls: string; Icon: typeof CheckCircle2 }> = {
  AVAILABLE:            { cls: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20', Icon: CheckCircle2 },
  INSTALLING:           { cls: 'text-blue-400 bg-blue-500/10 border-blue-500/20',          Icon: RefreshCw },
  NOT_INSTALLED:        { cls: 'text-neutral-400 bg-neutral-800 border-neutral-700',       Icon: Download },
  UNAVAILABLE:          { cls: 'text-amber-400 bg-amber-500/10 border-amber-500/20',       Icon: AlertTriangle },
  INSTALL_FAILED:       { cls: 'text-red-400 bg-red-500/10 border-red-500/20',             Icon: XCircle },
  VERSION_UNSUPPORTED:  { cls: 'text-amber-400 bg-amber-500/10 border-amber-500/20',       Icon: AlertTriangle },
  HEALTH_CHECK_FAILED:  { cls: 'text-red-400 bg-red-500/10 border-red-500/20',             Icon: XCircle },
};

function ago(iso?: string): string {
  if (!iso) return 'never';
  const s = Math.round((Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.round(s / 60)}m ago`;
  return `${Math.round(s / 3600)}h ago`;
}

export function PipelineHealthView({ accessToken, folderUrl }: { accessToken?: string | null; folderUrl?: string }) {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const res = await fetch('/api/pipeline/health');
      if (!res.ok) throw new Error(`health endpoint returned ${res.status}`);
      setHealth(await res.json());
      setError(null);
    } catch (e: any) {
      setError(e.message);
    }
  }, []);

  useEffect(() => {
    load();
    const t = setInterval(load, 3000);
    return () => clearInterval(t);
  }, [load]);

  const provision = async (tiers: string[]) => {
    setBusy(tiers.join(','));
    try {
      await fetch('/api/pipeline/provision', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tiers }),
      });
      await load();
    } finally { setBusy(null); }
  };

  const toggleWatch = async () => {
    const running = health?.watcher?.running;
    setBusy('watch');
    try {
      const folderId = folderUrl?.split('/').pop();
      await fetch(`/api/pipeline/watch/${running ? 'stop' : 'start'}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folderId, token: accessToken }),
      });
      await load();
    } finally { setBusy(null); }
  };

  if (error && !health) {
    return (
      <div className="border border-red-500/20 bg-red-500/5 rounded-lg p-4 text-sm text-red-400">
        <AlertTriangle size={14} className="inline mr-2" />
        Pipeline health unavailable — {error}
      </div>
    );
  }
  if (!health) {
    return <div className="text-neutral-500 text-sm p-4">Loading pipeline health…</div>;
  }

  const c = health.counts;
  const s = health.scheduler;
  const available = health.tools.filter((t) => t.state === 'AVAILABLE').length;
  const optIn = health.tools.filter((t) => t.tier === 'ENHANCED' || t.tier === 'INTERCHANGE');
  const optInMissing = optIn.filter((t) => t.state !== 'AVAILABLE');

  return (
    <div className="space-y-4">
      {/* ---- Drive counts, derived from the live queue ---- */}
      <div className="border border-neutral-800 rounded-lg bg-neutral-950">
        <div className="flex items-center justify-between px-4 py-3 border-b border-neutral-800">
          <div className="flex items-center gap-2">
            <Radio size={15} className={health.watcher.running ? 'text-emerald-400' : 'text-neutral-500'} />
            <span className="font-bold text-sm tracking-tight">DRIVE PIPELINE</span>
            <span className={`text-[10px] px-2 py-0.5 rounded border font-bold ${
              health.watcher.running
                ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
                : 'text-neutral-500 bg-neutral-900 border-neutral-800'}`}>
              {health.watcher.running ? 'AUTO-INGEST ON' : 'AUTO-INGEST OFF'}
            </span>
          </div>
          <button
            onClick={toggleWatch}
            disabled={busy === 'watch' || !accessToken}
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40"
            title={!accessToken ? 'Connect Google Drive first' : ''}
          >
            {health.watcher.running ? <PauseCircle size={13} /> : <PlayCircle size={13} />}
            {health.watcher.running ? 'Stop watching' : 'Watch folder'}
          </button>
        </div>

        <div className="grid grid-cols-5 divide-x divide-neutral-800">
          {[
            { label: 'discovered', v: c.discovered, cls: 'text-neutral-200' },
            { label: 'processed',  v: c.processed,  cls: 'text-emerald-400' },
            { label: 'processing', v: c.processing, cls: 'text-blue-400' },
            { label: 'queued',     v: c.queued,     cls: 'text-neutral-400' },
            { label: 'failed',     v: c.failed,     cls: c.failed > 0 ? 'text-red-400' : 'text-neutral-500' },
          ].map((x) => (
            <div key={x.label} className="px-4 py-3">
              <div className={`text-2xl font-bold tabular-nums ${x.cls}`}>{x.v}</div>
              <div className="text-[10px] uppercase tracking-wider text-neutral-500 mt-0.5">{x.label}</div>
            </div>
          ))}
        </div>

        {health.watcher.running && (
          <div className="px-4 py-2 border-t border-neutral-800 text-[11px] text-neutral-500 flex items-center gap-2">
            <Clock size={11} />
            Last scan {ago(health.watcher.lastScanAt)}
            {health.watcher.lastResult?.error && (
              <span className="text-amber-400">· {health.watcher.lastResult.error}</span>
            )}
            {typeof health.watcher.intervalMs === 'number' && (
              <span>· every {Math.round(health.watcher.intervalMs / 1000)}s</span>
            )}
          </div>
        )}
      </div>

      {/* ---- Resource ceilings ---- */}
      <div className="border border-neutral-800 rounded-lg bg-neutral-950 px-4 py-3">
        <div className="flex items-center gap-2 mb-2">
          <Cpu size={14} className="text-neutral-400" />
          <span className="font-bold text-xs tracking-tight">RESOURCE LIMITS</span>
        </div>
        <div className="flex flex-wrap gap-x-6 gap-y-1 text-[11px] text-neutral-400 tabular-nums">
          <span>light <b className="text-neutral-200">{s.active.LIGHT ?? 0}/{s.limits.light}</b></span>
          <span>cpu-heavy <b className="text-neutral-200">{s.active.CPU_HEAVY ?? 0}/{s.limits.cpuHeavy}</b></span>
          <span>gpu <b className="text-neutral-200">{s.active.GPU ?? 0}/{s.limits.gpu}</b></span>
          <span className="flex items-center gap-1">
            <HardDrive size={11} /> temp
            <b className="text-neutral-200">{s.diskUsedMB}/{s.diskQuotaMB} MB</b>
          </span>
          {s.queuedWaiters > 0 && <span className="text-amber-400">{s.queuedWaiters} waiting for a slot</span>}
        </div>
      </div>

      {/* ---- Tool table ---- */}
      <div className="border border-neutral-800 rounded-lg bg-neutral-950 overflow-hidden">
        <div className="flex items-center justify-between px-4 py-3 border-b border-neutral-800">
          <div className="flex items-center gap-2">
            <Activity size={15} className="text-neutral-400" />
            <span className="font-bold text-sm tracking-tight">TOOLCHAIN</span>
            <span className="text-[11px] text-neutral-500">{available}/{health.tools.length} available</span>
          </div>
          {optInMissing.length > 0 && (
            <div className="flex gap-2">
              {optInMissing.some((t) => t.tier === 'ENHANCED') && (
                <button
                  onClick={() => provision(['ENHANCED'])}
                  disabled={!!busy}
                  className="text-[11px] px-2.5 py-1 rounded border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40"
                >
                  {busy === 'ENHANCED' ? 'Installing…' : 'Install enhanced tier'}
                </button>
              )}
              {optInMissing.some((t) => t.tier === 'INTERCHANGE') && (
                <button
                  onClick={() => provision(['INTERCHANGE'])}
                  disabled={!!busy}
                  className="text-[11px] px-2.5 py-1 rounded border border-neutral-700 hover:bg-neutral-900 disabled:opacity-40"
                >
                  {busy === 'INTERCHANGE' ? 'Installing…' : 'Install interchange'}
                </button>
              )}
            </div>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-[10px] uppercase tracking-wider text-neutral-500 border-b border-neutral-800">
                <th className="text-left font-medium px-4 py-2">Tool</th>
                <th className="text-left font-medium px-3 py-2">Version</th>
                <th className="text-left font-medium px-3 py-2">State</th>
                <th className="text-left font-medium px-3 py-2">Capabilities</th>
                <th className="text-left font-medium px-3 py-2">Last health check</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800/60">
              {health.tools.map((t) => {
                const st = STATE_STYLE[t.state] ?? STATE_STYLE.UNAVAILABLE;
                const Icon = st.Icon;
                return (
                  <tr key={t.id} className="hover:bg-neutral-900/40 align-top">
                    <td className="px-4 py-2.5">
                      <div className="font-semibold text-neutral-200">{t.name}</div>
                      <div className="text-[10px] text-neutral-500">
                        {t.tier}
                        {t.provisionedByApp && <span className="text-emerald-500/70"> · auto-provisioned</span>}
                        {t.installSource && <span> · {t.installSource}</span>}
                      </div>
                    </td>
                    <td className="px-3 py-2.5 font-mono text-[11px] text-neutral-300">
                      {/* No version is shown as absent, not as a guess. */}
                      {t.version ?? <span className="text-neutral-600">—</span>}
                    </td>
                    <td className="px-3 py-2.5">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded border text-[10px] font-bold ${st.cls}`}>
                        <Icon size={11} className={t.state === 'INSTALLING' ? 'animate-spin' : ''} />
                        {t.state}
                      </span>
                      {t.installError && (
                        <div className="text-[10px] text-neutral-500 mt-1 max-w-xs leading-snug">{t.installError}</div>
                      )}
                    </td>
                    <td className="px-3 py-2.5">
                      <div className="flex flex-wrap gap-1 max-w-[16rem]">
                        {t.capabilities.map((cap) => (
                          <span key={cap} className="text-[9px] px-1.5 py-0.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-400">
                            {cap}
                          </span>
                        ))}
                      </div>
                      <div className="text-[9px] text-neutral-600 mt-1">
                        {t.runtimeRequirements.resourceClass}
                        {t.runtimeRequirements.gpu && ' · gpu'}
                        {` · ~${t.runtimeRequirements.ramMB}MB`}
                      </div>
                    </td>
                    <td className="px-3 py-2.5 text-[11px]">
                      {t.lastHealthCheck ? (
                        <>
                          <span className={t.lastHealthCheck.ok ? 'text-emerald-400' : 'text-red-400'}>
                            {t.lastHealthCheck.ok ? 'PASS' : 'FAIL'}
                          </span>
                          <span className="text-neutral-500"> ({t.lastHealthCheck.kind})</span>
                          <div className="text-[10px] text-neutral-600">
                            {ago(t.lastHealthCheck.ranAt)}
                            {typeof t.lastHealthCheck.durationMs === 'number' && ` · ${t.lastHealthCheck.durationMs}ms`}
                          </div>
                          {!t.lastHealthCheck.ok && (
                            <div className="text-[10px] text-neutral-500 mt-0.5 max-w-xs">{t.lastHealthCheck.detail}</div>
                          )}
                        </>
                      ) : (
                        <span className="text-neutral-600">not run</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {!health.environment.canApt && !health.environment.canPip && (
          <div className="px-4 py-2.5 border-t border-neutral-800 text-[11px] text-amber-400 flex items-start gap-2">
            <AlertTriangle size={12} className="mt-px shrink-0" />
            <span>
              PROVISIONING_UNAVAILABLE — environment does not permit dependency installation
              {health.environment.reason && <span className="text-neutral-500"> ({health.environment.reason})</span>}.
              The pipeline continues with the tools that genuinely exist.
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
