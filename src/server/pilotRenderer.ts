import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';
import { createHash } from 'crypto';
import { productionMemory } from './productionMemory';
import { ProductionProgressLedger } from './productionProgress';
import { attachFfmpegProgress } from './ffmpegProgress';

export type PilotCutMode = 'AUTONOMOUS' | 'SHOWRUNNER';
export interface PilotAssemblyClip { sourceFileId: string; sourcePath: string; start: number; end: number; gagId?: string; score?: number; reason: string; sourceOrder?: number; }
export interface PilotAssemblyGeneratedClip { id: string; path: string; purpose: string; provenance: 'GENERATED'; position: 'BEFORE_FINAL_SOURCE_CLIPS' | 'TERMINAL_TAG'; }
export interface PilotAssemblyManifest { episodeId: 'EP01'; title: 'The Walk'; cutMode: PilotCutMode; status: 'ROUGH_CUT_READY' | 'WAITING_FOR_EVIDENCE'; generatedAt: string; sourceClipCount: number; selectedClipCount: number; clips: PilotAssemblyClip[]; generatedClips: PilotAssemblyGeneratedClip[]; missingBeats: string[]; outputPath?: string; timelinePath?: string; }

const CACHE_ROOT = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media'));
const SEGMENT_CACHE_ROOT = path.resolve(process.env.TRIPPEDD_SEGMENT_CACHE || path.join(CACHE_ROOT, 'assembly-segments'));
const OUTPUT_ROOT = path.resolve(process.env.TRIPPEDD_OUTPUT_DIR || path.join(process.cwd(), 'public', 'production'));
const GENERATED_SUBJECTIVITY = path.resolve(process.cwd(), 'production', 'EP01', 'generated', 'blender', 'ep01_subjectivity.mp4');
const GENERATED_BASTARD_TAG = path.resolve(process.cwd(), 'production', 'EP01', 'generated', 'blender', 'ep01_bastard_tag.mp4');
const CUT_MODE: PilotCutMode = process.env.TRIPPEDD_CUT_MODE === 'AUTONOMOUS' ? 'AUTONOMOUS' : 'SHOWRUNNER';
const OUTPUT_BASENAME = process.env.TRIPPEDD_OUTPUT_BASENAME || (CUT_MODE === 'AUTONOMOUS' ? 'EP01-AUTONOMOUS' : 'EP01-SHOWRUNNER');
const SEGMENT_PROFILE = 'h264-1080p24-crf20-veryfast-aac160k';

