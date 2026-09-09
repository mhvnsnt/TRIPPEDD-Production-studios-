import { spawn } from 'child_process';
import fs from 'fs/promises';
import path from 'path';

const started = Date.now();
const root = process.cwd();
const outputDir = path.resolve(process.env.TRIPPEDD_OUTPUT_DIR || path.join(root, 'public', 'production'));
const mediaDir = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(root, '.trippedd', 'media'));
const segmentDir = path.resolve(process.env.TRIPPEDD_SEGMENT_CACHE || path.join(mediaDir, 'assembly-segments'));
const basename = process.env.TRIPPEDD_OUTPUT_BASENAME || 'EP01-SHOWRUNNER';

async function fileSize(file: string) { try { return (await fs.stat(file)).size; } catch { return 0; } }
async function countFiles(dir: string, pattern: RegExp) { try { return (await fs.readdir(dir, { withFileTypes: true })).filter(e => e.isFile() && pattern.test(e.name)).length; } catch { return 0; } }
async function readManifest() { try { return JSON.parse(await fs.readFile(path.join(outputDir, `${basename}.json`), 'utf8')); } catch { return null; } }
function elapsed() { return `${((Date.now() - started) / 60000).toFixed(1)}m`; }
function pct(done: number, total: number) { return total > 0 ? Math.min(99, Math.round((done / total) * 100)) : 0; }

const target = process.argv[2] || 'scripts/run-public-pilot-fast.ts';
const args = process.argv.slice(3);
const child = spawn(process.execPath, ['node_modules/tsx/dist/cli.mjs', target, ...args], { stdio: ['ignore', 'pipe', 'pipe'], env: process.env });
child.stdout.on('data', data => process.stdout.write(data));
child.stderr.on('data', data => process.stderr.write(data));

let stopping = false;
const heartbeat = setInterval(async () => {
  if (stopping) return;
  const manifest = await readManifest();
  const selected = Number(manifest?.selectedClipCount || 0);
  const segmentOutput = path.join(outputDir, `${basename}-segments`);
  const sourceSegments = await countFiles(segmentOutput, /^\d{3}\.mp4$/);
  const generatedSegments = await countFiles(segmentOutput, /^\d{3}-generated\.mp4$/);
  const cachedSegments = await countFiles(segmentDir, /^[a-f0-9]{32}\.mp4$/);
  const mp4 = await fileSize(path.join(outputDir, `${basename}.mp4`));
  const otio = await fileSize(path.join(outputDir, `${basename}.otio`));
  const json = await fileSize(path.join(outputDir, `${basename}.json`));
  const generated = Number(manifest?.generatedClips?.length || 0);
  const total = selected + generated;
  const completed = sourceSegments + generatedSegments;
  const stage = !selected ? 'ANALYSIS' : completed < total ? 'SEGMENT_ENCODING' : mp4 > 0 ? 'COMPLETE_ASSEMBLY' : 'FINAL_CONCAT';
  const progress = !selected ? 0 : completed < total ? pct(completed, total) : mp4 > 0 ? 99 : 95;
  console.log(`[EP01 PROGRESS ${elapsed()}] stage=${stage} | selected=${selected || '?'} | encoded=${completed}/${total || '?'} | cached=${cachedSegments} | assembly=${progress}% | mp4=${mp4}B | otio=${otio}B | json=${json}B`);
}, 15000);

const stop = (signal: NodeJS.Signals) => { stopping = true; clearInterval(heartbeat); child.kill(signal); };
process.once('SIGTERM', () => stop('SIGTERM'));
process.once('SIGINT', () => stop('SIGINT'));
child.once('exit', (code, signal) => {
  stopping = true;
  clearInterval(heartbeat);
  console.log(`[EP01 PROGRESS ${elapsed()}] production command exited code=${code ?? 'null'} signal=${signal ?? 'none'}`);
  process.exit(code ?? (signal ? 1 : 0));
});
