import fs from 'fs/promises';
import path from 'path';
import { spawn } from 'child_process';
import { productionMemory } from './productionMemory';

export interface PilotAssemblyClip { sourceFileId: string; sourcePath: string; start: number; end: number; gagId?: string; score?: number; reason: string; }
export interface PilotAssemblyManifest {
  episodeId: 'EP01'; title: 'The Walk'; status: 'ROUGH_CUT_READY' | 'WAITING_FOR_EVIDENCE'; generatedAt: string;
  sourceClipCount: number; selectedClipCount: number; clips: PilotAssemblyClip[]; missingBeats: string[]; outputPath?: string; timelinePath?: string;
}

const CACHE_ROOT = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media'));
const OUTPUT_ROOT = path.resolve(process.env.TRIPPEDD_OUTPUT_DIR || path.join(process.cwd(), 'public', 'production'));

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

function writeOtioTimeline(clips: PilotAssemblyClip[], outputPath: string) {
  const rate = 24;
  let timelineFrame = 0;
  const otioClips = clips.map((clip, index) => {
    const durationFrames = Math.max(1, Math.round((clip.end - clip.start) * rate));
    const item = {
      OTIO_SCHEMA: 'Clip.2',
      name: `EP01-${String(index + 1).padStart(3, '0')}-${clip.gagId || 'select'}`,
      source_range: {
        OTIO_SCHEMA: 'TimeRange.1',
        start_time: { OTIO_SCHEMA: 'RationalTime.1', value: Math.round(clip.start * rate), rate },
        duration: { OTIO_SCHEMA: 'RationalTime.1', value: durationFrames, rate }
      },
      media_reference: {
        OTIO_SCHEMA: 'ExternalReference.1',
        target_url: clip.sourcePath,
        available_range: null,
        metadata: {
          trippedd: {
            sourceFileId: clip.sourceFileId,
            gagId: clip.gagId,
            score: clip.score,
            reason: clip.reason,
            provenance: 'SOURCE_MEDIA'
          }
        }
      },
      metadata: { trippedd: { timelineStartFrame: timelineFrame, physicalTruth: true } }
    };
    timelineFrame += durationFrames;
    return item;
  });
  return {
    OTIO_SCHEMA: 'Timeline.1',
    name: 'TRIPPEDD EP01 — The Walk — First Assembly',
    global_start_time: null,
    tracks: [{ OTIO_SCHEMA: 'Stack.1', name: 'Video 1', children: [{ OTIO_SCHEMA: 'Track.1', name: 'Picture', kind: 'Video', children: otioClips }] }],
    metadata: {
      trippedd: {
        episodeId: 'EP01',
        editorialStatus: 'ROUGH_CUT',
        physicalSourceChronology: 'AUTHORITATIVE_FOR_WHAT_HAPPENED',
        generatedMaterialPolicy: 'NOT_PHYSICAL_SOURCE_EVIDENCE',
        nextStages: ['SUBJECTIVITY_GENERATION', 'EDITORIAL_LOCK', 'QC', 'SHOWRUNNER_GREENLIGHT']
      }
    }
  };
}

