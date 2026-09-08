import fs from 'fs/promises';
import path from 'path';
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);
const root = process.cwd();
const configPath = path.join(root, 'config', 'studio-toolchain.json');
const reportPath = path.join(root, 'public', 'production', 'studio-toolchain-audit.json');

type Result = {
  id: string;
  status: 'AVAILABLE' | 'UNAVAILABLE' | 'BROKEN';
  version?: string;
  error?: string;
};

const config = JSON.parse(await fs.readFile(configPath, 'utf8')) as { required: string[]; optional: string[] };
const checks: Record<string, { command: string; args: string[] }> = {
  ffmpeg: { command: 'ffmpeg', args: ['-version'] },
  ffprobe: { command: 'ffprobe', args: ['-version'] },
  opencv: { command: 'python3', args: ['-c', 'import cv2; print(cv2.__version__)'] },
  // PySceneDetect's CLI has no --version option; import the package instead.
  pyscenedetect: { command: 'python3', args: ['-c', 'import scenedetect; print(getattr(scenedetect, "__version__", "installed"))'] },
  whisper: { command: 'python3', args: ['-c', 'import faster_whisper; print("faster-whisper import OK")'] },
  tesseract: { command: 'tesseract', args: ['--version'] },
  otio: { command: 'python3', args: ['-c', 'import opentimelineio as otio; print(otio.__version__)'] },
  blender: { command: 'blender', args: ['--version'] },
  kdenlive: { command: 'kdenlive', args: ['--version'] },
  mlt: { command: 'melt', args: ['-version'] },
  natron: { command: 'Natron', args: ['--version'] },
  opencolorio: { command: 'ociocheck', args: ['--version'] },
  openassetio: { command: 'python3', args: ['-c', 'import openassetio; print("openassetio import OK")'] },
  opencue: { command: 'cueadmin', args: ['-version'] },
  demucs: { command: 'demucs', args: ['--help'] }
};

async function check(id: string): Promise<Result> {
  const spec = checks[id];
  if (!spec) return { id, status: 'BROKEN', error: 'No executable check defined.' };
  try {
    const { stdout, stderr } = await execFileAsync(spec.command, spec.args, { maxBuffer: 4 * 1024 * 1024 });
    const output = `${stdout || ''}${stderr || ''}`.trim();
    return { id, status: 'AVAILABLE', version: output.split(/\r?\n/)[0].slice(0, 200) };
  } catch (error: any) {
    return { id, status: 'UNAVAILABLE', error: error?.message || String(error) };
  }
}

const ids = [...new Set([...config.required, ...config.optional])];
const results = await Promise.all(ids.map(check));
const requiredFailures = results.filter(result => config.required.includes(result.id) && result.status !== 'AVAILABLE');
const report = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  status: requiredFailures.length ? 'BLOCKED' : 'READY',
  requiredFailures: requiredFailures.map(result => result.id),
  tools: results,
  policy: {
    missingOptionalToolsAreNotFailures: true,
    fakeAvailabilityIsForbidden: true,
    reportIsTechnicalOnly: true
  }
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
if (requiredFailures.length) process.exitCode = 2;
