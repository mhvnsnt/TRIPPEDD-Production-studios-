import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';

export const DEFAULT_PUBLIC_DRIVE_FOLDER_URL = 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const MEDIA_EXTENSIONS = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp']);

function pythonCommand() { return process.platform === 'win32' ? 'python' : 'python3'; }

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
    const child = spawn(pythonCommand(), ['-m', 'pip', 'install', '--user', 'gdown>=6.0.0'], { stdio: 'inherit' });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`Unable to install gdown automatically (exit ${code}).`)));
  });
}

async function runGdown(args: string[]) {
  await ensureGdown();
  return new Promise<string>((resolve, reject) => {
    const child = spawn(pythonCommand(), ['-m', 'gdown', ...args], { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = ''; let stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk.toString(); });
    child.stderr.on('data', chunk => { stderr += chunk.toString(); });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve(stdout) : reject(new Error(`gdown failed (exit ${code}): ${stderr.trim() || stdout.trim()}`)));
  });
}

export async function listPublicDriveFolder(folderUrl = DEFAULT_PUBLIC_DRIVE_FOLDER_URL) {
  const raw = await runGdown([folderUrl, '--folder', '--json', '--quiet']);
  const entries = JSON.parse(raw) as Array<{ url: string; path: string }>;
  return entries.filter(entry => MEDIA_EXTENSIONS.has(path.extname(entry.path).toLowerCase())).map((entry, index) => {
    const idMatch = entry.url.match(/[?&]id=([^&]+)/) || entry.url.match(/\/d\/([^/]+)/);
    const id = idMatch?.[1] || `public-${index}-${Buffer.from(entry.path).toString('base64url').slice(0, 16)}`;
    return { id, name: path.basename(entry.path), path: entry.path, url: entry.url, mimeType: mimeFor(entry.path) };
  });
}

export async function downloadPublicDriveFile(url: string, destination: string) {
  await ensureGdown();
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await new Promise<void>((resolve, reject) => {
    const child = spawn(pythonCommand(), ['-m', 'gdown', url, '-O', destination, '--continue'], { stdio: 'inherit' });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`gdown file download failed (exit ${code}).`)));
  });
}

export async function downloadPublicDriveFolder(folderUrl = DEFAULT_PUBLIC_DRIVE_FOLDER_URL, destination = path.join(process.cwd(), '.trippedd', 'public-drive')) {
  await ensureGdown();
  await fs.mkdir(destination, { recursive: true });
  await new Promise<void>((resolve, reject) => {
    const child = spawn(pythonCommand(), ['-m', 'gdown', folderUrl, '-O', destination, '--folder', '--remaining-ok'], { stdio: 'inherit' });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`Public Google Drive download failed (gdown exit ${code}).`)));
  });
  const files: string[] = [];
  async function walk(dir: string) { for (const entry of await fs.readdir(dir, { withFileTypes: true })) { const full = path.join(dir, entry.name); if (entry.isDirectory()) await walk(full); else if (MEDIA_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) files.push(full); } }
  await walk(destination); return files;
}

function mimeFor(name: string) {
  const ext = path.extname(name).toLowerCase();
  return ({ '.mp4': 'video/mp4', '.mov': 'video/quicktime', '.m4v': 'video/x-m4v', '.webm': 'video/webm', '.avi': 'video/x-msvideo', '.mkv': 'video/x-matroska', '.mpg': 'video/mpeg', '.mpeg': 'video/mpeg', '.3gp': 'video/3gpp' } as Record<string, string>)[ext] || 'application/octet-stream';
}
