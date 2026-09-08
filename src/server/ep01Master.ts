import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';

export interface EP01MasterManifest {
  episodeId: 'EP01';
  title: 'The Walk';
  status: 'READY_FOR_FINAL_RENDER' | 'FINAL_MASTER_READY' | 'BLOCKED';
  firstAssemblyPath?: string;
  finalMasterPath?: string;
  generatedSubjectivityPath?: string;
  durationSeconds?: number;
  gates: {
    sourceAssembly: boolean;
    subjectivityAsset: boolean;
    editorialLock: boolean;
    qc: boolean;
    showrunnerGreenlight: boolean;
  };
  blockedReasons: string[];
  generatedAt: string;
}

const OUTPUT_ROOT = path.resolve(process.env.TRIPPEDD_OUTPUT_DIR || path.join(process.cwd(), 'public', 'production'));
const FINAL_PATH = path.join(OUTPUT_ROOT, 'EP01-FINAL.mp4');
const MANIFEST_PATH = path.join(OUTPUT_ROOT, 'EP01-final.json');
const LOCK_PATH = path.join(process.cwd(), 'production', 'EP01', 'EDITORIAL-LOCK.json');
const QC_PATH = path.join(process.cwd(), 'production', 'EP01', 'QC-PASS.json');
const GREENLIGHT_PATH = path.join(process.cwd(), 'production', 'EP01', 'SHOWRUNNER-GREENLIGHT.json');
const SUBJECTIVITY_PATH = path.resolve(process.env.EP01_SUBJECTIVITY_VIDEO || path.join(process.cwd(), 'production', 'EP01', 'generated', 'blender', 'ep01_subjectivity.mp4'));

function exists(file: string) {
  return fs.access(file).then(() => true).catch(() => false);
}

async function run(command: string, args: string[]) {
  await new Promise<void>((resolve, reject) => {
    const child = spawn(command, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stderr = '';
    child.stderr.on('data', data => { stderr += data.toString(); });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}: ${stderr.slice(-3000)}`)));
  });
}

async function readJson<T>(file: string): Promise<T | null> {
  try { return JSON.parse(await fs.readFile(file, 'utf8')) as T; } catch { return null; }
}

/**
 * Builds the final pilot only when every production gate is explicitly present.
 * The first assembly is never silently promoted to final.
 */
export async function buildEp01FinalMaster(): Promise<EP01MasterManifest> {
  const firstManifest = await readJson<{ outputPath?: string }>(path.join(OUTPUT_ROOT, 'EP01-first-assembly.json'));
  const sourceAssembly = !!firstManifest?.outputPath && await exists(path.join(process.cwd(), 'public', firstManifest.outputPath.replace(/^\//, '')));
  const subjectivityAsset = await exists(SUBJECTIVITY_PATH);
  const editorialLock = await exists(LOCK_PATH);
  const qc = await exists(QC_PATH);
  const showrunnerGreenlight = await exists(GREENLIGHT_PATH);

  const blockedReasons: string[] = [];
  if (!sourceAssembly) blockedReasons.push('Real first assembly is not available.');
  if (!subjectivityAsset) blockedReasons.push(`Subjectivity render is missing: ${SUBJECTIVITY_PATH}`);
  if (!editorialLock) blockedReasons.push('Editorial lock has not been approved.');
  if (!qc) blockedReasons.push('QC pass has not been recorded.');
  if (!showrunnerGreenlight) blockedReasons.push('Showrunner greenlight has not been recorded.');

  const base: EP01MasterManifest = {
    episodeId: 'EP01', title: 'The Walk', status: blockedReasons.length ? 'BLOCKED' : 'READY_FOR_FINAL_RENDER',
    firstAssemblyPath: firstManifest?.outputPath, gates: { sourceAssembly, subjectivityAsset, editorialLock, qc, showrunnerGreenlight },
    blockedReasons, generatedAt: new Date().toISOString(),
  };
  await fs.mkdir(OUTPUT_ROOT, { recursive: true });

  if (blockedReasons.length) {
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  // The locked editorial sequence is encoded as an explicit concat list. Generated
  // subjectivity is inserted as its own provenance-bearing production asset.
  const lock = await readJson<{ segments: string[] }>(LOCK_PATH);
  const files = (lock?.segments ?? []).map(file => path.resolve(file));
  if (!files.length) {
    base.status = 'BLOCKED';
    base.blockedReasons.push('Editorial lock contains no media segments.');
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  const concatPath = path.join(OUTPUT_ROOT, 'EP01-final.concat.txt');
  await fs.writeFile(concatPath, files.map(file => `file '${file.replace(/'/g, "'\\''")}'`).join('\n') + '\n', 'utf8');
  await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', concatPath, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', FINAL_PATH]);

  base.status = 'FINAL_MASTER_READY';
  base.finalMasterPath = '/production/EP01-FINAL.mp4';
  const probe = await new Promise<string>((resolve, reject) => {
    const child = spawn('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_PATH]);
    let out = ''; child.stdout.on('data', d => { out += d.toString(); }); child.on('error', reject); child.on('close', c => c === 0 ? resolve(out.trim()) : reject(new Error('ffprobe failed')));
  });
  base.durationSeconds = Number(probe) || undefined;
  await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
  return base;
}
