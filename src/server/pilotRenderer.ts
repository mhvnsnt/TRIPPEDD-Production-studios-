import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';
import { productionMemory } from './productionMemory';

export type PilotCutMode = 'AUTONOMOUS' | 'SHOWRUNNER';
export interface PilotAssemblyClip { sourceFileId: string; sourcePath: string; start: number; end: number; gagId?: string; score?: number; reason: string; sourceOrder?: number; }
export interface PilotAssemblyGeneratedClip { id: string; path: string; purpose: string; provenance: 'GENERATED'; position: 'POST_SOURCE_DISCOVERY'; }
export interface PilotAssemblyManifest { episodeId: 'EP01'; title: 'The Walk'; cutMode: PilotCutMode; status: 'ROUGH_CUT_READY' | 'WAITING_FOR_EVIDENCE'; generatedAt: string; sourceClipCount: number; selectedClipCount: number; clips: PilotAssemblyClip[]; generatedClips: PilotAssemblyGeneratedClip[]; missingBeats: string[]; outputPath?: string; timelinePath?: string; }

const CACHE_ROOT = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media'));
const OUTPUT_ROOT = path.resolve(process.env.TRIPPEDD_OUTPUT_DIR || path.join(process.cwd(), 'public', 'production'));
const GENERATED_SUBJECTIVITY = path.resolve(process.cwd(), 'production', 'EP01', 'generated', 'blender', 'ep01_subjectivity.mp4');
const CUT_MODE: PilotCutMode = process.env.TRIPPEDD_CUT_MODE === 'AUTONOMOUS' ? 'AUTONOMOUS' : 'SHOWRUNNER';
const OUTPUT_BASENAME = process.env.TRIPPEDD_OUTPUT_BASENAME || (CUT_MODE === 'AUTONOMOUS' ? 'EP01-AUTONOMOUS' : 'EP01-SHOWRUNNER');

