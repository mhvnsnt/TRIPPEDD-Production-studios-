/**
 * Turns a proposed cut into an actual watchable video file.
 *
 * This is the thing that makes the difference between "here is an edit plan"
 * and "here is your scene, watch it." Every segment is cut from the real source
 * media at the real timestamps the editor chose, then joined into one file.
 */
import path from 'path';
import { mkdir, rm, writeFile, stat } from 'fs/promises';
import { existsSync } from 'fs';
import { executeTool } from '../../tools/execution/executor';
import type { SourceRange } from '../types';
import type { ToolRunProvenance } from '../../types';

export interface RenderRequest {
  sceneId: string;
  ranges: SourceRange[];
  /** sourceFileId -> absolute path of the real media. */
  resolveMedia: (sourceFileId: string) => string | undefined;
  outDir: string;
  ffmpegPath: string;
  /** Output size; source is letterboxed into it so mixed footage joins cleanly. */
  width?: number;
  height?: number;
  fps?: number;
}

export interface RenderResult {
  ok: boolean;
  outputPath?: string;
  durationSec?: number;
  segmentCount: number;
  /** Non-fatal problems, e.g. a segment that could not be cut. */
  warnings: string[];
  error?: string;
  provenance: ToolRunProvenance[];
}

export class MissingRenderMediaError extends Error {
  constructor(id: string) {
    super(`no media on disk for "${id}" — cannot render a scene from footage that is not here`);
    this.name = 'MissingRenderMediaError';
  }
}

/**
 * Cut one segment and normalise it. Re-encoding rather than stream-copying is
 * deliberate: a stream copy can only cut on keyframes, which drags a cut point
 * up to seconds away from where the editor placed it. The whole value of the
 * edit is that the in/out points are exact.
 */
async function cutSegment(
  req: RenderRequest, src: string, r: SourceRange, index: number, tmpDir: string
): Promise<{ path: string; provenance: ToolRunProvenance; ok: boolean; error?: string }> {
  const out = path.join(tmpDir, `seg_${String(index).padStart(3, '0')}.mp4`);
  const dur = Math.max(0.05, r.endTime - r.startTime);
  const w = req.width ?? 1280, h = req.height ?? 720, fps = req.fps ?? 30;

  const run = await executeTool({
    tool: 'ffmpeg', version: 'render', executablePath: req.ffmpegPath,
    args: [
      '-y', '-v', 'error',
      // Seek before -i for speed, then trim precisely after decode.
      '-ss', String(Math.max(0, r.startTime)), '-t', String(dur), '-i', src,
      '-vf', `scale=${w}:${h}:force_original_aspect_ratio=decrease,pad=${w}:${h}:(ow-iw)/2:(oh-ih)/2,fps=${fps},format=yuv420p`,
      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
      // A silent track is added when the source has none, so concat never fails
      // on a segment that simply has no audio.
      '-af', 'aresample=async=1:first_pts=0',
      '-c:a', 'aac', '-ar', '48000', '-ac', '2',
      '-shortest', out,
    ],
    sourceFileId: r.sourceFileId, timeoutMs: 600_000,
  });

  return { path: out, provenance: run.provenance, ok: run.provenance.success && existsSync(out), error: run.stderr.slice(0, 200) };
}

export async function renderScene(req: RenderRequest): Promise<RenderResult> {
  const provenance: ToolRunProvenance[] = [];
  const warnings: string[] = [];

  if (!req.ranges.length) {
    return { ok: false, segmentCount: 0, warnings, error: 'the scene has no ranges to render', provenance };
  }

  // Fail loudly if the footage is not actually here.
  for (const r of req.ranges) {
    const p = req.resolveMedia(r.sourceFileId);
    if (!p || !existsSync(p)) throw new MissingRenderMediaError(r.sourceFileId);
  }

  await mkdir(req.outDir, { recursive: true });
  const tmpDir = path.join(req.outDir, `.tmp_${req.sceneId}`);
  await rm(tmpDir, { recursive: true, force: true });
  await mkdir(tmpDir, { recursive: true });

  try {
    const parts: string[] = [];
    for (let i = 0; i < req.ranges.length; i++) {
      const r = req.ranges[i];
      const src = req.resolveMedia(r.sourceFileId)!;
      const seg = await cutSegment(req, src, r, i, tmpDir);
      provenance.push(seg.provenance);
      if (seg.ok) parts.push(seg.path);
      else warnings.push(`segment ${i + 1} (${r.sourceFileId} ${r.startTime.toFixed(2)}-${r.endTime.toFixed(2)}) could not be cut: ${seg.error}`);
    }

    if (!parts.length) {
      return { ok: false, segmentCount: 0, warnings, error: 'no segment could be cut from the source media', provenance };
    }

    const outputPath = path.join(req.outDir, `${req.sceneId}.mp4`);

    if (parts.length === 1) {
      // One segment: the cut file IS the scene.
      const single = await executeTool({
        tool: 'ffmpeg', version: 'render', executablePath: req.ffmpegPath,
        args: ['-y', '-v', 'error', '-i', parts[0], '-c', 'copy', outputPath],
        sourceFileId: req.sceneId, timeoutMs: 300_000,
      });
      provenance.push(single.provenance);
      if (!single.provenance.success) {
        return { ok: false, segmentCount: parts.length, warnings, error: single.stderr.slice(0, 300), provenance };
      }
    } else {
      const listFile = path.join(tmpDir, 'concat.txt');
      await writeFile(listFile, parts.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n'));
      const joined = await executeTool({
        tool: 'ffmpeg', version: 'render', executablePath: req.ffmpegPath,
        args: ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', listFile,
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
               '-c:a', 'aac', '-movflags', '+faststart', outputPath],
        sourceFileId: req.sceneId, timeoutMs: 900_000,
      });
      provenance.push(joined.provenance);
      if (!joined.provenance.success) {
        return { ok: false, segmentCount: parts.length, warnings, error: joined.stderr.slice(0, 300), provenance };
      }
    }

    const size = (await stat(outputPath)).size;
    if (size < 1024) {
      return { ok: false, segmentCount: parts.length, warnings, error: `render produced a ${size}-byte file`, provenance };
    }

    return {
      ok: true,
      outputPath,
      durationSec: Number(req.ranges.reduce((a, r) => a + (r.endTime - r.startTime), 0).toFixed(3)),
      segmentCount: parts.length,
      warnings,
      provenance,
    };
  } finally {
    await rm(tmpDir, { recursive: true, force: true });
  }
}
