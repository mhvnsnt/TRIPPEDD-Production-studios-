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

type Config = { required: string[]; optional: string[]; schemaVersion: number };
const config = JSON.parse(await fs.readFile(configPath, 'utf8')) as Config;

const checks: Record<string, { command: string; args: string[] }> = {
  ffmpeg: { command: 'ffmpeg', args: ['-version'] },
  ffprobe: { command: 'ffprobe', args: ['-version'] },
  opencv: { command: 'python3', args: ['-c', 'import cv2; print(cv2.__version__)'] },
  pyscenedetect: { command: 'python3', args: ['-c', 'import scenedetect; print(getattr(scenedetect, "__version__", "installed"))'] },
  whisper: { command: 'python3', args: ['-c', 'import faster_whisper; print("faster-whisper import OK")'] },
  tesseract: { command: 'tesseract', args: ['--version'] },
  otio: { command: 'python3', args: ['-c', 'import opentimelineio as otio; print(otio.__version__)'] },
  blender: { command: 'blender', args: ['--version'] },
  openimageio: { command: 'oiiotool', args: ['--version'] },
  openexr: { command: 'exrheader', args: ['--help'] },
  imagemagick: { command: 'magick', args: ['-version'] },
  sox: { command: 'sox', args: ['--version'] },
  rubberband: { command: 'rubberband', args: ['--help'] },
  kdenlive: { command: 'kdenlive', args: ['--version'] },
  mlt: { command: 'melt', args: ['-version'] },
  natron: { command: 'Natron', args: ['--version'] },
  opencolorio: { command: 'ociocheck', args: ['--version'] },
  openassetio: { command: 'python3', args: ['-c', 'import openassetio; print("openassetio import OK")'] },
  opencue: { command: 'cueadmin', args: ['-version'] },
  demucs: { command: 'demucs', args: ['--help'] },
  flamenco: { command: 'flamenco-manager', args: ['--version'] },
  gstreamer: { command: 'gst-launch-1.0', args: ['--version'] },
  openusd: { command: 'python3', args: ['-c', 'from pxr import Usd; print(Usd.GetVersion())'] },
  materialx: { command: 'python3', args: ['-c', 'import MaterialX as mx; print(mx.getVersionString())'] },
  osl: { command: 'oslc', args: ['--version'] },
  openvdb: { command: 'python3', args: ['-c', 'import pyopenvdb; print("pyopenvdb import OK")'] },
  openfx: { command: 'pkg-config', args: ['--modversion', 'openfx'] },
  openrv: { command: 'rv', args: ['-version'] },
  xstudio: { command: 'xstudio', args: ['--version'] },
  rez: { command: 'rez', args: ['--version'] },
  'aswf-docker': { command: 'docker', args: ['--version'] }
};

async function check(id: string): Promise<Result> {
  const spec = checks[id];
  if (!spec) return { id, status: 'BROKEN', error: 'No executable/library smoke check defined.' };
  try {
    const { stdout, stderr } = await execFileAsync(spec.command, spec.args, { maxBuffer: 4 * 1024 * 1024 });
    const output = `${stdout || ''}${stderr || ''}`.trim();
    return { id, status: 'AVAILABLE', version: output.split(/\r?\n/)[0].slice(0, 200) };
  } catch (error: any) {
    const code = error?.code;
    return { id, status: code === 'ENOENT' ? 'UNAVAILABLE' : 'BROKEN', error: error?.message || String(error) };
  }
}

const ids = [...new Set([...config.required, ...config.optional])];
const results = await Promise.all(ids.map(check));
const requiredFailures = results.filter(result => config.required.includes(result.id) && result.status !== 'AVAILABLE');
const brokenTools = results.filter(result => result.status === 'BROKEN');
const report = {
  schemaVersion: 3,
  toolchainSchemaVersion: config.schemaVersion,
  generatedAt: new Date().toISOString(),
  status: requiredFailures.length || brokenTools.length ? 'BLOCKED' : 'READY',
  requiredFailures: requiredFailures.map(result => result.id),
  brokenTools: brokenTools.map(result => ({ id: result.id, error: result.error })),
  tools: results,
  policy: {
    missingOptionalToolsAreNotFailures: true,
    fakeAvailabilityIsForbidden: true,
    missingChecksAreBroken: true,
    reportIsTechnicalOnly: true,
    openSourceFirst: true
  }
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
if (requiredFailures.length || brokenTools.length) process.exitCode = 2;
