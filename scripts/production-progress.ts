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
let totalSources = 0;
let analyzed = 0;
let selected = 0;
let encoded = 0;
let cached = 0;

function printStage(stage: string, done: number, total: number, detail: string) {
  console.log(`[EP01 PROGRESS ${elapsed()}] ${stage.padEnd(18)} ${bar(done, total)} | ${detail}`);
}

function handleOutput(text: string) {
  process.stdout.write(text);
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim()) continue;
    const mediaMatch = line.match(/(\d+) supported media file/);
    if (mediaMatch) {
      totalSources = Number(mediaMatch[1]);
      printStage('SOURCE DISCOVERY', totalSources, totalSources, `media files discovered=${totalSources}`);
    }
    if (/Analyzed /.test(line)) {
      analyzed += 1;
      printStage('SOURCE ANALYSIS', analyzed, Math.max(totalSources, analyzed), `completed=${analyzed}/${totalSources || '?'}`);
    }
    if (/Skipping timed-out\/failed source/.test(line)) {
      analyzed += 1;
      printStage('SOURCE ANALYSIS', analyzed, Math.max(totalSources, analyzed), `failed-but-accounted-for=${analyzed}/${totalSources || '?'}`);
    }
    if (/cache hit:/.test(line)) {
      cached += 1;
      encoded += 1;
      printStage('SEGMENT ENCODING', encoded, Math.max(selected, encoded), `cache reuse=${cached}`);
    }
    if (/encoded and cached:/.test(line)) {
      encoded += 1;
      printStage('SEGMENT ENCODING', encoded, Math.max(selected, encoded), `new segments=${encoded}`);
    }
    if (/Fast analysis batch complete:/.test(line)) {
      const match = line.match(/(\d+)\/(\d+)/);
      if (match) { analyzed = Number(match[1]); totalSources = Number(match[2]); }
      printStage('ANALYSIS COMPLETE', 1, 1, `usable=${match?.[1] ?? '?'} / ${match?.[2] ?? '?'}`);
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
  let stage: string;
  let done: number;
  let total: number;
  if (!manifestSelected) { stage = analyzed || totalSources ? 'SOURCE ANALYSIS' : 'INGEST'; done = analyzed; total = totalSources || 1; }
  else if (completedSegments < totalSegments) { stage = 'SEGMENT ENCODING'; done = completedSegments; total = totalSegments; }
  else if (mp4 > 0) { stage = 'ASSEMBLY COMPLETE'; done = 1; total = 1; }
  else { stage = 'FINAL CONCAT'; done = 0; total = 1; }
  printStage(stage, done, total, `selected=${manifestSelected || '?'} encoded=${completedSegments}/${totalSegments || '?'} cached=${cacheCount} | mp4=${mp4}B otio=${otio}B json=${json}B`);
}, 15000);

const stop = (signal: NodeJS.Signals) => { stopping = true; clearInterval(heartbeat); child.kill(signal); };
process.once('SIGTERM', () => stop('SIGTERM'));
process.once('SIGINT', () => stop('SIGINT'));
child.once('exit', (code, signal) => {
  stopping = true;
  clearInterval(heartbeat);
  console.log(`[EP01 PROGRESS ${elapsed()}] ${code === 0 ? 'COMPLETE' : `FAILED(${code ?? signal ?? 'unknown'})`} ${bar(code === 0 ? 1 : 0, 1)} | production command exited`);
  process.exit(code ?? (signal ? 1 : 0));
});
