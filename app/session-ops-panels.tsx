'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';

type Json = Record<string, unknown>;
type Tab = 'health' | 'reconcile' | 'bus';
type HealthSample = { at: number; ok: boolean; latencyMs: number };
type BusEvent = { id: string; at: string; type: string; workspace: string; operationId?: string; authoritative: boolean; detail: string };

const MAX_HISTORY = 40;
function nowId(prefix: string) { return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`; }
function objectFields(value: Json): Array<[string, unknown]> { return Object.entries(value).sort(([a], [b]) => a.localeCompare(b)); }
function display(value: unknown) { return typeof value === 'string' ? value : JSON.stringify(value); }

async function getTarget(target: 'health' | 'state') {
  const response = await fetch(`/api/rocket/live-session?target=${target}`, { cache: 'no-store' });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body?.reason || `${target} HTTP ${response.status}`);
  return body as Json;
}

async function issueCommand(command: string, args: Json) {
  const response = await fetch('/api/rocket/live-session', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ command, args }) });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body?.reason || `${command} HTTP ${response.status}`);
  return body as Json;
}

export function SessionOpsPanels() {
  const [tab, setTab] = useState<Tab>('health');
  const [health, setHealth] = useState<Json>({ status: 'CHECKING' });
  const [samples, setSamples] = useState<HealthSample[]>([]);
  const [consecutiveFailures, setConsecutiveFailures] = useState(0);
  const [alerts, setAlerts] = useState<string[]>([]);
  const [runtimeState, setRuntimeState] = useState<Json | null>(null);
  const [rocketState] = useState<Json>({});
  const [conflicts, setConflicts] = useState<Array<{ key: string; runtime: unknown; rocket: unknown; severity: 'CRITICAL' | 'HIGH' | 'LOW' }>>([]);
  const [bus, setBus] = useState<BusEvent[]>([]);
  const [filter, setFilter] = useState('');
  const [busy, setBusy] = useState(false);
  const [lastReceipt, setLastReceipt] = useState('');

  const addEvent = useCallback((event: Omit<BusEvent, 'id' | 'at'>) => {
    setBus(previous => [{ ...event, id: nowId('evt'), at: new Date().toISOString() }, ...previous].slice(0, 100));
  }, []);

  const pollHealth = useCallback(async () => {
    const started = performance.now();
    try {
      const body = await getTarget('health');
      const latencyMs = Math.round(performance.now() - started);
      setHealth(body);
      setConsecutiveFailures(0);
      setSamples(previous => [...previous, { at: Date.now(), ok: true, latencyMs }].slice(-MAX_HISTORY));
      addEvent({ type: 'HEARTBEAT', workspace: 'Live Door', operationId: typeof body.operationId === 'string' ? body.operationId : undefined, authoritative: true, detail: `health OK · ${latencyMs}ms` });
    } catch (error) {
      const latencyMs = Math.round(performance.now() - started);
      setConsecutiveFailures(previous => previous + 1);
      setSamples(previous => [...previous, { at: Date.now(), ok: false, latencyMs }].slice(-MAX_HISTORY));
      setHealth({ status: 'UNAVAILABLE', reason: error instanceof Error ? error.message : 'Health request failed.' });
      setAlerts(previous => [`${new Date().toLocaleTimeString()} · DISCONNECT · ${error instanceof Error ? error.message : 'health failed'}`, ...previous].slice(0, 20));
      addEvent({ type: 'DISCONNECT', workspace: 'Live Door', authoritative: true, detail: error instanceof Error ? error.message : 'health failed' });
    }
  }, [addEvent]);

  useEffect(() => { void pollHealth(); const timer = window.setInterval(() => void pollHealth(), 5000); return () => window.clearInterval(timer); }, [pollHealth]);

  const reconcile = useCallback(async () => {
    setBusy(true);
    try {
      const body = await getTarget('state');
      const runtime = (body.state && typeof body.state === 'object' ? body.state : body) as Json;
      setRuntimeState(runtime);
      const next: typeof conflicts = [];
      for (const [key, value] of objectFields(runtime)) {
        if (!(key in rocketState)) continue;
        if (JSON.stringify(rocketState[key]) !== JSON.stringify(value)) {
          const severity = /status|live|authoritative|operation|artifact|sha/i.test(key) ? 'CRITICAL' : /state|phase|gate|publish|render/i.test(key) ? 'HIGH' : 'LOW';
          next.push({ key, runtime: value, rocket: rocketState[key], severity });
        }
      }
      setConflicts(next);
      setLastReceipt(typeof body.operationId === 'string' ? body.operationId : 'AWAITING_RECEIPT');
      addEvent({ type: 'RECONCILE', workspace: 'Live Door', operationId: typeof body.operationId === 'string' ? body.operationId : undefined, authoritative: Boolean(body.operationId), detail: `${next.length} measurable runtime/display conflicts` });
    } catch (error) {
      setAlerts(previous => [`${new Date().toLocaleTimeString()} · RECONCILE BLOCKED · ${error instanceof Error ? error.message : 'state failed'}`, ...previous].slice(0, 20));
    } finally { setBusy(false); }
  }, [addEvent, rocketState]);

  const resolveConflict = async (key: string, outcome: 'RUNTIME_WINS' | 'ROCKET_WINS' | 'MANUAL') => {
    setBusy(true);
    try {
      const body = await issueCommand('refresh', { source: 'session-health-reconcile', field: key, outcome, runtimeState: runtimeState?.[key] ?? null, rocketState: rocketState[key] ?? null });
      const operationId = typeof body.operationId === 'string' ? body.operationId : '';
      const receipt = body.receipt && typeof body.receipt === 'object' ? body.receipt : null;
      const runtimeSha = typeof body.runtimeSha256 === 'string' ? body.runtimeSha256 : typeof receipt?.runtimeSha256 === 'string' ? receipt.runtimeSha256 : '';
      if (!operationId || !runtimeSha) throw new Error('Reconcile resolution returned no operationId + runtime SHA receipt. Resolution remains uncommitted.');
      setLastReceipt(`${operationId} · runtime ${runtimeSha}`);
      if (outcome === 'RUNTIME_WINS' && runtimeState) setConflicts(previous => previous.filter(item => item.key !== key));
      else if (outcome === 'MANUAL') setConflicts(previous => previous.filter(item => item.key !== key));
      addEvent({ type: 'RECONCILE_ACK', workspace: 'Live Door', operationId, authoritative: true, detail: `${key} → ${outcome} · runtime SHA ${runtimeSha}` });
    } catch (error) {
      setAlerts(previous => [`${new Date().toLocaleTimeString()} · RESOLUTION BLOCKED · ${error instanceof Error ? error.message : 'resolution failed'}`, ...previous].slice(0, 20));
      addEvent({ type: 'RECONCILE_BLOCKED', workspace: 'Live Door', authoritative: true, detail: error instanceof Error ? error.message : 'resolution failed' });
    } finally { setBusy(false); }
  };

  const visibleBus = useMemo(() => bus.filter(event => !filter || `${event.type} ${event.workspace} ${event.detail}`.toLowerCase().includes(filter.toLowerCase())), [bus, filter]);
  const successes = samples.filter(sample => sample.ok).length;
  const successRate = samples.length ? Math.round(successes / samples.length * 100) : 0;
  const avgLatency = samples.length ? Math.round(samples.reduce((sum, sample) => sum + sample.latencyMs, 0) / samples.length) : 0;

  return <section style={{ position: 'fixed', left: 18, bottom: 18, zIndex: 999, width: 520, maxHeight: '70vh', overflow: 'auto', border: '1px solid rgba(64,0,255,.4)', borderRadius: 12, background: 'rgba(5,8,15,.97)', color: '#e8f7ff', boxShadow: '0 18px 60px rgba(0,0,0,.5)', fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' }}>
    <header style={{ padding: 10, borderBottom: '1px solid rgba(255,255,255,.08)' }}>
      <strong style={{ fontSize: 12, letterSpacing: 1 }}>SESSION OPERATIONS</strong>
      <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>{(['health', 'reconcile', 'bus'] as Tab[]).map(item => <button key={item} onClick={() => setTab(item)} style={{ padding: '6px 9px', borderRadius: 6, border: '1px solid rgba(255,255,255,.12)', background: tab === item ? '#4000FF' : '#0b1020', color: '#fff' }}>{item === 'health' ? '💓 HEALTH' : item === 'reconcile' ? '⟳ RECONCILE' : '⬡ STATE BUS'}</button>)}</div>
    </header>

    {tab === 'health' && <div style={{ padding: 12 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 6 }}>
        {[['STATUS', String(health.status || 'UNKNOWN')], ['SUCCESS', `${successRate}%`], ['AVG', `${avgLatency}ms`], ['FAIL STREAK', String(consecutiveFailures)]].map(([label, value]) => <div key={label} style={{ padding: 8, background: 'rgba(255,255,255,.04)', borderRadius: 6 }}><small>{label}</small><div style={{ marginTop: 4 }}>{value}</div></div>)}
      </div>
      <div style={{ marginTop: 10, fontSize: 10, opacity: .7 }}>REAL /health · 5s polling · {samples.length}/{MAX_HISTORY} samples · synthetic heartbeats prohibited</div>
      <div style={{ marginTop: 10, height: 40, display: 'flex', alignItems: 'end', gap: 2 }}>{samples.map((sample, index) => <span key={index} title={`${sample.latencyMs}ms`} style={{ height: `${Math.max(4, Math.min(40, sample.latencyMs / 4))}px`, flex: 1, background: sample.ok ? '#5eead4' : '#ff5c7a', opacity: .75 }} />)}</div>
      <div style={{ marginTop: 10 }}>{alerts.length ? alerts.map(alert => <div key={alert} style={{ fontSize: 10, padding: 5, color: '#ffb4c0' }}>{alert}</div>) : <span style={{ fontSize: 10, opacity: .6 }}>No disconnect alerts.</span>}</div>
    </div>}

    {tab === 'reconcile' && <div style={{ padding: 12 }}>
      <button onClick={() => void reconcile()} disabled={busy} style={{ width: '100%', padding: 8, borderRadius: 6, border: 0, background: '#4000FF', color: '#fff' }}>{busy ? 'RECONCILING…' : 'RECONCILE FROM RUNTIME /STATE'}</button>
      <div style={{ marginTop: 8, fontSize: 10, opacity: .7 }}>Runtime state is evidence. No display field is treated as authoritative until the runtime returns an operation receipt + runtime SHA.</div>
      {lastReceipt && <div style={{ marginTop: 7, fontSize: 10 }}>RECEIPT · {lastReceipt}</div>}
      <div style={{ marginTop: 10 }}>{conflicts.length === 0 ? <div style={{ padding: 12, opacity: .6, fontSize: 11 }}>No measurable conflicts. Missing comparison fields are UNKNOWN, not PASS.</div> : conflicts.map(conflict => <div key={conflict.key} style={{ padding: 9, marginBottom: 6, border: '1px solid rgba(255,255,255,.1)', borderRadius: 7 }}><strong>{conflict.severity} · {conflict.key}</strong><div style={{ fontSize: 10, marginTop: 5 }}>RUNTIME: {display(conflict.runtime)}</div><div style={{ fontSize: 10 }}>ROCKET: {display(conflict.rocket)}</div><div style={{ display: 'flex', gap: 5, marginTop: 7 }}>{(['RUNTIME_WINS', 'ROCKET_WINS', 'MANUAL'] as const).map(outcome => <button key={outcome} disabled={busy} onClick={() => void resolveConflict(conflict.key, outcome)} style={{ fontSize: 9, padding: 5, background: '#0b1020', color: '#fff', border: '1px solid rgba(255,255,255,.14)', borderRadius: 5 }}>{outcome}</button>)}</div></div>)}</div>
    </div>}

    {tab === 'bus' && <div style={{ padding: 12 }}>
      <input value={filter} onChange={event => setFilter(event.target.value)} placeholder="filter physical events…" style={{ width: '100%', boxSizing: 'border-box', padding: 8, background: '#0b1020', color: '#fff', border: '1px solid rgba(255,255,255,.14)', borderRadius: 6 }} />
      <div style={{ marginTop: 8, fontSize: 10, opacity: .7 }}>PHYSICAL EVENT BUS ONLY. Synthetic activity is intentionally excluded from authority.</div>
      <div style={{ marginTop: 8 }}>{visibleBus.map(event => <div key={event.id} style={{ padding: 7, borderBottom: '1px solid rgba(255,255,255,.06)', fontSize: 10 }}><strong>{event.type}</strong> · {event.workspace} · {event.authoritative ? 'AUTH' : 'NON-AUTH'}<div style={{ opacity: .65, marginTop: 2 }}>{event.detail}{event.operationId ? ` · ${event.operationId}` : ''}</div></div>)}</div>
    </div>}
  </section>;
}
