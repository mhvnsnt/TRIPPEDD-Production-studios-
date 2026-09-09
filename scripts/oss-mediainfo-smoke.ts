import fs from 'fs/promises';
import { spawn } from 'child_process';
import path from 'path';

const root = process.cwd();
const fixtureDir = path.join(root, '.tmp', 'mediainfo-smoke');
const fixture = path.join(fixtureDir, 'fixture.mp4');

function run(command: string, args: string[]) {
  return new Promise<{ stdout: string; stderr: string }>((resolve, reject) => {
    const child = spawn(command, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', d => { stdout += d.toString(); });
    child.stderr.on('data', d => { stderr += d.toString(); });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve({ stdout, stderr }) : reject(new Error(`${command} exited ${code}: ${stderr.slice(-2000)}`)));
  });
}

await fs.mkdir(fixtureDir, { recursive: true });
try {
  await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=size=320x180:rate=24:color=black', '-t', '1', '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', fixture]);
  const { stdout } = await run('mediainfo', ['--Output=JSON', fixture]);
  const report = JSON.parse(stdout);
  const tracks = Array.isArray(report?.media?.track) ? report.media.track : [];
  const video = tracks.find((track: any) => track['@type'] === 'Video');
  if (!video || Number(video.Width) !== 320 || Number(video.Height) !== 180) {
    throw new Error('MediaInfo did not report the expected 320x180 video track.');
  }
  const evidence = {
    tool: 'MediaInfo',
    command: 'mediainfo --Output=JSON',
    fixture,
    verified: true,
    video: { width: Number(video.Width), height: Number(video.Height), codec: video.Format ?? null },
    checkedAt: new Date().toISOString()
  };
  const evidencePath = path.join(fixtureDir, 'evidence.json');
  await fs.writeFile(evidencePath, JSON.stringify(evidence, null, 2));
  console.log(JSON.stringify(evidence, null, 2));
} finally {
  await fs.rm(fixtureDir, { recursive: true, force: true });
}
