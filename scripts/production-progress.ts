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

async function fileSize(file: string) { try { return (await fs.stat(file)).size; } catch { return 0; } }
async function countFiles(dir: string, pattern: RegExp) { try { return (await fs.readdir(dir, { withFileTypes: true })).filter(e => e.isFile() && pattern.test(e.name)).length; } catch { return 0; } }
async function readManifest() { try { return JSON.parse(await fs.readFile(path.join(outputDir, `${basename}.json`), 'utf8')); } catch { return null; } }
function elapsed() { return `${((Date.now() - started) / 60000).toFixed(1)}m`; }
function bar(done: number, total: number, width = 28) {
  if (!total) return `[${'·'.repeat(width)}] 0%`;
  const percent = Math.max(0, Math.min(100, Math.round((done / total) * 100)));
  const filled = Math.round((percent / 100) * width);
  return `[${'█'.repeat(filled)}${'·'.repeat(width - filled)}] ${percent}%`;
}

const target = process.argv[2] || 'scripts/run-public-pilot-fast.ts';
const args = process.argv.slice(3);
const child = spawn(process.execPath, ['node_modules/tsx/dist/cli.mjs', target, ...args], { stdio: ['ignore', 'pipe', 'pipe'], env: process.env });

let stopping = false;
let selected = 0;
let encoded = 0;
let cached = 0;
let analyzed = 0;
let lastStage = '';

function printStage(stage: string, done: number, total: number, detail: string) {
  lastStage = stage;
  console.log(`[EP01 PROGRESS ${elapsed()}] ${stage.padEnd(18)} ${bar(done, total)} | ${detail}`);
}

function handleOutput(text: string) {
  process.stdout.write(text);
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim()) continue;
    if (/Analyzed /.test(line)) {
      analyzed += 1;
      printStage('SOURCE ANALYSIS', analyzed, Math.max(analyzed, 1), `completed source analyses=${analyzed}`);
    }
    if (/available\.$/.test(line) && /supported media file/.test(line)) {
      const match = line.match(/(\d+) supported media/);
      if (match) printStage('SOURCE DISCOVERY', 1, 1, `media files discovered=${match[1]}`);
    }
    if (/cache hit:/.test(line)) {
      cached += 1;
      encoded += 1;
      printStage('SEGMENT ENCODING', encoded, Math.max(selected, encoded), `cache reuse=${cached}`);
    }
    if (/encoded and cached:/.test(line)) {
      encoded += 1;
      printStage('SEGMENT ENCODING', encoded, Math.max(selected, encoded), `new segments encoded=${encoded}`);
    }
    if (/Fast analysis batch complete:/.test(line)) {
      const match = line.match(/(\d+)\/(\d+)/);
      if (match) { analyzed = Number(match[1]); selected = Number(match[2]); }
      printStage('ANALYSIS COMPLETE', 1, 1, `usable sources=${match?.[1] ?? '?'} / ${match?.[2] ?? '?'}`);
    }
  }
}

child.stdout.on('data', data => handleOutput(data.toString()));
child.stderr.on('data', data => process.stderr.write(data));

const heartbeat = setInterval(async () => {
  if (stopping) return;
  const manifest = await readManifest();
  const manifestSelected = Number(manifest?.selectedClipCount || 0);
  if (manifestSelected > 0) selected = manifestSelected;
  const segmentOutput = path.join(outputDir, `${basename}-segments`);
  const sourceSegments = await countFiles(segmentOutput, /^\d{3}\.mp4$/);
  const generatedSegments = await countFiles(segmentOutput, /^\d{3}-generated\.mp4$/);
  const cacheCount = await countFiles(segmentDir, /^[a-f0-9]{32}\.mp4$/);
  const mp4 = await fileSize(path.join(outputDir, `${basename}.mp4`));
  const otio = await fileSize(path.join(outputDir, `${basename}.otio`));
  const json = await fileSize(path.join(outputDir, `${basename}.json`));
  const generated = Number(manifest?.generatedClips?.length || 0);
  const totalSegments = selected + generated;
  const completedSegments = sourceSegments + generatedSegments;
  const stage = !manifestSelected ? (analyzed ? 'SOURCE ANALYSIS' : 'INGEST') : completedSegments < totalSegments ? 'SEGMENT ENCODING' : mp4 > 0 ? 'ASSEMBLY COMPLETE' : 'FINAL CONCAT';
  const done = stage === 'INGEST' ? 0 : stage === 'SOURCE ANALYSIS' ? analyzed : Math.min(completedSegments, totalSegments || completedSegments);
  const total = stage === 'INGEST' ? 1 : stage === 'SOURCE ANALYSIS' ? Math.max(analyzed, 1) : Math.max(totalSegments, 1);
  console.log(`[EP01 PROGRESS ${elapsed()}] ${stage.padEnd(18)} ${bar(done, total)} | selected=${manifestSelected || '?'} encoded=${completedSegments}/${totalSegments || '?'} cached=${cacheCount} | files mp4=${mp4}B otio=${otio}B json=${json}B`);
}, 15000);

const stop = (signal: NodeJS.Signals) => { stopping = true; clearInterval(heartbeat); child.kill(signal); };
process.once('SIGTERM', () => stop('SIGTERM'));
process.once('SIGINT', () => stop('SIGINT'));
child.once('exit', (code, signal) => {
  stopping = true;
  clearInterval(heartbeat);
  const final = code === 0 ? 'COMPLETE' : `FAILED(${code ?? signal ?? 'unknown'})`;
  console.log(`[EP01 PROGRESS ${elapsed()}] ${final.padEnd(18)} ${bar(code === 0 ? 1 : 0, 1)} | production command exited`);
  process.exit(code ?? (signal ? 1 : 0));
});