function run(command: string, args: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stderr = '';
    child.stderr.on('data', data => { stderr += data.toString(); });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}: ${stderr.slice(-2000)}`)));
  });
}

function safeCachedPath(filePath: string): boolean {
  const resolved = path.resolve(filePath);
  return resolved === CACHE_ROOT || resolved.startsWith(`${CACHE_ROOT}${path.sep}`);
}

async function mapConcurrent<T>(items: T[], concurrency: number, worker: (item: T, index: number) => Promise<void>) {
  let cursor = 0;
  const workers = Array.from({ length: Math.min(concurrency, items.length) }, async () => {
    while (true) {
      const index = cursor++;
      if (index >= items.length) return;
      await worker(items[index], index);
    }
  });
  await Promise.all(workers);
}

function writeOtioTimeline(clips: PilotAssemblyClip[], generated: PilotAssemblyGeneratedClip[]) {
  const rate = 24;
  let timelineFrame = 0;
  const otioClips = clips.map((clip, index) => {
    const durationFrames = Math.max(1, Math.round((clip.end - clip.start) * rate));
    const item = {
      OTIO_SCHEMA: 'Clip.2', name: `${OUTPUT_BASENAME}-${String(index + 1).padStart(3, '0')}-${clip.gagId || 'select'}`,
      source_range: { OTIO_SCHEMA: 'TimeRange.1', start_time: { OTIO_SCHEMA: 'RationalTime.1', value: Math.round(clip.start * rate), rate }, duration: { OTIO_SCHEMA: 'RationalTime.1', value: durationFrames, rate } },
      media_reference: { OTIO_SCHEMA: 'ExternalReference.1', target_url: clip.sourcePath, available_range: null, metadata: { trippedd: { sourceFileId: clip.sourceFileId, gagId: clip.gagId, score: clip.score, reason: clip.reason, provenance: 'SOURCE_MEDIA' } } },
      metadata: { trippedd: { timelineStartFrame: timelineFrame, physicalTruth: true, sourceOrder: clip.sourceOrder, cutMode: CUT_MODE } }
    };
    timelineFrame += durationFrames;
    return item;
  });
  for (const item of generated) {
    otioClips.push({ OTIO_SCHEMA: 'Clip.2', name: item.id, source_range: null, media_reference: { OTIO_SCHEMA: 'ExternalReference.1', target_url: item.path, available_range: null, metadata: { trippedd: { provenance: item.provenance, purpose: item.purpose } } }, metadata: { trippedd: { timelineStartFrame: timelineFrame, physicalTruth: false, generated: true, purpose: item.purpose, cutMode: CUT_MODE } } } as any);
  }
  return { OTIO_SCHEMA: 'Timeline.1', name: `TRIPPEDD EP01 — The Walk — ${CUT_MODE} Cut`, global_start_time: null, tracks: [{ OTIO_SCHEMA: 'Stack.1', name: 'Video 1', children: [{ OTIO_SCHEMA: 'Track.1', name: 'Picture', kind: 'Video', children: otioClips }] }], metadata: { trippedd: { episodeId: 'EP01', cutMode: CUT_MODE, editorialStatus: 'ROUGH_CUT', physicalSourceChronology: 'AUTHORITATIVE_FOR_WHAT_HAPPENED', generatedMaterialPolicy: 'GENERATED_MATERIAL_IS_EXPLICITLY_NON_PHYSICAL', generatedSequences: generated.map(item => item.id), nextStages: ['EDITORIAL_REVIEW', 'FINAL_EDITORIAL_ASSEMBLY', 'QC', 'SHOWRUNNER_GREENLIGHT'] } } };
}

export async function buildEp01FirstAssembly(options: { maxClips?: number; clipPaddingSeconds?: number } = {}): Promise<PilotAssemblyManifest> {
  const maxClips = Math.max(1, Math.min(options.maxClips ?? 24, 80));
  const padding = Math.max(0, Math.min(options.clipPaddingSeconds ?? 1.25, 5));
  const memory = await productionMemory.load('trippedd');
  const sources = Object.values(memory.sources) as Array<{ fileId?: string; mediaPath?: string; sourceOrder?: number }>;
  const gags = Object.values(memory.gags) as Array<any>;
  const sourcePaths = new Map<string, { path: string; sourceOrder: number }>();
  for (const source of sources) if (source.fileId && source.mediaPath && safeCachedPath(source.mediaPath)) sourcePaths.set(source.fileId, { path: source.mediaPath, sourceOrder: Number.isFinite(source.sourceOrder) ? Number(source.sourceOrder) : Number.MAX_SAFE_INTEGER });

  const candidates: PilotAssemblyClip[] = [];
  for (const gag of gags) {
    const sourceFileId = gag.sourceFileId;
    const source = sourceFileId ? sourcePaths.get(sourceFileId) : undefined;
    if (!sourceFileId || !source || gag.reviewState === 'HUMAN_REJECTED') continue;
    for (const signal of (gag.signals ?? []).filter((item: any) => Number.isFinite(item.startTime) && Number.isFinite(item.endTime))) {
      const start = Math.max(0, Number(signal.startTime) - padding);
      const end = Math.max(start + 0.25, Number(signal.endTime) + padding);
      candidates.push({ sourceFileId, sourcePath: source.path, sourceOrder: source.sourceOrder, start, end, gagId: gag.id, score: Number(gag.score) || 0, reason: `${signal.type}: ${signal.evidence}` });
    }
  }

  candidates.sort((a, b) => (b.score ?? 0) - (a.score ?? 0) || (a.sourceOrder ?? Number.MAX_SAFE_INTEGER) - (b.sourceOrder ?? Number.MAX_SAFE_INTEGER) || a.start - b.start);
  const selected: PilotAssemblyClip[] = [];
  for (const candidate of candidates) {
    const duplicate = selected.some(existing => existing.sourceFileId === candidate.sourceFileId && Math.abs(existing.start - candidate.start) < 0.75 && Math.abs(existing.end - candidate.end) < 0.75);
    if (!duplicate) selected.push(candidate);
    if (selected.length >= maxClips) break;
  }
  selected.sort((a, b) => (a.sourceOrder ?? Number.MAX_SAFE_INTEGER) - (b.sourceOrder ?? Number.MAX_SAFE_INTEGER) || a.start - b.start || (b.score ?? 0) - (a.score ?? 0));

  const hasSubjectivity = await fs.access(GENERATED_SUBJECTIVITY).then(() => true).catch(() => false);
  const generatedClips: PilotAssemblyGeneratedClip[] = hasSubjectivity ? [{ id: 'ep01-lost-acid-subjectivity', path: GENERATED_SUBJECTIVITY, purpose: "Audience sees the character's subjective experience before returning to live action; generated material is not physical source evidence.", provenance: 'GENERATED', position: 'POST_SOURCE_DISCOVERY' }] : [];
  const missingBeats = selected.length ? ['STORY_REVIEW', ...(hasSubjectivity ? [] : ['SUBJECTIVITY_GENERATION']), 'FINAL_EDITORIAL_ASSEMBLY', 'QC', 'GREENLIGHT'] : ['MEDIA_ANALYSIS', 'GAG_DISCOVERY', 'SOURCE_SELECTS'];
  const manifest: PilotAssemblyManifest = { episodeId: 'EP01', title: 'The Walk', cutMode: CUT_MODE, status: selected.length ? 'ROUGH_CUT_READY' : 'WAITING_FOR_EVIDENCE', generatedAt: new Date().toISOString(), sourceClipCount: sourcePaths.size, selectedClipCount: selected.length, clips: selected, generatedClips, missingBeats };

  await fs.mkdir(OUTPUT_ROOT, { recursive: true });
  const otioPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.otio`);
  const jsonPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.json`);
  const outputPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.mp4`);
  await fs.writeFile(otioPath, JSON.stringify(writeOtioTimeline(selected, generatedClips), null, 2), 'utf8');
  manifest.timelinePath = `/production/${OUTPUT_BASENAME}.otio`;
  await fs.writeFile(jsonPath, JSON.stringify(manifest, null, 2), 'utf8');
  if (!selected.length) return manifest;

  const listPath = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}.concat.txt`);
  const segmentDir = path.join(OUTPUT_ROOT, `${OUTPUT_BASENAME}-segments`);
  await fs.rm(segmentDir, { recursive: true, force: true });
  await fs.mkdir(segmentDir, { recursive: true });
  const segmentPaths: string[] = Array(selected.length + generatedClips.length);
  const renderConcurrency = Math.max(1, Math.min(Number(process.env.EP01_RENDER_CONCURRENCY || 4), 8));
  await mapConcurrent(selected, renderConcurrency, async (clip, i) => {
    const segmentPath = path.join(segmentDir, `${String(i).padStart(3, '0')}.mp4`);
    await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-ss', clip.start.toFixed(3), '-i', clip.sourcePath, '-t', (clip.end - clip.start).toFixed(3), '-map', '0:v:0', '-map', '0:a?', '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '160k', '-movflags', '+faststart', segmentPath]);
    segmentPaths[i] = segmentPath;
  });

  let nextIndex = selected.length;
  for (const generated of generatedClips) {
    const segmentPath = path.join(segmentDir, `${String(nextIndex).padStart(3, '0')}-generated.mp4`);
    await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-i', generated.path, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-shortest', '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '160k', '-movflags', '+faststart', segmentPath]);
    segmentPaths[nextIndex++] = segmentPath;
  }

  const concatText = segmentPaths.map(file => `file '${file.replace(/'/g, "'\\''")}'`).join('\n') + '\n';
  await fs.writeFile(listPath, concatText, 'utf8');
  await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', listPath, '-c', 'copy', '-movflags', '+faststart', outputPath]);
  manifest.outputPath = `/production/${OUTPUT_BASENAME}.mp4`;
  await fs.writeFile(jsonPath, JSON.stringify(manifest, null, 2), 'utf8');
  return manifest;
}
