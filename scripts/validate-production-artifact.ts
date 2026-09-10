import 'node:fs/promises';
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';

const root = process.cwd();
const outputDir = path.join(root, 'public', 'production');
const cutNames = [process.env.TRIPPEDD_OUTPUT_BASENAME || 'EP01-STORY-RUNNER'];

type Probe = {
  duration: number;
  size: number;
  video: { codec: string; width: number; height: number; fps: number } | null;
  audio: { codec: string; sampleRate: number; channels: number } | null;
};

function exists(file: string) { return fs.access(file).then(() => true).catch(() => false); }
async function probe(file: string): Promise<Probe> {
  const args = ['-v', 'error', '-show_entries', 'format=duration,size', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels', '-of', 'json', file];
  return await new Promise((resolve, reject) => {
    const child = spawn('ffprobe', args, { cwd: root, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '';
    child.stdout.on('data', data => { stdout += data.toString(); });
    child.stderr.on('data', data => { stderr += data.toString(); });
    child.on('error', reject);
    child.on('close', code => {
      if (code !== 0) return reject(new Error(stderr || `ffprobe exited ${code}`));
      try {
        const data = JSON.parse(stdout);
        const streams = Array.isArray(data.streams) ? data.streams : [];
        const video = streams.find((s: any) => s.codec_type === 'video');
        const audio = streams.find((s: any) => s.codec_type === 'audio');
        const rate = video?.r_frame_rate?.includes('/') ? Number(video.r_frame_rate.split('/')[0]) / Number(video.r_frame_rate.split('/')[1]) : Number(video?.r_frame_rate || 0);
        resolve({
          duration: Number(data.format?.duration || 0),
          size: Number(data.format?.size || 0),
          video: video ? { codec: String(video.codec_name || ''), width: Number(video.width || 0), height: Number(video.height || 0), fps: rate } : null,
          audio: audio ? { codec: String(audio.codec_name || ''), sampleRate: Number(audio.sample_rate || 0), channels: Number(audio.channels || 0) } : null,
        });
      } catch (error) { reject(error); }
    });
  });
}

const failures: string[] = [];
const cuts: Record<string, Probe> = {};
for (const name of cutNames) {
  const file = path.join(outputDir, `${name}.mp4`);
  if (!(await exists(file))) { failures.push(`${name}: MP4 missing.`); continue; }
  try {
    const media = await probe(file);
    cuts[name] = media;
    if (media.duration <= 0) failures.push(`${name}: duration is zero.`);
    if (media.size <= 0) failures.push(`${name}: file size is zero.`);
    if (!media.video) failures.push(`${name}: no video stream.`);
    if (media.video && (media.video.width < 1280 || media.video.height < 720)) failures.push(`${name}: output resolution is below HD.`);
    if (media.video && Math.abs(media.video.fps - 24) > 0.05) failures.push(`${name}: expected 24fps, got ${media.video.fps}.`);
    if (!media.audio) failures.push(`${name}: no audio stream.`);
    if (media.audio && (media.audio.sampleRate < 44100 || media.audio.channels < 1)) failures.push(`${name}: invalid audio stream.`);
    // HARD GATE: prove temporal change by hashing sampled decoded frames.
    if (media.video) {
      const motionProbe = await new Promise<string>((resolve, reject) => {
        const child = spawn('ffmpeg', ['-v','error','-i',file,'-vf','fps=2','-frames:v','16','-f','framemd5','-'], { cwd: root, stdio: ['ignore','pipe','pipe'] });
        let stdout = '', stderr = '';
        child.stdout.on('data', d => { stdout += d.toString(); });
        child.stderr.on('data', d => { stderr += d.toString(); });
        child.on('error', reject);
        child.on('close', code => code === 0 ? resolve(stdout) : reject(new Error(stderr || 'frame hash probe failed')));
      });
      const hashes = motionProbe.split(/\\r?\\n/).filter(line => line && !line.startsWith('#') && line.includes(',')).map(line => line.split(',').pop()!.trim());
      const unique = new Set(hashes).size;
      if (hashes.length < 8 || unique < 4) failures.push(name + ': temporal-motion gate failed (' + unique + ' unique sampled frames).');
    }
    // HARD GATE: audio must contain measurable signal, not merely an attached silent track.
    if (media.audio) {
      const audioProbe = await new Promise<string>((resolve, reject) => {
        const child = spawn('ffmpeg', ['-hide_banner','-i',file,'-af','volumedetect','-f','null','-'], { cwd: root, stdio: ['ignore','pipe','pipe'] });
        let stderr = '';
        child.stderr.on('data', d => { stderr += d.toString(); });
        child.on('error', reject);
        child.on('close', code => code === 0 ? resolve(stderr) : reject(new Error(stderr || 'audio probe failed')));
      });
      if (/mean_volume:\\s*-inf\\s*dB/i.test(audioProbe)) failures.push(name + ': audio track is silent.');
    }
  } catch (error) { failures.push(`${name}: ffprobe failed: ${error instanceof Error ? error.message : String(error)}`); }
}

const report = { schemaVersion: 1, checkedAt: new Date().toISOString(), status: failures.length ? 'FAIL' : 'PASS', cuts, failures };
const reportPath = path.join(outputDir, 'production-artifact-qc.json');
await fs.mkdir(outputDir, { recursive: true });
await fs.writeFile(reportPath, JSON.stringify(report, null, 2), 'utf8');
console.log(JSON.stringify(report, null, 2));
if (failures.length) process.exitCode = 2;
