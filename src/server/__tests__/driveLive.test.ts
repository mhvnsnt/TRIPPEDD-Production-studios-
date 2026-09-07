import { describe, it, expect } from 'vitest';
import { DriveCredentials } from '../driveCredentials';
import { listDriveFiles } from '../driveWatcher';

/**
 * Live Drive integration.
 *
 * These run ONLY when a real credential is configured. When none is, they skip
 * with the exact missing capability printed — they never substitute a synthetic
 * Drive response to go green, because a green test that proves nothing about
 * Drive is worse than a skipped one.
 */
const FOLDER = process.env.TRIPPEDD_DRIVE_FOLDER || '1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';

const hasCreds = !!(
  process.env.GOOGLE_SERVICE_ACCOUNT_JSON ||
  process.env.GOOGLE_SERVICE_ACCOUNT_FILE ||
  (process.env.GOOGLE_OAUTH_CLIENT_ID && process.env.GOOGLE_OAUTH_CLIENT_SECRET && process.env.GOOGLE_OAUTH_REFRESH_TOKEN) ||
  process.env.TRIPPEDD_DRIVE_TOKEN
);

describe('Drive credential resolution', () => {
  it('reports the exact missing capability when nothing is configured', async () => {
    const c = new DriveCredentials();
    const status = await c.status();

    if (hasCreds) {
      expect(status.source).not.toBe('none');
      return;
    }
    expect(status.source).toBe('none');
    expect(status.unattended).toBe(false);
    // The message has to be actionable, not just "unavailable".
    expect(status.missingCapability).toContain('GOOGLE_SERVICE_ACCOUNT_JSON');
    expect(status.missingCapability).toContain('GOOGLE_OAUTH_REFRESH_TOKEN');
  });

  it('a browser token is usable but explicitly not unattended', async () => {
    const c = new DriveCredentials();
    c.setBrowserToken('ya29.fake-for-shape-check');
    const status = await c.status();

    if (status.source === 'browser_token') {
      expect(status.unattended).toBe(false);
      expect(status.detail).toMatch(/interactive|lapses/i);
    } else {
      // A durable credential is configured and correctly takes precedence.
      expect(status.unattended).toBe(true);
    }
  });

  it('an expired browser token is discarded rather than handed back', async () => {
    const c = new DriveCredentials();
    c.setBrowserToken('ya29.stale');
    // Reach past the accessor to age the token beyond its assumed lifetime.
    (c as any).browserToken.receivedAt = Date.now() - 3_700_000;
    (c as any).cached = undefined;
    const resolved = await c.resolve();
    if (!hasCreds) expect(resolved).toBeUndefined();
  });
});

describe.skipIf(!hasCreds)('Drive LIVE — real folder', () => {
  it('lists real files from the configured folder', async () => {
    const c = new DriveCredentials();
    if (process.env.TRIPPEDD_DRIVE_TOKEN) c.setBrowserToken(process.env.TRIPPEDD_DRIVE_TOKEN);
    const cred = await c.resolve();
    expect(cred, 'credential should resolve when configured').toBeTruthy();

    const files = await listDriveFiles(FOLDER, cred!.token);
    // Real filenames and real Drive ids — asserted as present, not as specific
    // values, because the folder contents legitimately change as uploads land.
    for (const f of files) {
      expect(f.id).toBeTruthy();
      expect(f.name).toBeTruthy();
      expect(f.mimeType).toBeTruthy();
    }
    console.log(`[drive-live] ${files.length} file(s) in ${FOLDER}:`);
    for (const f of files) console.log(`  ${f.id}  ${f.mimeType.padEnd(18)} ${f.name}`);
  }, 120_000);
});
