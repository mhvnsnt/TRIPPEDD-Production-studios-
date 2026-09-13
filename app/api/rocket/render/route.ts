import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'nodejs';

function workerUrl() {
  return process.env.ROCKET_RENDER_WORKER_URL?.replace(/\/$/, '') || '';
}

export async function GET() {
  const url = workerUrl();
  if (!url) {
    return NextResponse.json({
      status: 'UNAVAILABLE',
      authoritativePixels: false,
      reason: 'ROCKET_RENDER_WORKER_URL is not configured.'
    }, { status: 503 });
  }

  try {
    const response = await fetch(`${url}/health`, { cache: 'no-store' });
    const body = await response.json().catch(() => ({}));
    return NextResponse.json({
      status: response.ok ? 'READY' : 'UNAVAILABLE',
      authoritativePixels: false,
      worker: body
    }, { status: response.ok ? 200 : 503 });
  } catch (error) {
    return NextResponse.json({
      status: 'UNAVAILABLE',
      authoritativePixels: false,
      reason: error instanceof Error ? error.message : 'Render worker health check failed.'
    }, { status: 503 });
  }
}

export async function POST(request: NextRequest) {
  const url = workerUrl();
  if (!url) {
    return NextResponse.json({
      status: 'BLOCKED',
      authoritativePixels: false,
      reason: 'ROCKET_RENDER_WORKER_URL is not configured. No simulated render is permitted.'
    }, { status: 503 });
  }

  const expectedSecret = process.env.ROCKET_RENDER_WORKER_SECRET;
  if (expectedSecret && request.headers.get('x-rocket-render-secret') !== expectedSecret) {
    return NextResponse.json({ status: 'BLOCKED', authoritativePixels: false, reason: 'Render worker authorization failed.' }, { status: 401 });
  }

  const payload = await request.json().catch(() => null);
  if (!payload || typeof payload !== 'object') {
    return NextResponse.json({ status: 'BLOCKED', authoritativePixels: false, reason: 'Invalid render request.' }, { status: 400 });
  }

  try {
    const response = await fetch(`${url}/render`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      cache: 'no-store'
    });
    const body = await response.json().catch(() => ({}));
    const authoritative = response.ok && Boolean(body?.artifactSha256 && (body?.artifactUrl || body?.artifactPath));
    return NextResponse.json({
      ...body,
      status: authoritative ? (body.status || 'COMPLETED') : (body.status || 'AWAITING_PROVENANCE'),
      authoritativePixels: authoritative,
      provenanceRequired: true
    }, { status: response.ok ? 200 : 502 });
  } catch (error) {
    return NextResponse.json({
      status: 'UNAVAILABLE',
      authoritativePixels: false,
      reason: error instanceof Error ? error.message : 'Render worker request failed.'
    }, { status: 503 });
  }
}
