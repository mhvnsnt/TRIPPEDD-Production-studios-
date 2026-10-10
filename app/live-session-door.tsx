'use client';

import { useEffect, useState } from 'react';

type SessionState = {
  status?: string;
  liveSession?: boolean;
  authoritativeState?: boolean;
  source?: string;
  reason?: string;
  [key: string]: unknown;
};

const commands = ['inspect', 'measure', 'run_gate', 'render', 'publish', 'refresh', 'checkpoint'] as const;

export function LiveSessionDoor() {
  const [state, setState] = useState<SessionState>({ status: 'CHECKING' });
  const [command, setCommand] = useState<(typeof commands)[number]>('inspect');
  const [busy, setBusy] = useState(false);
  const [lastReceipt, setLastReceipt] = useState('');

  const refresh = async () => {
    try {
      const response = await fetch('/api/rocket/live-session?target=state', { cache: 'no-store' });
      const body = await response.json();
      setState(body);
    } catch (error) {
      setState({ status: 'UNAVAILABLE', liveSession: false, reason: error instanceof Error ? error.message : 'Connection failed.' });
    }
  };

  useEffect(() => {
    void refresh();
    const timer = window.setInterval(() => void refresh(), 3000);
    return () => window.clearInterval(timer);
  }, []);

  const run = async () => {
    setBusy(true);
    setLastReceipt('');
    try {
      const response = await fetch('/api/rocket/live-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, args: {} }),
      });
      const body = await response.json();
      setState(body);
      setLastReceipt(body.operationId || body.receipt?.operationId || body.artifactSha256 || 'AWAITING_RECEIPT');
    } catch (error) {
      setState({ status: 'UNAVAILABLE', liveSession: false, reason: error instanceof Error ? error.message : 'Command failed.' });
    } finally {
      setBusy(false);
    }
  };

  const live = state.liveSession && state.authoritativeState;
  return <aside style={{ position: 'fixed', right: 18, bottom: 18, zIndex: 1000, width: 360, border: '1px solid rgba(49,223,255,.35)', borderRadius: 12, background: 'rgba(5,8,15,.96)', color: '#e8f7ff', boxShadow: '0 18px 60px rgba(0,0,0,.45)', fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' }}>
    <div style={{ padding: '10px 12px', borderBottom: '1px solid rgba(255,255,255,.08)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <strong style={{ fontSize: 12, letterSpacing: 1 }}>⬡ LIVE PRODUCTION DOOR</strong>
      <span style={{ fontSize: 10, color: live ? '#5eead4' : '#ffb347' }}>{live ? 'SHARED STATE' : state.status || 'UNKNOWN'}</span>
    </div>
    <div style={{ padding: 12 }}>
      <div style={{ fontSize: 11, lineHeight: 1.45, opacity: .82, marginBottom: 10 }}>
        Rocket reads and drives the same physical runtime used by the production agents. No local/mock state is promoted.
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <select value={command} onChange={e => setCommand(e.target.value as typeof command)} disabled={busy} style={{ flex: 1, background: '#0b1020', color: 'inherit', border: '1px solid rgba(255,255,255,.14)', borderRadius: 6, padding: 7 }}>
          {commands.map(item => <option key={item} value={item}>{item}</option>)}
        </select>
        <button onClick={run} disabled={busy || !live} style={{ background: live ? '#4000FF' : '#202633', color: '#fff', border: 0, borderRadius: 6, padding: '7px 10px', cursor: live ? 'pointer' : 'not-allowed' }}>{busy ? 'RUN…' : 'DRIVE →'}</button>
      </div>
      <div style={{ marginTop: 10, padding: 8, borderRadius: 6, background: 'rgba(255,255,255,.035)', fontSize: 10, minHeight: 32 }}>
        {lastReceipt ? `RECEIPT · ${lastReceipt}` : state.reason || `SOURCE · ${state.source || 'physical-live-session'}`}
      </div>
      <button onClick={() => void refresh()} style={{ marginTop: 8, width: '100%', background: 'transparent', color: '#9bdcff', border: '1px solid rgba(155,220,255,.2)', borderRadius: 6, padding: 6 }}>REFRESH AUTHORITATIVE STATE</button>
    </div>
  </aside>;
}