function run(command: string, args: string[], onChild?: (child: ReturnType<typeof spawn>) => void): Promise<void> {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    onChild?.(child);
    let stderr = '';
    child.stderr.on('data', data => { stderr += data.toString(); });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}: ${stderr.slice(-2000)}`)));
  });
}

function extractDurationSeconds(args: string[]): number | undefined {
  const tIndex = args.indexOf('-t');
  if (tIndex >= 0) { const value = Number(args[tIndex + 1]); if (Number.isFinite(value) && value > 0) return value; }
  return undefined;
}

async function runWithProgress(command: string, args: string[], options: {
  ledger: ProductionProgressLedger;
  stageId: string;
  completed: number;
  total: number;
  artifactPath?: string;
  message?: string;
  progressBase?: number;
  progressSpan?: number;
}): Promise<void> {
  const { ledger, stageId, completed, total, artifactPath, message, progressBase = completed, progressSpan = 0 } = options;
  const durationSeconds = extractDurationSeconds(args);
  const progressArgs = command === 'ffmpeg' && durationSeconds ? ['-progress', 'pipe:1', '-nostats', ...args] : args;
  await ledger.update(stageId, { status: 'RUNNING', completed: progressBase, total, artifactPath, message });
  let lastFraction = 0;
  const heartbeat = setInterval(() => {
    void ledger.update(stageId, { status: 'RUNNING', completed: progressBase + (lastFraction * progressSpan), total, artifactPath, message }).catch(() => undefined);
  }, 5000);
  try {
    await run(command, progressArgs, child => {
      if (command === 'ffmpeg' && durationSeconds) attachFfmpegProgress(child, durationSeconds, sample => {
        if (sample.fraction === undefined) return;
        lastFraction = Math.max(lastFraction, sample.fraction);
        void ledger.update(stageId, {
          status: 'RUNNING',
          completed: progressBase + (lastFraction * progressSpan),
          total,
          artifactPath,
          message: `${message ?? 'Rendering'} · ${Math.round(lastFraction * 100)}%${sample.speed ? ` · ${sample.speed.toFixed(2)}x` : ''}`
        }).catch(() => undefined);
      });
    });
  } catch (error) {
    await ledger.update(stageId, { status: 'FAILED', completed: progressBase + (lastFraction * progressSpan), total, artifactPath, message: error instanceof Error ? error.message : String(error) });
    throw error;
  } finally {
    clearInterval(heartbeat);
  }
}

function safeCachedPath(filePath: string): boolean { const resolved = path.resolve(filePath); return resolved === CACHE_ROOT || resolved.startsWith(`${CACHE_ROOT}${path.sep}`); }
function segmentCachePath(clip: PilotAssemblyClip): string { const key = createHash('sha256').update(JSON.stringify({ sourceFileId: clip.sourceFileId, sourcePath: clip.sourcePath, start: Number(clip.start.toFixed(3)), end: Number(clip.end.toFixed(3)), profile: SEGMENT_PROFILE })).digest('hex').slice(0, 32); return path.join(SEGMENT_CACHE_ROOT, `${key}.mp4`); }

async function mapConcurrent<T>(items: T[], concurrency: number, worker: (item: T, index: number) => Promise<void>) {
  let cursor = 0; const workers = Array.from({ length: Math.min(concurrency, items.length) }, async () => { while (true) { const index = cursor++; if (index >= items.length) return; await worker(items[index], index); } }); await Promise.all(workers);
}
function interleaveGenerated(clips: PilotAssemblyClip[], generated: PilotAssemblyGeneratedClip[]) { const beforeFinal = generated.filter(item => item.position === 'BEFORE_FINAL_SOURCE_CLIPS'); const terminal = generated.filter(item => item.position === 'TERMINAL_TAG'); const insertAt = Math.max(0, clips.length - 3); return [...clips.slice(0, insertAt), ...beforeFinal, ...clips.slice(insertAt), ...terminal]; }
function writeOtioTimeline(clips: PilotAssemblyClip[], generated: PilotAssemblyGeneratedClip[]) {
  const rate = 24; let timelineFrame = 0;
  const otioClips = interleaveGenerated(clips, generated).map((item, index) => {
    if ('sourceFileId' in item) { const durationFrames = Math.max(1, Math.round((item.end - item.start) * rate)); const clip = item; const result = { OTIO_SCHEMA: 'Clip.2', name: `${OUTPUT_BASENAME}-${String(index + 1).padStart(3, '0')}-${clip.gagId || 'select'}`, source_range: { OTIO_SCHEMA: 'TimeRange.1', start_time: { OTIO_SCHEMA: 'RationalTime.1', value: Math.round(clip.start * rate), rate }, duration: { OTIO_SCHEMA: 'RationalTime.1', value: durationFrames, rate } }, media_reference: { OTIO_SCHEMA: 'ExternalReference.1', target_url: clip.sourcePath, available_range: null, metadata: { trippedd: { sourceFileId: clip.sourceFileId, gagId: clip.gagId, score: clip.score, reason: clip.reason, provenance: 'SOURCE_MEDIA' } } }, metadata: { trippedd: { timelineStartFrame: timelineFrame, physicalTruth: true, sourceOrder: clip.sourceOrder, cutMode: CUT_MODE } } }; timelineFrame += durationFrames; return result; }
    return { OTIO_SCHEMA: 'Clip.2', name: item.id, source_range: null, media_reference: { OTIO_SCHEMA: 'ExternalReference.1', target_url: item.path, available_range: null, metadata: { trippedd: { provenance: item.provenance, purpose: item.purpose } } }, metadata: { trippedd: { timelineStartFrame: timelineFrame, physicalTruth: false, generated: true, purpose: item.purpose, position: item.position, cutMode: CUT_MODE } } } as any;
  });
  return { OTIO_SCHEMA: 'Timeline.1', name: `TRIPPEDD EP01 — The Walk — ${CUT_MODE} Cut`, global_start_time: null, tracks: [{ OTIO_SCHEMA: 'Stack.1', name: 'Video 1', children: [{ OTIO_SCHEMA: 'Track.1', name: 'Picture', kind: 'Video', children: otioClips }] }], metadata: { trippedd: { episodeId: 'EP01', cutMode: CUT_MODE, editorialStatus: 'ROUGH_CUT', physicalSourceChronology: 'AUTHORITATIVE_FOR_WHAT_HAPPENED', generatedMaterialPolicy: 'GENERATED_MATERIAL_IS_EXPLICITLY_NON_PHYSICAL', generatedSequences: generated.map(item => item.id), nextStages: ['EDITORIAL_REVIEW', 'FINAL_EDITORIAL_ASSEMBLY', 'QC', 'SHOWRUNNER_GREENLIGHT'] } } };
}

export async function buildEp01FirstAssembly(options: { maxClips?: number; clipPaddingSeconds?: number } = {}): Promise<PilotAssemblyManifest> {
  const maxClips = Math.max(1, Math.min(options.maxClips ?? 24, 80)); const padding = Math.max(0, Math.min(options.clipPaddingSeconds ?? 1.25, 5)); const memory = await productionMemory.load('trippedd'); const sources = Object.values(memory.sources) as Array<{ fileId?: string; mediaPath?: string; sourceOrder?: number }>; const gags = Object.values(memory.gags) as Array<any>; const sourcePaths = new Map<string, { path: string; sourceOrder: number }>();
  for (const source of sources) if (source.fileId && source.mediaPath && safeCachedPath(source.mediaPath)) sourcePaths.set(source.fileId, { path: source.mediaPath, sourceOrder: Number.isFinite(source.sourceOrder) ? Number(source.sourceOrder) : Number.MAX_SAFE_INTEGER });
  const candidates: PilotAssemblyClip[] = [];
  for (const gag of gags) { const sourceFileId = gag.sourceFileId; const source = sourceFileId ? sourcePaths.get(sourceFileId) : undefined; if (!sourceFileId || !source || gag.reviewState === 'HUMAN_REJECTED') continue; for (const signal of (gag.signals ?? []).filter((item: any) => Number.isFinite(item.startTime) && Number.isFinite(item.endTime))) { const start = Math.max(0, Number(signal.startTime) - padding); const end = Math.max(start + 0.25, Number(signal.endTime) + padding); candidates.push({ sourceFileId, sourcePath: source.path, sourceOrder: source.sourceOrder, start, end, gagId: gag.id, score: Number(gag.score) || 0, reason: `${signal.type}: ${signal.evidence}` }); } }
  candidates.sort((a, b) => (b.score ?? 0) - (a.score ?? 0) || (a.sourceOrder ?? Number.MAX_SAFE_INTEGER) - (b.sourceOrder ?? Number.MAX_SAFE_INTEGER) || a.start - b.start); const selected: PilotAssemblyClip[] = []; for (const candidate of candidates) { const duplicate = selected.some(existing => existing.sourceFileId === candidate.sourceFileId && Math.abs(existing.start - candidate.start) < 0.75 && Math.abs(existing.end - candidate.end) < 0.75); if (!duplicate) selected.push(candidate); if (selected.length >= maxClips) break; } selected.sort((a, b) => (a.sourceOrder ?? Number.MAX_SAFE_INTEGER) - (b.sourceOrder ?? Number.MAX_SAFE_INTEGER) || a.start - b.start || (b.score ?? 0) - (a.score ?? 0));
  const generatedClips: PilotAssemblyGeneratedClip[] = []; if (await fs.access(GENERATED_SUBJECTIVITY).then(() => true).catch(() => false)) generatedClips.push({ id: 'ep01-lost-acid-subjectivity', path: GENERATED_SUBJECTIVITY, purpose: "Audience sees the character's subjective experience before returning to live action; generated material is not physical source evidence.", provenance: 'GENERATED', position: 'BEFORE_FINAL_SOURCE_CLIPS' }); if (await fs.access(GENERATED_BASTARD_TAG).then(() => true).catch(() => false)) generatedClips.push({ id: 'ep01-bastard-tag', path: GENERATED_BASTARD_TAG, purpose: 'Terminal mystery tag introducing Bannon/The Bastard after The Walk. This is generated and not physical source evidence.', provenance: 'GENERATED', position: 'TERMINAL_TAG' });
  const missingBeats = selected.length ? ['STORY_REVIEW', ...(generatedClips.some(item => item.id === 'ep01-lost-acid-subjectivity') ? [] : ['SUBJECTIVITY_GENERATION']), ...(generatedClips.some(item => item.id === 'ep01-bastard-tag') ? [] : ['BASTARD_TAG_GENERATION']), 'FINAL_EDITORIAL_ASSEMBLY', 'QC', 'GREENLIGHT'] : ['MEDIA_ANALYSIS', 'GAG_DISCOVERY', 'SOURCE_SELECTS'];
  const manifest: PilotAssemblyManifest = { episodeId: 'EP01', title: 'The Walk', cutMode: CUT_MODE, status: selected.length ? 'ROUGH_CUT_READY' : 'WAITING_FOR_EVIDENCE', generatedAt: new Date().toISOString(), sourceClipCount: sourcePaths.size, selectedClipCount: selected.length, clips: selected, generatedClips, missingBeats };
  const runId = process.env.TRIPPEDD_RUN_ID || process.env.GITHUB_RUN_ID || `${Date.now()}-${process.pid}`; const ledger = new ProductionProgressLedger({ episodeId: 'EP01', runId, rootDir: path.join(OUTPUT_ROOT, '.progress') });
  await ledger.init([{ id: 'source-discovery', label: 'Source discovery', total: Math.max(1, sourcePaths.size) }, { id: 'timeline-planning', label: 'Timeline planning', total: 1 }, { id: 'source-segments', label: 'Source segment encoding', total: selected.length }, { id: 'generated-segments', label: 'Generated segment encoding', total: generatedClips.length }, { id: 'final-concat', label: 'Final concatenation', total: 1 }, { id: 'assembly-complete', label: 'Assembly complete', total: 1 }]);
  await ledger.update('source-discovery', { status: 'COMPLETE', completed: sourcePaths.size, total: Math.max(1, sourcePaths.size), message: `Discovered ${sourcePaths.size} cached source media files.` });
  await fs.mkdir(OUTPUT_ROOT, { recursive: true }); const otioPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.otio`); const jsonPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.json`); const outputPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.mp4`);
  await ledger.update('timeline-planning', { status: 'RUNNING', completed: 0, total: 1, message: 'Writing OTIO and assembly manifest.' }); await fs.writeFile(otioPath, JSON.stringify(writeOtioTimeline(selected, generatedClips), null, 2), 'utf8'); await ledger.update('timeline-planning', { status: 'COMPLETE', completed: 1, total: 1 }); manifest.timelinePath = `/production/${OUTPUT_BASENAME}.otio`; await fs.writeFile(jsonPath, JSON.stringify(manifest, null, 2), 'utf8'); if (!selected.length) return manifest;
  const listPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.concat.txt`); const segmentDir = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}-segments`); await fs.rm(segmentDir, { recursive: true, force: true }); await fs.mkdir(segmentDir, { recursive: true }); await fs.mkdir(SEGMENT_CACHE_ROOT, { recursive: true });
  const sourceSegmentPaths: string[] = Array(selected.length); const renderConcurrency = Math.max(1, Math.min(Number(process.env.EP01_RENDER_CONCURRENCY || 4), 8));
  await mapConcurrent(selected, renderConcurrency, async (clip, i) => { const cachePath = segmentCachePath(clip); const segmentPath = path.join(segmentDir, `${String(i).padStart(3, '0')}.mp4`); if (await fs.stat(cachePath).then(stat => stat.size > 0).catch(() => false)) { await fs.copyFile(cachePath, segmentPath); console.log(`[pilot-renderer] cache hit: ${path.basename(cachePath)}`); } else { const tempPath = path.join(SEGMENT_CACHE_ROOT, `.${path.basename(cachePath, '.mp4')}.partial-${process.pid}-${i}.mp4`); await fs.rm(tempPath, { force: true }); await runWithProgress('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-ss', clip.start.toFixed(3), '-i', clip.sourcePath, '-t', (clip.end - clip.start).toFixed(3), '-map', '0:v:0', '-map', '0:a?', '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '160k', '-movflags', '+faststart', tempPath], { ledger, stageId: 'source-segments', completed: i, total: selected.length, progressBase: i, progressSpan: 1, artifactPath: tempPath, message: `Encoding source segment ${i + 1}/${selected.length}.` }); await fs.rename(tempPath, cachePath); await fs.copyFile(cachePath, segmentPath); console.log(`[pilot-renderer] encoded and cached: ${path.basename(cachePath)}`); } if (!(await fs.stat(segmentPath).then(stat => stat.size > 0).catch(() => false))) throw new Error(`Missing source segment after render: ${segmentPath}`); sourceSegmentPaths[i] = segmentPath; await ledger.update('source-segments', { status: 'RUNNING', completed: i + 1, total: selected.length, artifactPath: segmentPath, message: `Ready source segment ${i + 1}/${selected.length}.` }); });
  await ledger.update('source-segments', { status: 'COMPLETE', completed: selected.length, total: selected.length });
  const generatedSegmentPaths = new Map<string, string>();
  for (let i = 0; i < generatedClips.length; i++) { const generated = generatedClips[i]; const segmentPath = path.join(segmentDir, `${String(selected.length + i).padStart(3, '0')}-generated.mp4`); await runWithProgress('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-i', generated.path, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-shortest', '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '160k', '-movflags', '+faststart', segmentPath], { ledger, stageId: 'generated-segments', completed: i, total: generatedClips.length, progressBase: i, progressSpan: 1, artifactPath: segmentPath, message: `Encoding generated segment ${i + 1}/${generatedClips.length}.` }); generatedSegmentPaths.set(generated.id, segmentPath); await ledger.update('generated-segments', { status: 'RUNNING', completed: i + 1, total: generatedClips.length, artifactPath: segmentPath, message: `Ready generated segment ${i + 1}/${generatedClips.length}.` }); }
  await ledger.update('generated-segments', { status: 'COMPLETE', completed: generatedClips.length, total: generatedClips.length });
  const beforeFinal = generatedClips.filter(item => item.position === 'BEFORE_FINAL_SOURCE_CLIPS'); const terminal = generatedClips.filter(item => item.position === 'TERMINAL_TAG'); const insertAt = Math.max(0, selected.length - 3); const orderedPaths = [...sourceSegmentPaths.slice(0, insertAt), ...beforeFinal.map(item => generatedSegmentPaths.get(item.id)!).filter(Boolean), ...sourceSegmentPaths.slice(insertAt), ...terminal.map(item => generatedSegmentPaths.get(item.id)!).filter(Boolean)]; const concatText = orderedPaths.map(file => `file '${file.replace(/'/g, "'\\''")}'`).join('\n') + '\n'; await fs.writeFile(listPath, concatText, 'utf8');
  await runWithProgress('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', listPath, '-c', 'copy', '-movflags', '+faststart', outputPath], { ledger, stageId: 'final-concat', completed: 0, total: 1, progressBase: 0, progressSpan: 1, artifactPath: outputPath, message: 'Concatenating the measured assembly segments.' });
  await ledger.update('final-concat', { status: 'COMPLETE', completed: 1, total: 1, artifactPath: outputPath }); await ledger.update('assembly-complete', { status: 'COMPLETE', completed: 1, total: 1, artifactPath: outputPath, message: 'EP01 assembly artifact verified by successful ffmpeg completion.' }); manifest.outputPath = `/production/${OUTPUT_BASENAME}.mp4`; await fs.writeFile(jsonPath, JSON.stringify(manifest, null, 2), 'utf8'); return manifest;
}
