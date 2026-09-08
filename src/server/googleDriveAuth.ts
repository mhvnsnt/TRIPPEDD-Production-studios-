import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';

const GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth';
const GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token';
const DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive.readonly';
const TOKEN_FILE = process.env.TRIPPEDD_GOOGLE_TOKEN_FILE || path.join(process.cwd(), '.trippedd', 'google-drive-oauth.json');

type StoredTokens = {
  access_token?: string;
  refresh_token?: string;
  expires_at?: number;
  scope?: string;
  token_type?: string;
};

const pendingStates = new Map<string, number>();
let cachedTokens: StoredTokens | null = null;

function clientId() {
  const value = process.env.GOOGLE_CLIENT_ID || process.env.VITE_GOOGLE_CLIENT_ID;
  if (!value) throw new Error('Google OAuth client ID is not configured. Set GOOGLE_CLIENT_ID or VITE_GOOGLE_CLIENT_ID.');
  return value;
}

function clientSecret() {
  const value = process.env.GOOGLE_CLIENT_SECRET;
  if (!value) throw new Error('Google OAuth client secret is not configured. Set GOOGLE_CLIENT_SECRET.');
  return value;
}

function redirectUri() {
  return process.env.GOOGLE_REDIRECT_URI || `${(process.env.APP_URL || 'http://localhost:3000').replace(/\/$/, '')}/api/auth/google/callback`;
}

async function loadTokens(): Promise<StoredTokens | null> {
  if (cachedTokens) return cachedTokens;
  try {
    cachedTokens = JSON.parse(await fs.readFile(TOKEN_FILE, 'utf8')) as StoredTokens;
    return cachedTokens;
  } catch {
    return null;
  }
}

async function saveTokens(tokens: StoredTokens) {
  cachedTokens = tokens;
  await fs.mkdir(path.dirname(TOKEN_FILE), { recursive: true });
  await fs.writeFile(TOKEN_FILE, JSON.stringify(tokens, null, 2), { encoding: 'utf8', mode: 0o600 });
}

export function getGoogleOAuthStatus() {
  return {
    configured: Boolean((process.env.GOOGLE_CLIENT_ID || process.env.VITE_GOOGLE_CLIENT_ID) && process.env.GOOGLE_CLIENT_SECRET),
    authenticated: Boolean(cachedTokens?.refresh_token || cachedTokens?.access_token),
    redirectUri: redirectUri(),
    scope: DRIVE_SCOPE,
  };
}

export function createGoogleAuthorizationUrl() {
  const state = crypto.randomBytes(32).toString('hex');
  pendingStates.set(state, Date.now() + 10 * 60 * 1000);
  const params = new URLSearchParams({
    client_id: clientId(),
    redirect_uri: redirectUri(),
    response_type: 'code',
    access_type: 'offline',
    prompt: 'consent',
    include_granted_scopes: 'true',
    scope: DRIVE_SCOPE,
    state,
  });
  return `${GOOGLE_AUTH_URL}?${params.toString()}`;
}

export async function exchangeGoogleCode(code: string, state: string) {
  const expires = pendingStates.get(state);
  pendingStates.delete(state);
  if (!expires || expires < Date.now()) throw new Error('Google OAuth state is missing or expired.');

  const body = new URLSearchParams({
    code,
    client_id: clientId(),
    client_secret: clientSecret(),
    redirect_uri: redirectUri(),
    grant_type: 'authorization_code',
  });
  const response = await fetch(GOOGLE_TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const payload = await response.json() as any;
  if (!response.ok || !payload.access_token) {
    throw new Error(payload.error_description || payload.error || 'Google OAuth token exchange failed.');
  }

  const previous = await loadTokens();
  await saveTokens({
    access_token: payload.access_token,
    refresh_token: payload.refresh_token || previous?.refresh_token,
    expires_at: Date.now() + Number(payload.expires_in || 3600) * 1000,
    scope: payload.scope,
    token_type: payload.token_type,
  });
}

export async function getGoogleAccessToken(): Promise<string | null> {
  const tokens = await loadTokens();
  if (!tokens) return null;
  if (tokens.access_token && tokens.expires_at && tokens.expires_at > Date.now() + 60_000) return tokens.access_token;
  if (!tokens.refresh_token) return tokens.access_token || null;

  const body = new URLSearchParams({
    client_id: clientId(),
    client_secret: clientSecret(),
    refresh_token: tokens.refresh_token,
    grant_type: 'refresh_token',
  });
  const response = await fetch(GOOGLE_TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const payload = await response.json() as any;
  if (!response.ok || !payload.access_token) {
    cachedTokens = null;
    throw new Error(payload.error_description || payload.error || 'Google access-token refresh failed; reconnect Drive.');
  }
  await saveTokens({
    ...tokens,
    access_token: payload.access_token,
    expires_at: Date.now() + Number(payload.expires_in || 3600) * 1000,
    scope: payload.scope || tokens.scope,
    token_type: payload.token_type || tokens.token_type,
  });
  return payload.access_token;
}

export async function revokeGoogleAccess() {
  const tokens = await loadTokens();
  if (tokens?.refresh_token) {
    await fetch(`https://oauth2.googleapis.com/revoke?token=${encodeURIComponent(tokens.refresh_token)}`, { method: 'POST' });
  }
  cachedTokens = null;
  await fs.rm(TOKEN_FILE, { force: true });
}
