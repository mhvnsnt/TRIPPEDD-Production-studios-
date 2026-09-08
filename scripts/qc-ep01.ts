import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';

const root = process.cwd();
const output = path.join(root, 'public', 'production');
const firstManifestPath = path.join(output, 'EP01-first-assembly.json');
const subjectivityPath = path.resolve(process.env.EP01_SUBJECTIVITY_VIDEO || path.join(root, 'production', 'EP01', 'generated', 'blender', 'ep01_subjectivity.mp4'));
const lockPath = path.join(root, 'production', 'EP01', 'EDITORIAL-LOCK.json');
const qcPath = path.join(root, 'production', 'EP01', 'QC-PASS.json');

async function exists(file: string) {
  try { await fs.access(file); return true; } catch { return false; }
}

async function probe(file: string) {
  return await new Promise<{ duration: number; streams: number }>((resolve, reject) => {
    const child = spawn('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-show_entries', 'stream=index', '-of', 'json', file]);
    let out = '';
    let err = '';
    child.stdout.on('data', d => { out += d.toString(); });
    child.stderr.on('data', d => { err += d.toString(); });
    child.on('error', reject);
    child.on('close', code => {
      if (code !== 0) return reject(new Error(err || `ffprobe exited ${code}`));
      const data = JSON.parse(out);
      resolve({ duration: Number(data.format?.duration || 0), streams: Array.isArray(data.streams) ? data.streams.length : 0 });
    });
  });
}

const failures: string[] = [];
let firstPath: string | undefined;
try {
  const manifest = JSON.parse(await fs.readFile(firstManifestPath, 'utf8'));
  firstPath = manifest.outputPath;
} catch { failures.push('First assembly manifest is missing or invalid.'); }

const firstFile = firstPath ? path.join(root, 'public', firstPath.replace(/^\//, '')) : '';
if (!firstFile || !(await exists(firstFile))) failures.push('First assembly video is missing.');
if (!(await exists(subjectivityPath))) failures.push(`Subjectivity MP4 is missing: ${subjectivityPath}`);
if (!(await exists(lockPath))) failures.push('EDITORIAL-LOCK.json is missing.');

let firstProbe: { duration: number; streams: number } | null = null;
let subjectivityProbe: { duration: number; streams: number } | null = null;
if (firstFile && await exists(firstFile)) {
  try { firstProbe = await probe(firstFile); if (firstProbe.duration <= 0 || firstProbe.streams === 0) failures.push('First assembly failed media probe.'); }
  catch (e: any) { failures.push(`First assembly probe failed: ${e.message}`); }
}
if (await exists(subjectivityPath)) {
  try { subjectivityProbe = await probe(subjectivityPath); if (subjectivityProbe.duration <= 0 || subjectivityProbe.streams === 0) failures.push('Subjectivity asset failed media probe.'); }
  catch (e: any) { failures.push(`Subjectivity probe failed: ${e.message}`); }
}

if (failures.length) {
  await fs.writeFile(qcPath, JSON.stringify({ episodeId: 'EP01', status: 'FAILED', failures, checkedAt: new Date().toISOString() }, null, 2));
  console.error(JSON.stringify({ status: 'FAILED', failures }, null, 2));
  process.exitCode = 2;
} else {
  const result = {
    episodeId: 'EP01', status: 'PASS', checkedAt: new Date().toISOString(),
    checks: { firstAssembly: firstProbe, subjectivityAsset: subjectivityProbe, editorialLockPresent: true },
    note: 'Technical/media QC passed. This does not constitute showrunner greenlight.'
  };
  await fs.writeFile(qcPath, JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
}
