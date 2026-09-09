import { spawn } from 'child_process';
import fs from 'fs/promises';
import path from 'path';

const started = Date.now();
const root = process.cwd();
const outputDir = path.resolve(process.env.TRIPPEDD_OUTPUT_DIR || path.join(root, 'public', 'production'));
const mediaDir = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(root, '.trippedd', 'media'));
const segmentDir = path.resolve(process.env.TRIPPEDD_SEGMENT_CACHE || path.join(mediaDir, 'assembly-segments'));
const basename = process.env.TRIPPEDD_OUTPUT_BASENAME || 'EP01-SHOWRUNNER';
const maxClips = Number(process.env.EP01_MAX_CLIPS || 24);

async function countFiles(dir: string, pattern: RegExp) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    return entries.filter(e => e.isFile() && pattern.test(e.name)).length;
  } catch { return 0; }
}

async function bytes(file: string) {
  try { return (await fs.stat(file)).size; } catch { return 0; }
}

function elapsed() {
  return `${((Date.now() - started) / 60000).toFixed(1)}m`;
}

let child: ReturnType<typeof spawn>;
const target = process.argv[2] || 'scripts/run-public-pilot-fast.ts';
const args = process.argv.slice(3);
child = spawn(process.execPath, ['node_modules/tsx/dist/cli.mjs', target, ...args], {
  stdio: 'inherit',
  env: process.env,
});

let stopping = false;
const heartbeat = setInterval(async () => {
  if (stopping) return;
  const media = await countFiles(mediaDir, /\.(mp4|mov|m4v|webm|avi|mkv|mpg|mpeg|3gp|wav|mp3|m4a)$/i);
  const segments = await countFiles(segmentDir, /\.mp4$/i);
  const output = await bytes(path.join(outputDir, `${basename}.mp4`));
  const otio = await bytes(path.join(outputDir, `${basename}.otio`));
  const json = await bytes(path.join(outputDir, `${basename}.json`));
  const percent = segments > 0 ? Math.min(99, Math.round((segments / Math.max(1, maxClips)) * 90)) : 0;
  console.log(`[EP01 PROGRESS ${elapsed()}] sources=${media} | encoded_segments=${segments}/${maxClips} | assembly_estimate=${percent}% | mp4=${output}B | otio=${otio}B | json=${json}B`);
}, 30000);

const stop = (signal: NodeJS.Signals) => { stopping = true; clearInterval(heartbeat); child.kill(signal); };
process.once('SIGTERM', () => stop('SIGTERM'));
process.once('SIGINT', () => stop('SIGINT'));

child.once('exit', (code, signal) => {
  stopping = true;
  clearInterval(heartbeat);
  console.log(`[EP01 PROGRESS ${elapsed()}] production command exited code=${code ?? 'null'} signal=${signal ?? 'none'}`);
  process.exit(code ?? (signal ? 1 : 0));
});
