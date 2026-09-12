/**
 * Drive credential resolution.
 *
 * The UI obtains a token through @react-oauth/google, which is an interactive
 * browser flow producing a token that expires in about an hour. That is fine
 * while someone is sitting in front of the app, but it cannot support "drop
 * footage in Drive and walk away" — the background watcher goes silent the
 * moment the tab is closed and the token lapses.
 *
 * So credentials resolve in order of durability:
 *   1. Service account key      (indefinite, unattended; folder must be shared
 *                                with the service-account address)
 *   2. OAuth refresh token      (indefinite, unattended, acts as the user)
 *   3. Browser-supplied token   (interactive only, expires)
 *
 * Nothing here ever invents a credential. When none resolves, the caller is
 * told exactly which capability is missing.
 */
import { createSign } from 'crypto';
import { readFile } from 'fs/promises';

export type CredentialSource = 'service_account' | 'refresh_token' | 'browser_token' | 'none';

export interface ResolvedCredential {
  token: string;
  source: CredentialSource;
  expiresAt: number;
}

export interface CredentialStatus {
  source: CredentialSource;
  unattended: boolean;
  detail: string;
  /** Named capability that is missing, when nothing usable resolved. */
  missingCapability?: string;
}

const SCOPE = 'https://www.googleapis.com/auth/drive.readonly';
const TOKEN_URL = 'https://oauth2.googleapis.com/token';
/** Refresh a little early so a long job never starts on a dying token. */
const EXPIRY_MARGIN_MS = 120_000;

function b64url(input: Buffer | string): string {
  return Buffer.from(input).toString('base64')
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

interface ServiceAccountKey {
  client_email: string;
  private_key: string;
  token_uri?: string;
}

async function loadServiceAccount(): Promise<ServiceAccountKey | undefined> {
  const inline = process.env.GOOGLE_SERVICE_ACCOUNT_JSON;
  const file = process.env.GOOGLE_SERVICE_ACCOUNT_FILE;
  let raw: string | undefined;

  if (inline) raw = inline.trim().startsWith('{') ? inline : Buffer.from(inline, 'base64').toString('utf8');
  else if (file) raw = await readFile(file, 'utf8').catch(() => undefined);

  if (!raw) return undefined;
  try {
    const k = JSON.parse(raw);
    if (!k.client_email || !k.private_key) return undefined;
    return k;
  } catch {
    return undefined;
  }
}

/** Signs a JWT assertion and exchanges it for an access token. */
async function mintFromServiceAccount(key: ServiceAccountKey): Promise<ResolvedCredential> {
  const now = Math.floor(Date.now() / 1000);
  const header = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const claim = b64url(JSON.stringify({
    iss: key.client_email,
    scope: SCOPE,
    aud: key.token_uri || TOKEN_URL,
    exp: now + 3600,
    iat: now,
  }));

  const signer = createSign('RSA-SHA256');
  signer.update(`${header}.${claim}`);
  const signature = b64url(signer.sign(key.private_key.replace(/\\n/g, '\n')));
  const assertion = `${header}.${claim}.${signature}`;

  const res = await fetch(key.token_uri || TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion,
    }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok || !body.access_token) {
    throw new Error(`service-account token exchange failed: ${res.status} ${body.error_description || body.error || ''}`.trim());
  }
  return {
    token: body.access_token,
    source: 'service_account',
    expiresAt: Date.now() + (body.expires_in ?? 3600) * 1000,
  };
}

async function mintFromRefreshToken(): Promise<ResolvedCredential> {
  const client_id = process.env.GOOGLE_OAUTH_CLIENT_ID!;
  const client_secret = process.env.GOOGLE_OAUTH_CLIENT_SECRET!;
  const refresh_token = process.env.GOOGLE_OAUTH_REFRESH_TOKEN!;

  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id, client_secret, refresh_token, grant_type: 'refresh_token' }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok || !body.access_token) {
    throw new Error(`refresh-token exchange failed: ${res.status} ${body.error_description || body.error || ''}`.trim());
  }
  return {
    token: body.access_token,
    source: 'refresh_token',
    expiresAt: Date.now() + (body.expires_in ?? 3600) * 1000,
  };
}

function hasRefreshTokenConfig(): boolean {
  return !!(process.env.GOOGLE_OAUTH_CLIENT_ID
    && process.env.GOOGLE_OAUTH_CLIENT_SECRET
    && process.env.GOOGLE_OAUTH_REFRESH_TOKEN);
}

export class DriveCredentials {
  private cached?: ResolvedCredential;
  /** Token handed over by the browser UI; interactive-only, expires. */
  private browserToken?: { token: string; receivedAt: number };

  setBrowserToken(token: string): void {
    this.browserToken = { token, receivedAt: Date.now() };
    // A newly supplied browser token supersedes a cached one from the same source.
    if (this.cached?.source === 'browser_token') this.cached = undefined;
  }

  /** Resolve a usable token, or undefined with a stated reason. */
  async resolve(): Promise<ResolvedCredential | undefined> {
    if (this.cached && this.cached.expiresAt - EXPIRY_MARGIN_MS > Date.now()) return this.cached;

    const sa = await loadServiceAccount();
    if (sa) {
      this.cached = await mintFromServiceAccount(sa);
      return this.cached;
    }

    if (hasRefreshTokenConfig()) {
      this.cached = await mintFromRefreshToken();
      return this.cached;
    }

    if (this.browserToken) {
      // Google access tokens live ~1h. We do not know the true issue time, so
      // treat receipt as the start and let the API be the final authority.
      const assumedExpiry = this.browserToken.receivedAt + 3600_000;
      if (assumedExpiry - EXPIRY_MARGIN_MS > Date.now()) {
        this.cached = { token: this.browserToken.token, source: 'browser_token', expiresAt: assumedExpiry };
        return this.cached;
      }
      this.browserToken = undefined; // lapsed; do not hand back a dead token
    }

    return undefined;
  }

  /** Describes what is available without minting anything. */
  async status(): Promise<CredentialStatus> {
    if (await loadServiceAccount()) {
      return { source: 'service_account', unattended: true, detail: 'service account key configured' };
    }
    if (hasRefreshTokenConfig()) {
      return { source: 'refresh_token', unattended: true, detail: 'OAuth refresh token configured' };
    }
    if (this.browserToken) {
      const remainingMs = this.browserToken.receivedAt + 3600_000 - Date.now();
      if (remainingMs > 0) {
        return {
          source: 'browser_token',
          unattended: false,
          detail: `interactive browser token, ~${Math.round(remainingMs / 60000)}m remaining; unattended ingest stops when it lapses`,
        };
      }
    }
    return {
      source: 'none',
      unattended: false,
      detail: 'no Google Drive credential available',
      missingCapability:
        'Set GOOGLE_SERVICE_ACCOUNT_JSON (or _FILE) for unattended access, or ' +
        'GOOGLE_OAUTH_CLIENT_ID + GOOGLE_OAUTH_CLIENT_SECRET + GOOGLE_OAUTH_REFRESH_TOKEN, ' +
        'or sign in through the app UI for an interactive session token.',
    };
  }

  /** Test seam. */
  __clear(): void {
    this.cached = undefined;
    this.browserToken = undefined;
  }
}

export const driveCredentials = new DriveCredentials();
