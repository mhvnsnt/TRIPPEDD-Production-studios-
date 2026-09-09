import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';

const DEFAULT_FOLDER_URL = 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const MEDIA_EXTENSIONS = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp', '.wav', '.mp3', '.m4a']);

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
    const child = spawn(pythonCommand(), ['-m', 'pip', 'install', '--user', '--upgrade', 'gdown>=6.1.0'], { stdio: 'inherit' });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`Unable to install gdown automatically (exit ${code}).`)));
  });
  if (!(await hasGdown())) throw new Error('gdown installation completed but the executable is not available to Python.');
}

export async function downloadPublicDriveFolder(folderUrl = DEFAULT_FOLDER_URL, destination = path.join(process.cwd(), '.trippedd', 'public-drive')) {
  await ensureGdown();
  await fs.mkdir(destination, { recursive: true });

  let gdownExit = 0;
  await new Promise<void>((resolve, reject) => {
    const child = spawn(pythonCommand(), ['-m', 'gdown', folderUrl, '-O', destination, '--folder'], { stdio: 'inherit' });
    child.on('error', reject);
    child.on('close', code => { gdownExit = code ?? 1; resolve(); });
  });

  const files: string[] = [];
  async function walk(dir: string) {
    for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) await walk(full);
      else if (MEDIA_EXTENSIONS.has(path.extname(entry.name).toLowerCase()) && (await fs.stat(full)).size > 0) files.push(full);
    }
  }
  await walk(destination);

  const reportPath = path.join(destination, '.ingest-report.json');
  await fs.writeFile(reportPath, JSON.stringify({
    tool: 'gdown',
    exitCode: gdownExit,
    partialSuccess: gdownExit !== 0 && files.length > 0,
    mediaFilesRecovered: files.length,
    generatedAt: new Date().toISOString(),
    policy: 'individual inaccessible Drive files do not invalidate successfully downloaded source evidence'
  }, null, 2));

  if (!files.length) {
    throw new Error(`Public Google Drive ingest produced no usable media files (gdown exit ${gdownExit}).`);
  }
  if (gdownExit !== 0) {
    console.warn(`Public Google Drive ingest partially succeeded: gdown exit ${gdownExit}; recovered ${files.length} usable media file(s). Continuing with recovered source evidence.`);
  }
  return files;
}
