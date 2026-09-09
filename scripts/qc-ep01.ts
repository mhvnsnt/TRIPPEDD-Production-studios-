import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';

const root = process.cwd();
const output = path.join(root, 'public', 'production');
const firstManifestPath = path.join(output, 'EP01-first-assembly.json');
const subjectivityPath = path.resolve(process.env.EP01_SUBJECTIVITY_VIDEO || path.join(root, 'production', 'EP01', 'generated', 'blender', 'ep01_subjectivity.mp4'));
const lockPath = path.join(root, 'production', 'EP01', 'EDITORIAL-LOCK.json');
const qcPath = path.join(root, 'production', 'EP01', 'QC-PASS.json');
const showrunnerPath = path.join(output, process.env.TRIPPEDD_QC_BASENAME ? `${process.env.TRIPPEDD_QC_BASENAME}.mp4` : 'EP01-SHOWRUNNER.mp4');

async function exists(file: string) { try { await fs.access(file); return true; } catch { return false; } }
async function fileSize(file: string) { try { return (await fs.stat(file)).size; } catch { return 0; } }

async function probe(file: string) {
  return await new Promise<{ duration: number; streams: number; video: boolean; audio: boolean }>((resolve, reject) => {
    const child = spawn('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-show_entries', 'stream=index,codec_type', '-of', 'json', file]);
    let out = ''; let err = '';
    child.stdout.on('data', d => { out += d.toString(); }); child.stderr.on('data', d => { err += d.toString(); }); child.on('error', reject);
    child.on('close', code => {
      if (code !== 0) return reject(new Error(err || `ffprobe exited ${code}`));
      const data = JSON.parse(out); const streams = Array.isArray(data.streams) ? data.streams : [];
      resolve({ duration: Number(data.format?.duration || 0), streams: streams.length, video: streams.some((s: any) => s.codec_type === 'video'), audio: streams.some((s: any) => s.codec_type === 'audio') });
    });
  });
}

async function run(command: string, args: string[]) {
  return await new Promise<void>((resolve, reject) => {
    const child = spawn(command, args, { stdio: ['ignore', 'pipe', 'pipe'] }); let stderr = '';
    child.stderr.on('data', d => { stderr += d.toString(); }); child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}: ${stderr.slice(-2000)}`)));
  });
}

const failures: string[] = [];
const checks: Record<string, unknown> = {};
let firstPath: string | undefined;
try { firstPath = JSON.parse(await fs.readFile(firstManifestPath, 'utf8')).outputPath; } catch { failures.push('First assembly manifest is missing or invalid.'); }
const firstFile = firstPath ? path.join(root, 'public', firstPath.replace(/^\//, '')) : '';
if (!firstFile || !(await exists(firstFile))) failures.push('First assembly video is missing.');
if (!(await exists(subjectivityPath))) failures.push(`Subjectivity MP4 is missing: ${subjectivityPath}`);
if (!(await exists(lockPath))) failures.push('EDITORIAL-LOCK.json is missing.');
if (!(await exists(showrunnerPath))) failures.push(`Showrunner output is missing: ${showrunnerPath}`);

let firstProbe: Awaited<ReturnType<typeof probe>> | null = null;
let subjectivityProbe: Awaited<ReturnType<typeof probe>> | null = null;
let showrunnerProbe: Awaited<ReturnType<typeof probe>> | null = null;
if (firstFile && await exists(firstFile)) { try { firstProbe = await probe(firstFile); if (firstProbe.duration <= 0 || !firstProbe.video) failures.push('First assembly failed media probe.'); } catch (e: any) { failures.push(`First assembly probe failed: ${e.message}`); } }
if (await exists(subjectivityPath)) { try { subjectivityProbe = await probe(subjectivityPath); if (subjectivityProbe.duration <= 0 || !subjectivityProbe.video) failures.push('Subjectivity asset failed media probe.'); } catch (e: any) { failures.push(`Subjectivity probe failed: ${e.message}`); } }
if (await exists(showrunnerPath)) { try { showrunnerProbe = await probe(showrunnerPath); if (showrunnerProbe.duration <= 0 || !showrunnerProbe.video) failures.push('Showrunner output failed media probe.'); } catch (e: any) { failures.push(`Showrunner probe failed: ${e.message}`); } }
checks.firstAssembly = firstProbe;
checks.subjectivityAsset = subjectivityProbe;
checks.showrunner = showrunnerProbe;
checks.artifactBytes = { firstAssembly: firstFile ? await fileSize(firstFile) : 0, subjectivity: await fileSize(subjectivityPath), showrunner: await fileSize(showrunnerPath) };

const reference = process.env.EP01_VMAF_REFERENCE;
let vmaf: { attempted: boolean; available: boolean; score?: number; log?: string } = { attempted: false, available: false };
if (reference && await exists(reference) && showrunnerProbe) {
  vmaf.attempted = true;
  const logPath = path.join(output, 'EP01-vmaf.json');
  try {
    await run('ffmpeg', ['-hide_banner', '-nostats', '-i', showrunnerPath, '-i', reference, '-lavfi', `libvmaf=log_fmt=json:log_path=${logPath}`, '-f', 'null', '-']);
    const data = JSON.parse(await fs.readFile(logPath, 'utf8')); const score = Number(data?.pooled_metrics?.vmaf?.mean);
    if (!Number.isFinite(score)) throw new Error('VMAF completed without a numeric mean score.');
    vmaf = { attempted: true, available: true, score, log: logPath };
  } catch (e: any) { failures.push(`VMAF reference QC failed: ${e.message}`); }
}
checks.vmaf = vmaf;

const result = failures.length
  ? { episodeId: 'EP01', status: 'FAILED', failures, checkedAt: new Date().toISOString(), checks }
  : { episodeId: 'EP01', status: 'PASS', checkedAt: new Date().toISOString(), checks, note: 'Technical/media QC passed. This does not constitute showrunner greenlight.' };
await fs.writeFile(qcPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
if (failures.length) process.exitCode = 2;
