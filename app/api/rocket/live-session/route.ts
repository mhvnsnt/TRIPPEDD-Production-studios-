import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'nodejs';

const ALLOWED_COMMANDS = new Set([
  'inspect',
  'measure',
  'run_gate',
  'render',
  'publish',
  'refresh',
  'checkpoint',
]);

function envPath(name: string, fallback: string) {
  return process.env[name]?.replace(/^\/+|\/+$/g, '') || fallback.replace(/^\/+|\/+$/g, '');
}

function sessionUrl() {
  return process.env.ROCKET_LIVE_SESSION_URL?.replace(/\/$/, '') || '';
}

function unauthorized(request: NextRequest) {
  const expected = process.env.ROCKET_LIVE_SESSION_SECRET;
  return Boolean(expected && request.headers.get('x-rocket-live-session-secret') !== expected);
}

async function proxy(url: string, path: string, init?: RequestInit) {
  return fetch(`${url}/${path}`, {
    ...init,
    cache: 'no-store',
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
  });
}

export async function GET(request: NextRequest) {
  const url = sessionUrl();
  if (!url) {
    return NextResponse.json({
      status: 'UNAVAILABLE',
      liveSession: false,
      reason: 'ROCKET_LIVE_SESSION_URL is not configured. No local or simulated session is exposed.',
    }, { status: 503 });
  }
  if (unauthorized(request)) {
    return NextResponse.json({ status: 'BLOCKED', liveSession: false, reason: 'Live session authorization failed.' }, { status: 401 });
  }

  const target = request.nextUrl.searchParams.get('target') || 'state';
  const paths: Record<string, string> = {
    health: envPath('ROCKET_LIVE_SESSION_HEALTH_PATH', 'health'),
    capabilities: envPath('ROCKET_LIVE_SESSION_CAPABILITIES_PATH', 'capabilities'),
    state: envPath('ROCKET_LIVE_SESSION_STATE_PATH', 'state'),
  };
  if (!Object.hasOwn(paths, target)) {
    return NextResponse.json({ status: 'BLOCKED', liveSession: false, reason: 'Unsupported live-session target.' }, { status: 400 });
  }

  try {
    const response = await proxy(url, paths[target]);
    const body = await response.json().catch(() => ({}));
    return NextResponse.json({
      ...body,
      status: response.ok ? (body.status || 'READY') : (body.status || 'UNAVAILABLE'),
      liveSession: response.ok,
      authoritativeState: response.ok && target !== 'health',
      source: 'physical-live-session',
    }, { status: response.ok ? 200 : 502 });
  } catch (error) {
    return NextResponse.json({
      status: 'UNAVAILABLE',
      liveSession: false,
      reason: error instanceof Error ? error.message : 'Live session connection failed.',
    }, { status: 503 });
  }
}

export async function POST(request: NextRequest) {
  const url = sessionUrl();
  if (!url) {
    return NextResponse.json({
      status: 'BLOCKED',
      liveSession: false,
      reason: 'ROCKET_LIVE_SESSION_URL is not configured. No simulated session is permitted.',
    }, { status: 503 });
  }
  if (unauthorized(request)) {
    return NextResponse.json({ status: 'BLOCKED', liveSession: false, reason: 'Live session authorization failed.' }, { status: 401 });
  }

  const payload = await request.json().catch(() => null) as { command?: unknown; args?: unknown } | null;
  if (!payload || typeof payload.command !== 'string' || !ALLOWED_COMMANDS.has(payload.command)) {
    return NextResponse.json({
      status: 'BLOCKED',
      liveSession: false,
      reason: 'Command is missing or not in the Rocket live-session allowlist.',
      allowedCommands: [...ALLOWED_COMMANDS],
    }, { status: 400 });
  }

  try {
    const response = await proxy(url, envPath('ROCKET_LIVE_SESSION_COMMAND_PATH', 'command'), {
      method: 'POST',
      body: JSON.stringify({ command: payload.command, args: payload.args ?? {} }),
    });
    const body = await response.json().catch(() => ({}));
    const authoritative = response.ok && Boolean(body?.operationId || body?.receipt || body?.artifactSha256);
    return NextResponse.json({
      ...body,
      status: authoritative ? (body.status || 'COMPLETED') : (body.status || 'AWAITING_RECEIPT'),
      liveSession: response.ok,
      authoritativeState: authoritative,
      receiptRequired: true,
      source: 'physical-live-session',
    }, { status: response.ok ? 200 : 502 });
  } catch (error) {
    return NextResponse.json({
      status: 'UNAVAILABLE',
      liveSession: false,
      reason: error instanceof Error ? error.message : 'Live session command failed.',
    }, { status: 503 });
  }
}
