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

async function probeMedia(file: string): Promise<{ duration: number; streams: number }> {
  return await new Promise((resolve, reject) => {
    const child = spawn('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-show_entries', 'stream=index', '-of', 'json', file]);
    let out = '';
    let err = '';
    child.stdout.on('data', data => { out += data.toString(); });
    child.stderr.on('data', data => { err += data.toString(); });
    child.on('error', reject);
    child.on('close', code => {
      if (code !== 0) return reject(new Error(err || `ffprobe exited ${code}`));
      try {
        const data = JSON.parse(out);
        resolve({ duration: Number(data.format?.duration || 0), streams: Array.isArray(data.streams) ? data.streams.length : 0 });
      } catch (error) {
        reject(error);
      }
    });
  });
}

/**
 * Builds the final pilot only when every production gate is explicitly present.
 * The first assembly is never silently promoted to final.
 */
export async function buildEp01FinalMaster(): Promise<EP01MasterManifest> {
  const firstManifest = await readJson<{ outputPath?: string }>(path.join(OUTPUT_ROOT, 'EP01-first-assembly.json'));
  const firstAssemblyFile = firstManifest?.outputPath ? path.join(process.cwd(), 'public', firstManifest.outputPath.replace(/^\//, '')) : '';
  const sourceAssembly = !!firstAssemblyFile && await exists(firstAssemblyFile);
  const subjectivityAsset = await exists(SUBJECTIVITY_PATH);
  const lock = await readJson<{ approved?: boolean; segments?: string[] }>(LOCK_PATH);
  const qcRecord = await readJson<{ status?: string }>(QC_PATH);
  const greenlight = await readJson<{ status?: string }>(GREENLIGHT_PATH);
  const editorialLock = !!lock?.approved;
  const qc = qcRecord?.status === 'PASS';
  const showrunnerGreenlight = greenlight?.status === 'GREENLIT';

  const blockedReasons: string[] = [];
  if (!sourceAssembly) blockedReasons.push('Real first assembly is not available.');
  if (!subjectivityAsset) blockedReasons.push(`Subjectivity render is missing: ${SUBJECTIVITY_PATH}`);
  if (!editorialLock) blockedReasons.push('Editorial lock has not been approved.');
  if (!qc) blockedReasons.push('QC-PASS.json does not record PASS.');
  if (!showrunnerGreenlight) blockedReasons.push('Showrunner greenlight is not GREENLIT.');

  const base: EP01MasterManifest = {
    episodeId: 'EP01', title: 'The Walk', status: blockedReasons.length ? 'BLOCKED' : 'READY_FOR_FINAL_RENDER',
    firstAssemblyPath: firstManifest?.outputPath,
    generatedSubjectivityPath: subjectivityAsset ? SUBJECTIVITY_PATH : undefined,
    gates: { sourceAssembly, subjectivityAsset, editorialLock, qc, showrunnerGreenlight },
    blockedReasons, generatedAt: new Date().toISOString(),
  };
  await fs.mkdir(OUTPUT_ROOT, { recursive: true });

  if (blockedReasons.length) {
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  const rawSegments = lock?.segments ?? [];
  const files = rawSegments.map(file => path.resolve(file));
  if (!files.length) {
    base.status = 'BLOCKED';
    base.blockedReasons.push('Editorial lock contains no media segments.');
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  // The generated subjective sequence must be explicitly present in the locked
  // editorial order. Existence alone is never enough to make it into the master.
  const subjectivityResolved = path.resolve(SUBJECTIVITY_PATH);
  const hasSubjectivity = files.some(file => file === subjectivityResolved);
  if (!hasSubjectivity) {
    base.status = 'BLOCKED';
    base.blockedReasons.push('Editorial lock does not explicitly include the approved subjectivity asset.');
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  for (const file of files) {
    if (!(await exists(file))) {
      base.status = 'BLOCKED';
      base.blockedReasons.push(`Locked media segment is missing: ${file}`);
    }
  }
  if (base.blockedReasons.length) {
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  // Probe every locked segment before encoding so a corrupt asset cannot silently
  // produce a final master that appears complete.
  for (const file of files) {
    const media = await probeMedia(file);
    if (media.duration <= 0 || media.streams === 0) {
      base.status = 'BLOCKED';
      base.blockedReasons.push(`Locked media segment failed ffprobe: ${file}`);
    }
  }
  if (base.blockedReasons.length) {
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  const concatPath = path.join(OUTPUT_ROOT, 'EP01-final.concat.txt');
  await fs.writeFile(concatPath, files.map(file => `file '${file.replace(/'/g, "'\\''")}'`).join('\n') + '\n', 'utf8');
  await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', concatPath, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', FINAL_PATH]);

  const finalMedia = await probeMedia(FINAL_PATH);
  if (finalMedia.duration <= 0 || finalMedia.streams === 0) {
    base.status = 'BLOCKED';
    base.blockedReasons.push('Final master failed post-render media probe.');
    await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
    return base;
  }

  base.status = 'FINAL_MASTER_READY';
  base.finalMasterPath = '/production/EP01-FINAL.mp4';
  base.durationSeconds = finalMedia.duration;
  await fs.writeFile(MANIFEST_PATH, JSON.stringify(base, null, 2), 'utf8');
  return base;
}
