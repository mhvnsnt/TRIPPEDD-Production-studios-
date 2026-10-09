/**
 * Getting the real footage out of Drive and onto disk.
 *
 * Two routes, tried in order:
 *   1. A credential (service account / refresh token / session token) via the
 *      Drive API. Works for private folders.
 *   2. gdown, which needs no credential at all — but only if the folder's
 *      sharing is set to "Anyone with the link".
 *
 * If neither works the ingest STOPS and says exactly why. It never substitutes
 * generated footage: a blue rectangle is not your show.
 */
import path from 'path';
import { mkdir, readdir, stat } from 'fs/promises';
import { existsSync } from 'fs';
import { executeTool } from '../core/tools/execution/executor';
import { driveCredentials } from './driveCredentials';
import { listDriveFiles, type DriveFile } from './driveWatcher';

const VIDEO_EXT = /\.(mp4|mov|m4v|mkv|avi|webm|m2ts|mts)$/i;

export type DriveAccessRoute = 'CREDENTIAL' | 'PUBLIC_LINK' | 'NONE';

export interface DriveIngestReport {
  ok: boolean;
  route: DriveAccessRoute;
  folderId: string;
  /** Every file seen in the folder, video or not. */
  discovered: { id?: string; name: string; mimeType?: string; bytes?: number; localPath?: string }[];
  videoCount: number;
  downloaded: number;
  skippedExisting: number;
  /** Set when nothing could be reached. Names the actual blocker. */
  blocker?: string;
  howToFix?: string;
}

export function folderIdFrom(input: string): string {
  const m = input.match(/folders\/([A-Za-z0-9_-]{10,})/);
  return m ? m[1] : input.trim();
}

/** Route 1: the Drive API with whatever credential is configured. */
async function viaCredential(folderId: string, dest: string): Promise<DriveIngestReport | undefined> {
  const cred = await driveCredentials.resolve();
  if (!cred) return undefined;

  const files = await listDriveFiles(folderId, cred.token);
  const report: DriveIngestReport = {
    ok: true, route: 'CREDENTIAL', folderId,
    discovered: files.map((f) => ({ id: f.id, name: f.name, mimeType: f.mimeType, bytes: Number(f.size) || undefined })),
    videoCount: 0, downloaded: 0, skippedExisting: 0,
  };

  for (const f of files) {
    if (!VIDEO_EXT.test(f.name) && !/^video\//i.test(f.mimeType ?? '')) continue;
    report.videoCount++;
    const out = path.join(dest, safeName(f.name));
    if (existsSync(out)) { report.skippedExisting++; continue; }

    const res = await fetch(`https://www.googleapis.com/drive/v3/files/${f.id}?alt=media`, {
      headers: { Authorization: `Bearer ${cred.token}` },
    });
    if (!res.ok) continue;
    const buf = Buffer.from(await res.arrayBuffer());
    const { writeFile } = await import('fs/promises');
    await writeFile(out, buf);
    report.downloaded++;
    const rec = report.discovered.find((d) => d.id === f.id);
    if (rec) rec.localPath = out;
  }
  return report;
}

/** Route 2: gdown, for a folder shared as "Anyone with the link". */
async function viaPublicLink(folderId: string, dest: string, pythonPath: string): Promise<DriveIngestReport> {
  const before = new Set(existsSync(dest) ? await readdir(dest) : []);

  const run = await executeTool({
    tool: 'gdown', version: 'drive', executablePath: pythonPath,
    args: ['-m', 'gdown', '--folder', `https://drive.google.com/drive/folders/${folderId}`,
           '-O', dest, '--remaining-ok'],
    sourceFileId: 'drive-ingest', timeoutMs: 3_600_000,
  });

  const combined = `${run.stdout}\n${run.stderr}`;
  const after = existsSync(dest) ? await readdir(dest) : [];
  const discovered: DriveIngestReport['discovered'] = [];
  let videoCount = 0, downloaded = 0, skippedExisting = 0;

  for (const name of after) {
    const p = path.join(dest, name);
    let bytes: number | undefined;
    try { bytes = (await stat(p)).size; } catch { /* vanished */ }
    discovered.push({ name, bytes, localPath: p });
    if (VIDEO_EXT.test(name)) {
      videoCount++;
      if (before.has(name)) skippedExisting++; else downloaded++;
    }
  }

  if (!run.provenance.success && !videoCount) {
    // Read the actual reason out of gdown rather than guessing at it.
    const permission = /permission|Anyone with the link|401|403|Cannot retrieve/i.test(combined);
    return {
      ok: false, route: 'NONE', folderId, discovered: [], videoCount: 0, downloaded: 0, skippedExisting: 0,
      blocker: permission
        ? 'REAL SOURCE MEDIA IS NOT ACCESSIBLE — the Drive folder is private and no Google credential is configured'
        : `REAL SOURCE MEDIA IS NOT ACCESSIBLE — ${combined.trim().split('\n').pop()?.slice(0, 200)}`,
      howToFix: permission
        ? 'Either: (a) open the folder in Drive, press Share, set General access to "Anyone with the link" (Viewer) — then press Get my footage again; or (b) set GOOGLE_SERVICE_ACCOUNT_JSON and share the folder with that service account.'
        : 'Check the folder link and that the folder still exists.',
    };
  }

  return { ok: videoCount > 0, route: 'PUBLIC_LINK', folderId, discovered, videoCount, downloaded, skippedExisting,
    blocker: videoCount ? undefined : 'The folder was reachable but contains no video files.' };
}

function safeName(n: string): string {
  return path.basename(n).replace(/[^\w.\- ]+/g, '_').slice(0, 160);
}

/**
 * Pull the real footage down. Credential first, public link second, hard stop
 * third — with the reason stated.
 */
export async function ingestDriveFolder(
  folderInput: string, destDir: string, pythonPath: string
): Promise<DriveIngestReport> {
  const folderId = folderIdFrom(folderInput);
  await mkdir(destDir, { recursive: true });

  try {
    const viaCred = await viaCredential(folderId, destDir);
    if (viaCred) return viaCred;
  } catch (e: any) {
    // Fall through to the public route; the credential path's failure is
    // reported only if that one also fails.
  }

  return viaPublicLink(folderId, destDir, pythonPath);
}
