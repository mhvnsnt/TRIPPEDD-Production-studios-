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
  status: 'AVAILABLE' | 'UNAVAILABLE' | 'BROKEN' | 'SERVICE_CANDIDATE';
  version?: string;
  error?: string;
};

type Spec = { command: string; args: string[] } | { service: true; note: string };

const config = JSON.parse(await fs.readFile(configPath, 'utf8')) as { required: string[]; optional: string[] };
const checks: Record<string, Spec> = {
  ffmpeg: { command: 'ffmpeg', args: ['-version'] },
  ffprobe: { command: 'ffprobe', args: ['-version'] },
  opencv: { command: 'python3', args: ['-c', 'import cv2; print(cv2.__version__)'] },
  pyscenedetect: { command: 'python3', args: ['-c', 'import scenedetect; print(getattr(scenedetect, "__version__", "installed"))'] },
  whisper: { command: 'python3', args: ['-c', 'import faster_whisper; print("faster-whisper import OK")'] },
  tesseract: { command: 'tesseract', args: ['--version'] },
  otio: { command: 'python3', args: ['-c', 'import opentimelineio as otio; print(otio.__version__)'] },
  blender: { command: 'blender', args: ['--version'] },
  mediainfo: { command: 'mediainfo', args: ['--Version'] },
  exiftool: { command: 'exiftool', args: ['-ver'] },
  bwfmetaedit: { command: 'bwfmetaedit', args: ['--version'] },
  vmaf: { command: 'vmaf', args: ['--version'] },
  kdenlive: { command: 'kdenlive', args: ['--version'] },
  mlt: { command: 'melt', args: ['-version'] },
  olive: { command: 'olive-editor', args: ['--version'] },
  shotcut: { command: 'shotcut', args: ['--version'] },
  audacity: { command: 'audacity', args: ['--version'] },
  ardour: { command: 'ardour', args: ['--version'] },
  rubberband: { command: 'rubberband', args: ['--version'] },
  aubio: { command: 'python3', args: ['-c', 'import aubio; print(aubio.version)'] },
  natron: { command: 'Natron', args: ['--version'] },
  opencolorio: { command: 'ociocheck', args: ['--version'] },
  openassetio: { command: 'python3', args: ['-c', 'import openassetio; print("openassetio import OK")'] },
  usd: { command: 'usdcat', args: ['--help'] },
  materialx: { command: 'python3', args: ['-c', 'import MaterialX; print(MaterialX.__version__)'] },
  openvdb: { command: 'python3', args: ['-c', 'import pyopenvdb; print("openvdb import OK")'] },
  embree: { command: 'python3', args: ['-c', 'import embree; print("embree import OK")'] },
  demucs: { command: 'demucs', args: ['--help'] },
  pyblish: { command: 'python3', args: ['-c', 'import pyblish.api; print("pyblish import OK")'] },
  pytorch: { command: 'python3', args: ['-c', 'import torch; print(torch.__version__)'] },
  onnxruntime: { command: 'python3', args: ['-c', 'import onnxruntime; print(onnxruntime.__version__)'] },
  prometheus: { service: true, note: 'service integration candidate; validate endpoint in deployment environment' },
  grafana: { service: true, note: 'service integration candidate; validate endpoint in deployment environment' },
  opentelemetry: { command: 'python3', args: ['-c', 'import opentelemetry; print("opentelemetry import OK")'] },
  flamenco: { command: 'flamenco', args: ['--version'] },
  opencue: { command: 'cueadmin', args: ['-version'] },
  kitsu: { service: true, note: 'Kitsu server/API candidate; requires a configured service endpoint' },
  zou: { service: true, note: 'Zou service/API candidate; requires a configured service endpoint' }
};

async function check(id: string): Promise<Result> {
  const spec = checks[id];
  if (!spec) return { id, status: 'BROKEN', error: 'No executable or service check defined.' };
  if ('service' in spec) return { id, status: 'SERVICE_CANDIDATE', version: spec.note };
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
  schemaVersion: 2,
  generatedAt: new Date().toISOString(),
  status: requiredFailures.length ? 'BLOCKED' : 'READY',
  requiredFailures: requiredFailures.map(result => result.id),
  tools: results,
  policy: {
    missingOptionalToolsAreNotFailures: true,
    serviceCandidatesAreNotPretendedToBeInstalled: true,
    fakeAvailabilityIsForbidden: true,
    reportIsTechnicalOnly: true
  }
};

await fs.mkdir(path.dirname(reportPath), { recursive: true });
await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
if (requiredFailures.length) process.exitCode = 2;