/** Build an actual MP4 first assembly from cached source media and timed comedy selects. */
export async function buildEp01FirstAssembly(options: { maxClips?: number; clipPaddingSeconds?: number } = {}): Promise<PilotAssemblyManifest> {
  const maxClips = Math.max(1, Math.min(options.maxClips ?? 24, 80));
  const padding = Math.max(0, Math.min(options.clipPaddingSeconds ?? 1.25, 5));
  const memory = await productionMemory.load('trippedd');
  const sources = Object.values(memory.sources) as Array<{ fileId?: string; mediaPath?: string }>;
  const gags = Object.values(memory.gags) as Array<any>;
  const sourcePaths = new Map<string, string>();
  for (const source of sources) if (source.fileId && source.mediaPath && safeCachedPath(source.mediaPath)) sourcePaths.set(source.fileId, source.mediaPath);

  const candidates: PilotAssemblyClip[] = [];
  for (const gag of gags) {
    const sourceFileId = gag.sourceFileId;
    const sourcePath = sourceFileId ? sourcePaths.get(sourceFileId) : undefined;
    if (!sourceFileId || !sourcePath || gag.reviewState === 'HUMAN_REJECTED') continue;
    for (const signal of (gag.signals ?? []).filter((item: any) => Number.isFinite(item.startTime) && Number.isFinite(item.endTime))) {
      const start = Math.max(0, Number(signal.startTime) - padding);
      const end = Math.max(start + 0.25, Number(signal.endTime) + padding);
      candidates.push({ sourceFileId, sourcePath, start, end, gagId: gag.id, score: Number(gag.score) || 0, reason: `${signal.type}: ${signal.evidence}` });
    }
  }

  candidates.sort((a, b) => (b.score ?? 0) - (a.score ?? 0));
  const selected = candidates.slice(0, maxClips).sort((a, b) => a.sourceFileId.localeCompare(b.sourceFileId) || a.start - b.start);
  const manifest: PilotAssemblyManifest = {
    episodeId: 'EP01', title: 'The Walk', status: selected.length ? 'ROUGH_CUT_READY' : 'WAITING_FOR_EVIDENCE', generatedAt: new Date().toISOString(),
    sourceClipCount: sourcePaths.size, selectedClipCount: selected.length, clips: selected,
    missingBeats: selected.length ? ['STORY_REVIEW', 'SUBJECTIVITY_GENERATION', 'FINAL_EDITORIAL_ASSEMBLY', 'QC', 'GREENLIGHT'] : ['MEDIA_ANALYSIS', 'GAG_DISCOVERY', 'SOURCE_SELECTS'],
  };

  await fs.mkdir(OUTPUT_ROOT, { recursive: true });
  const timelinePath = path.join(OUTPUT_ROOT, 'EP01-first-assembly.otio');
  await fs.writeFile(timelinePath, JSON.stringify(writeOtioTimeline(selected, timelinePath), null, 2), 'utf8');
  manifest.timelinePath = '/production/EP01-first-assembly.otio';
  await fs.writeFile(path.join(OUTPUT_ROOT, 'EP01-first-assembly.json'), JSON.stringify(manifest, null, 2), 'utf8');
  if (!selected.length) return manifest;

  const listPath = path.join(OUTPUT_ROOT, 'EP01-first-assembly.concat.txt');
  const segmentDir = path.join(OUTPUT_ROOT, 'EP01-first-assembly-segments');
  await fs.rm(segmentDir, { recursive: true, force: true });
  await fs.mkdir(segmentDir, { recursive: true });
  const segmentPaths: string[] = Array(selected.length);
  const renderConcurrency = Math.max(1, Math.min(Number(process.env.EP01_RENDER_CONCURRENCY || 4), 8));

  await mapConcurrent(selected, renderConcurrency, async (clip, i) => {
    const segmentPath = path.join(segmentDir, `${String(i).padStart(3, '0')}.mp4`);
    await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-ss', clip.start.toFixed(3), '-i', clip.sourcePath, '-t', (clip.end - clip.start).toFixed(3), '-map', '0:v:0', '-map', '0:a?', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', segmentPath]);
    segmentPaths[i] = segmentPath;
  });

  const concatText = segmentPaths.map(file => `file '${file.replace(/'/g, "'\\''")}'`).join('\n') + '\n';
  await fs.writeFile(listPath, concatText, 'utf8');
  const outputPath = path.join(OUTPUT_ROOT, 'EP01-first-assembly.mp4');
  await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', listPath, '-c', 'copy', '-movflags', '+faststart', outputPath]);
  manifest.outputPath = '/production/EP01-first-assembly.mp4';
  await fs.writeFile(path.join(OUTPUT_ROOT, 'EP01-first-assembly.json'), JSON.stringify(manifest, null, 2), 'utf8');
  return manifest;
}
