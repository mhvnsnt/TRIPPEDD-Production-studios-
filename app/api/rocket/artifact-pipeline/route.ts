import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'nodejs';

type ArtifactRequest = {
  operationId?: unknown;
  repo?: unknown;
  branch?: unknown;
  baseSha?: unknown;
  editor?: unknown;
  operation?: unknown;
  artifactPath?: unknown;
  artifactSha256?: unknown;
  validation?: unknown;
  checkpoint?: unknown;
};

function sessionUrl() {
  return process.env.ROCKET_LIVE_SESSION_URL?.replace(/\/$/, '') || '';
}

function unauthorized(request: NextRequest) {
  const expected = process.env.ROCKET_LIVE_SESSION_SECRET;
  return Boolean(expected && request.headers.get('x-rocket-live-session-secret') !== expected);
}

function missing(value: unknown) {
  return typeof value !== 'string' || value.trim().length === 0;
}

export async function POST(request: NextRequest) {
  const url = sessionUrl();
  if (!url) {
    return NextResponse.json({ status: 'BLOCKED', authoritative: false, reason: 'ROCKET_LIVE_SESSION_URL is not configured. Artifact Pipeline has no worker/session fallback.' }, { status: 503 });
  }
  if (unauthorized(request)) {
    return NextResponse.json({ status: 'BLOCKED', authoritative: false, reason: 'Live session authorization failed.' }, { status: 401 });
  }

  const payload = await request.json().catch(() => null) as ArtifactRequest | null;
  if (!payload || missing(payload.operationId) || missing(payload.editor) || missing(payload.artifactPath) || missing(payload.artifactSha256)) {
    return NextResponse.json({
      status: 'BLOCKED',
      authoritative: false,
      reason: 'Artifact receipt is incomplete. operationId, editor, artifactPath, and artifactSha256 are required before the worker can publish.',
    }, { status: 400 });
  }

  try {
    const response = await fetch(`${url}/command`, {
      method: 'POST',
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        command: 'publish',
        args: {
          operationId: payload.operationId,
          repo: payload.repo,
          branch: payload.branch,
          baseSha: payload.baseSha,
          editor: payload.editor,
          operation: payload.operation,
          artifactPath: payload.artifactPath,
          artifactSha256: payload.artifactSha256,
          validation: payload.validation,
          checkpoint: payload.checkpoint,
          source: 'rocket-artifact-pipeline',
        },
      }),
    });
    const body = await response.json().catch(() => ({}));
    const authoritative = response.ok && Boolean(
      body?.operationId &&
      (body?.receipt || body?.artifactSha256 || body?.commitSha)
    );
    return NextResponse.json({
      ...body,
      status: authoritative ? (body.status || 'COMPLETED') : (body.status || 'AWAITING_RECEIPT'),
      authoritative,
      receiptRequired: true,
      source: 'physical-live-session',
    }, { status: response.ok ? 200 : 502 });
  } catch (error) {
    return NextResponse.json({
      status: 'UNAVAILABLE',
      authoritative: false,
      reason: error instanceof Error ? error.message : 'Artifact worker/session request failed.',
    }, { status: 503 });
  }
}
