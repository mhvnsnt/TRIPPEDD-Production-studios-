import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';

const DEFAULT_FOLDER_URL = 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const MEDIA_EXTENSIONS = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp', '.wav', '.mp3', '.m4a']);

function pythonCommand() { return process.platform === 'win32' ? 'python' : 'python3'; }

type FolderEntry = { url: string; path: string };
export type DriveIngestProgress = {
  phase: 'DISCOVERED' | 'DOWNLOADING' | 'PARTIAL' | 'COMPLETE' | 'FAILED';
  total: number;
  completed: number;
  failed: number;
  current?: string;
  error?: string;
};

async function hasGdown() {
  return new Promise<boolean>((resolve) => {
    const child = spawn(pythonCommand(), ['-m', 'gdown', '--version'], { stdio: 'ignore' });
    child.on('error', () => resolve(false));
    child.on('close', code => resolve(code === 0));
  });
}

async function ensureGdown() {
  if (await hasGdown()) return;
  await new Promise<void>((resolve, reject) => {
    const child = spawn(pythonCommand(), ['-m', 'pip', 'install', '--user', '--upgrade', 'gdown>=6.2.0'], { stdio: 'inherit' });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`Unable to install gdown automatically (exit ${code}).`)));
  });
  if (!(await hasGdown())) throw new Error('gdown installation completed but the executable is not available to Python.');
}

async function runCommand(command: string, args: string[], stdio: 'inherit' | 'pipe' = 'inherit') {
  return new Promise<{ code: number; stdout: string; stderr: string }>((resolve, reject) => {
    const child = spawn(command, args, { stdio: stdio === 'pipe' ? ['ignore', 'pipe', 'pipe'] : 'inherit' });
    let stdout = '';
    let stderr = '';
    if (child.stdout) child.stdout.on('data', data => { stdout += data.toString(); });
    if (child.stderr) child.stderr.on('data', data => { stderr += data.toString(); });
    child.on('error', reject);
    child.on('close', code => resolve({ code: code ?? 1, stdout, stderr }));
  });
}

async function runGdown(args: string[], stdio: 'inherit' | 'pipe' = 'inherit') {
  return runCommand(pythonCommand(), ['-m', 'gdown', ...args], stdio);
}

function cookieArgs() {
  const file = process.env.TRIPPEDD_DRIVE_COOKIES_FILE;
  return file ? ['--cookies', file] : [];
}

async function walkMedia(dir: string) {
  const files: string[] = [];
  async function walk(current: string) {
    for (const entry of await fs.readdir(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) await walk(full);
      else if (MEDIA_EXTENSIONS.has(path.extname(entry.name).toLowerCase()) && (await fs.stat(full)).size > 0) files.push(full);
    }
  }
  await walk(dir);
  return files;
}

function rcloneConfigured() {
  return Boolean(process.env.TRIPPEDD_RCLONE_REMOTE && process.env.TRIPPEDD_RCLONE_PATH);
}

