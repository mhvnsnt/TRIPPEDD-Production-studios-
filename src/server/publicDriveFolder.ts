import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';

const DEFAULT_FOLDER_URL = 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const MEDIA_EXTENSIONS = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp', '.wav', '.mp3', '.m4a']);

function pythonCommand() { return process.platform === 'win32' ? 'python' : 'python3'; }

type FolderEntry = { url: string; path: string };
export type DriveIngestProgress = {
  phase: 'DISCOVERED' | 'DOWNLOADING' | 'COMPLETE' | 'FAILED';
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

async function runGdown(args: string[], stdio: 'inherit' | 'pipe' = 'inherit') {
  return new Promise<{ code: number; stdout: string; stderr: string }>((resolve, reject) => {
    const child = spawn(pythonCommand(), ['-m', 'gdown', ...args], { stdio: stdio === 'pipe' ? ['ignore', 'pipe', 'pipe'] : 'inherit' });
    let stdout = '';
    let stderr = '';
    if (child.stdout) child.stdout.on('data', data => { stdout += data.toString(); });
    if (child.stderr) child.stderr.on('data', data => { stderr += data.toString(); });
    child.on('error', reject);
    child.on('close', code => resolve({ code: code ?? 1, stdout, stderr }));
  });
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

export async function downloadPublicDriveFolder(
  folderUrl = DEFAULT_FOLDER_URL,
  destination = path.join(process.cwd(), '.trippedd', 'public-drive'),
  onProgress?: (progress: DriveIngestProgress) => void,
) {
  await ensureGdown();
  await fs.mkdir(destination, { recursive: true });

  // gdown 6.1+ exposes --folder --json, allowing us to turn one opaque
  // all-or-nothing download into resumable per-file operations. gdown 6.2
  // also supports browser cookies for quota-throttled public files.
  const listing = await runGdown([...cookieArgs(), folderUrl, '--folder', '--json'], 'pipe');
  if (listing.code !== 0) {
    throw new Error(`Unable to enumerate public Google Drive folder (gdown exit ${listing.code}). ${listing.stderr.trim()}`);
  }

  let entries: FolderEntry[];
  try {
    entries = JSON.parse(listing.stdout.trim().split('\n').filter(Boolean).at(-1) || '[]');
  } catch (error) {
    throw new Error(`Unable to parse gdown folder manifest: ${error instanceof Error ? error.message : String(error)}`);
  }

  const mediaEntries = entries.filter(entry => MEDIA_EXTENSIONS.has(path.extname(entry.path).toLowerCase()));
  onProgress?.({ phase: 'DISCOVERED', total: mediaEntries.length, completed: 0, failed: 0 });

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
  onProgress?.({ phase: 'COMPLETE', total: mediaEntries.length, completed: files.length, failed, current: `${files.length} usable media file(s)` });
  if (!files.length) {
    const detail = failures.slice(0, 3).join(' | ');
    throw new Error(`Public Google Drive produced no usable media files. ${failed}/${mediaEntries.length} downloads failed. ${detail}`.trim());
  }
  return files;
}