async function tryRcloneRecovery(destination: string, onProgress?: (progress: DriveIngestProgress) => void) {
  if (!rcloneConfigured()) return { total: 0, completed: 0, failed: 0, attempted: false };
  const script = path.join(process.cwd(), 'scripts', 'production', 'rclone-drive-recovery.sh');
  const scriptExists = await fs.stat(script).then(stat => stat.isFile()).catch(() => false);
  if (!scriptExists) return { total: 0, completed: 0, failed: 0, attempted: false };

  onProgress?.({ phase: 'DISCOVERED', total: 0, completed: 0, failed: 0, current: 'rclone authenticated recovery' });
  const child = spawn('bash', [script], {
    env: { ...process.env, TRIPPEDD_RCLONE_DEST: destination },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let stdout = '';
  let stderr = '';
  child.stdout.on('data', data => {
    const text = data.toString();
    stdout += text;
    for (const line of text.split(/\r?\n/)) {
      const discovered = line.match(/^RCLONE_DISCOVERED total=(\d+)/);
      if (discovered) onProgress?.({ phase: 'DISCOVERED', total: Number(discovered[1]), completed: 0, failed: 0, current: 'rclone remote manifest' });
      const progress = line.match(/^RCLONE_PROGRESS total=(\d+) completed=(\d+) failed=(\d+) current=(.*)$/);
      if (progress) onProgress?.({ phase: 'DOWNLOADING', total: Number(progress[1]), completed: Number(progress[2]), failed: Number(progress[3]), current: progress[4] });
      const status = line.match(/^RCLONE_STATUS=(COMPLETE|PARTIAL|EMPTY).*total=(\d+) completed=(\d+) failed=(\d+)/);
      if (status) onProgress?.({ phase: status[1] === 'COMPLETE' ? 'COMPLETE' : status[1] === 'PARTIAL' ? 'PARTIAL' : 'FAILED', total: Number(status[2]), completed: Number(status[3]), failed: Number(status[4]), current: 'rclone recovery' });
    }
  });
  child.stderr.on('data', data => { stderr += data.toString(); });
  const code = await new Promise<number>(resolve => child.on('close', value => resolve(value ?? 1)));
  const discovered = stdout.match(/RCLONE_DISCOVERED total=(\d+)/);
  const last = [...stdout.matchAll(/RCLONE_STATUS=(COMPLETE|PARTIAL|EMPTY).*total=(\d+) completed=(\d+) failed=(\d+)/g)].at(-1);
  return {
    total: Number(last?.[2] ?? discovered?.[1] ?? 0),
    completed: Number(last?.[3] ?? 0),
    failed: Number(last?.[4] ?? 0),
    attempted: true,
    code,
    error: stderr.trim().slice(-1000),
  };
}

function parseGdownFolderManifest(stdout: string): FolderEntry[] {
  // gdown --folder --json can pretty-print the JSON array across multiple
  // lines. Do not parse only the final line: it may be just "]".
  const text = stdout.replace(/^\uFEFF/, '').trim();
  const start = text.indexOf('[');
  const end = text.lastIndexOf(']');
  if (start < 0 || end <= start) throw new Error('gdown returned no JSON array manifest');
  const parsed: unknown = JSON.parse(text.slice(start, end + 1));
  if (!Array.isArray(parsed)) throw new Error('gdown folder manifest is not an array');
  return parsed.filter((entry): entry is FolderEntry => {
    if (!entry || typeof entry !== 'object') return false;
    const value = entry as Record<string, unknown>;
    return typeof value.url === 'string' && typeof value.path === 'string';
  });
}

export async function downloadPublicDriveFolder(
  folderUrl = DEFAULT_FOLDER_URL,
  destination = path.join(process.cwd(), '.trippedd', 'public-drive'),
  onProgress?: (progress: DriveIngestProgress) => void,
) {
  await fs.mkdir(destination, { recursive: true });

  // Prefer an authorized rclone Google Drive remote when configured. This uses
  // the Drive API transport and can avoid the anonymous public-download path.
  // It cannot and does not attempt to defeat a server-side Google quota.
  const rclone = await tryRcloneRecovery(destination, onProgress);
  if (rclone.attempted && rclone.total > 0) {
    const recovered = await walkMedia(destination);
    if (rclone.completed === rclone.total && recovered.length >= rclone.total) {
      onProgress?.({ phase: 'COMPLETE', total: rclone.total, completed: rclone.total, failed: rclone.failed, current: `${rclone.total} usable media file(s) via rclone` });
      return recovered;
    }
    if (recovered.length > 0) {
      onProgress?.({ phase: 'PARTIAL', total: rclone.total, completed: Math.min(recovered.length, rclone.total), failed: rclone.failed, current: `${recovered.length} usable media file(s); gdown fallback continues` });
    }
  }

  await ensureGdown();

  // gdown 6.1+ exposes --folder --json, allowing one opaque all-or-nothing
  // download to become resumable per-file operations. gdown also supports
  // browser cookies for quota-throttled public files.
  const listing = await runGdown([...cookieArgs(), folderUrl, '--folder', '--json'], 'pipe');
  if (listing.code !== 0) {
    const existing = await walkMedia(destination);
    if (existing.length > 0) {
      onProgress?.({ phase: 'PARTIAL', total: Math.max(rclone.total, existing.length), completed: existing.length, failed: rclone.failed + 1, current: 'gdown manifest blocked; preserving recovered media', error: listing.stderr.trim() });
      return existing;
    }
    throw new Error(`Unable to enumerate public Google Drive folder (gdown exit ${listing.code}). ${listing.stderr.trim()}`);
  }

  let entries: FolderEntry[];
  try {
    entries = parseGdownFolderManifest(listing.stdout);
  } catch (error) {
    const existing = await walkMedia(destination);
    if (existing.length > 0) {
      onProgress?.({ phase: 'PARTIAL', total: Math.max(rclone.total, existing.length), completed: existing.length, failed: rclone.failed + 1, current: 'gdown manifest parse failed; preserving recovered media', error: error instanceof Error ? error.message : String(error) });
      return existing;
    }
    throw new Error(`Unable to parse gdown folder manifest: ${error instanceof Error ? error.message : String(error)}`);
  }

  const mediaEntries = entries.filter(entry => MEDIA_EXTENSIONS.has(path.extname(entry.path).toLowerCase()));
  onProgress?.({ phase: 'DISCOVERED', total: mediaEntries.length, completed: 0, failed: 0, current: 'gdown public manifest' });

  let completed = 0;
  let failed = 0;
  const failures: string[] = [];
  for (const entry of mediaEntries) {
    const relative = entry.path.replace(/^[/\\]+/, '');
    const output = path.join(destination, relative);
    await fs.mkdir(path.dirname(output), { recursive: true });
    try {
      const existing = await fs.stat(output).catch(() => null);
      if (existing && existing.size > 0) {
        completed++;
        onProgress?.({ phase: 'DOWNLOADING', total: mediaEntries.length, completed, failed, current: path.basename(output) });
        continue;
      }

      onProgress?.({ phase: 'DOWNLOADING', total: mediaEntries.length, completed, failed, current: path.basename(output) });
      const result = await runGdown([...cookieArgs(), entry.url, '-O', output, '--continue'], 'inherit');
      const stat = await fs.stat(output).catch(() => null);
      if (result.code !== 0 || !stat || stat.size === 0) {
        failed++;
        failures.push(`${relative}: gdown exit ${result.code}`);
        onProgress?.({ phase: 'FAILED', total: mediaEntries.length, completed, failed, current: path.basename(output), error: failures.at(-1) });
        continue;
      }
      completed++;
      onProgress?.({ phase: 'DOWNLOADING', total: mediaEntries.length, completed, failed, current: path.basename(output) });
    } catch (error) {
      failed++;
      const message = `${relative}: ${error instanceof Error ? error.message : String(error)}`;
      failures.push(message);
      onProgress?.({ phase: 'FAILED', total: mediaEntries.length, completed, failed, current: path.basename(output), error: message });
    }
  }

  const files = await walkMedia(destination);
  const expected = mediaEntries.length;
  if (files.length >= expected && expected > 0) {
    onProgress?.({ phase: 'COMPLETE', total: expected, completed: expected, failed, current: `${expected} usable media file(s)` });
    return files;
  }

  onProgress?.({ phase: 'PARTIAL', total: expected, completed: Math.min(files.length, expected), failed, current: `${files.length}/${expected} usable media file(s)` });
  if (!files.length) {
    const detail = failures.slice(0, 3).join(' | ');
    throw new Error(`Public Google Drive produced no usable media files. ${failed}/${expected} downloads failed. ${detail}`.trim());
  }
  return files;
}
