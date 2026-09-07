/**
 * Editorial project export.
 *
 * Produces genuinely loadable projects, not a JSON "edit plan":
 *   - OpenTimelineIO for interchange, written by the real otio library;
 *   - Kdenlive/MLT XML that the real `melt` binary can parse and render.
 *
 * Every clip references real media at real time ranges taken from the scene
 * candidate. There are no placeholder clips and no invented timecodes: an
 * export whose media is missing fails rather than emitting a plausible file.
 */
import path from 'path';
import { writeFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { executeTool } from '../tools/execution/executor';
import { runnerRoot } from '../tools/execution/runnerRoot';
import type { EditorialSceneCandidate, SourceRange } from './types';
import type { ToolRunProvenance } from '../types';

export interface MediaResolver {
  /** Absolute path of the real media for a source file id, if present. */
  (sourceFileId: string): string | undefined;
}

export interface ExportResult {
  format: 'otio' | 'kdenlive';
  outputPath: string;
  clipCount: number;
  totalDuration: number;
  provenance?: ToolRunProvenance;
  /** Set when the export was verified by loading it back with a real tool. */
  verified: boolean;
  verifyDetail?: string;
}

export class MissingMediaError extends Error {
  constructor(public readonly sourceFileId: string) {
    super(`no local media resolved for source file "${sourceFileId}" — refusing to export a project referencing media that is not there`);
    this.name = 'MissingMediaError';
  }
}

function resolveAll(scenes: EditorialSceneCandidate[], resolve: MediaResolver) {
  const media = new Map<string, string>();
  for (const s of scenes) {
    for (const r of s.ranges) {
      if (media.has(r.sourceFileId)) continue;
      const p = resolve(r.sourceFileId);
      if (!p || !existsSync(p)) throw new MissingMediaError(r.sourceFileId);
      media.set(r.sourceFileId, p);
    }
  }
  return media;
}

function orderedRanges(scenes: EditorialSceneCandidate[]): { scene: EditorialSceneCandidate; range: SourceRange }[] {
  return [...scenes]
    .sort((a, b) => a.proposedOrder - b.proposedOrder)
    .flatMap((scene) => scene.ranges.map((range) => ({ scene, range })));
}

// ------------------------------------------------------------------- OTIO

/**
 * Builds the timeline via the real opentimelineio library so the file is
 * whatever that library says an OTIO file is, rather than our guess at its
 * schema.
 */
export async function exportOTIO(
  scenes: EditorialSceneCandidate[],
  resolve: MediaResolver,
  outDir: string,
  opts: { name?: string; pythonPath: string; rate?: number }
): Promise<ExportResult> {
  const media = resolveAll(scenes, resolve);
  const items = orderedRanges(scenes);
  if (!items.length) throw new Error('no ranges to export');

  await mkdir(outDir, { recursive: true });
  const outputPath = path.join(outDir, `${opts.name ?? 'episode'}.otio`);
  const rate = opts.rate ?? 30;

  const spec = {
    name: opts.name ?? 'TRIPPEDD Edit',
    rate,
    clips: items.map(({ scene, range }) => ({
      name: `${scene.proposedTitle} [${range.sourceFileId}]`,
      target_url: media.get(range.sourceFileId)!,
      start: range.startTime,
      duration: Number((range.endTime - range.startTime).toFixed(3)),
      scene_id: scene.id,
    })),
  };

  const specPath = path.join(outDir, `${opts.name ?? 'episode'}.spec.json`);
  await writeFile(specPath, JSON.stringify(spec, null, 2));

  const script = `
import json, sys
import opentimelineio as otio

spec = json.load(open(sys.argv[1]))
tl = otio.schema.Timeline(name=spec["name"])
track = otio.schema.Track(name="V1", kind=otio.schema.TrackKind.Video)
tl.tracks.append(track)
rate = spec["rate"]

for c in spec["clips"]:
    mr = otio.opentime.TimeRange(
        start_time=otio.opentime.RationalTime(round(c["start"] * rate), rate),
        duration=otio.opentime.RationalTime(round(c["duration"] * rate), rate),
    )
    clip = otio.schema.Clip(
        name=c["name"],
        media_reference=otio.schema.ExternalReference(target_url=c["target_url"]),
        source_range=mr,
    )
    clip.metadata["trippedd"] = {"scene_id": c["scene_id"]}
    track.append(clip)

otio.adapters.write_to_file(tl, sys.argv[2])

# Read it back and report what the library itself sees, so a claim of success
# is the library's, not ours.
back = otio.adapters.read_from_file(sys.argv[2])
# each_clip() was removed in otio 0.17+; find_clips() is the current API and
# older builds still have each_clip, so support whichever this install has.
if hasattr(back, "find_clips"):
    n = len(list(back.find_clips()))
elif hasattr(back, "each_clip"):
    n = len(list(back.each_clip()))
else:
    n = sum(len([c for c in t if isinstance(c, otio.schema.Clip)]) for t in back.tracks)
print(json.dumps({"clips": n, "duration": back.duration().to_seconds()}))
`.trim();

  const scriptPath = path.join(outDir, '_otio_build.py');
  await writeFile(scriptPath, script);

  const r = await executeTool({
    tool: 'otio', version: 'export', executablePath: opts.pythonPath,
    args: [scriptPath, specPath, outputPath],
    sourceFileId: 'editorial-export', timeoutMs: 120_000,
  });

  if (!r.provenance.success) {
    throw new Error(`OTIO export failed: ${r.stderr.slice(0, 300)}`);
  }

  let verified = false;
  let verifyDetail = '';
  try {
    const back = JSON.parse(r.stdout.trim().split('\n').pop() || '{}');
    verified = back.clips === spec.clips.length;
    verifyDetail = `otio read back ${back.clips} clip(s), ${Number(back.duration).toFixed(2)}s`;
  } catch {
    verifyDetail = 'could not parse verification output';
  }

  return {
    format: 'otio',
    outputPath,
    clipCount: spec.clips.length,
    totalDuration: spec.clips.reduce((a, c) => a + c.duration, 0),
    provenance: r.provenance,
    verified,
    verifyDetail,
  };
}

// --------------------------------------------------------------- Kdenlive

function xmlEscape(s: string): string {
  return s.replace(/[<>&"']/g, (c) =>
    ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&apos;' }[c]!));
}

function tc(seconds: number, rate: number): string {
  // MLT accepts clock format; frames keep the cut on a real frame boundary.
  const f = Math.max(0, Math.round(seconds * rate));
  const total = f / rate;
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${s.toFixed(3).padStart(6, '0')}`;
}

/**
 * Emits Kdenlive-compatible MLT XML. Kdenlive projects ARE MLT documents, so
 * one file serves both opening in Kdenlive and rendering with melt.
 */
export async function exportKdenlive(
  scenes: EditorialSceneCandidate[],
  resolve: MediaResolver,
  outDir: string,
  opts: { name?: string; rate?: number; meltPath?: string } = {}
): Promise<ExportResult> {
  const media = resolveAll(scenes, resolve);
  const items = orderedRanges(scenes);
  if (!items.length) throw new Error('no ranges to export');

  const rate = opts.rate ?? 30;
  await mkdir(outDir, { recursive: true });
  const outputPath = path.join(outDir, `${opts.name ?? 'episode'}.kdenlive`);

  const producers: string[] = [];
  const entries: string[] = [];
  const producerIdFor = new Map<string, string>();

  let pIdx = 0;
  for (const [fileId, filePath] of media) {
    const id = `producer${pIdx++}`;
    producerIdFor.set(fileId, id);
    producers.push(
      `  <producer id="${id}" in="00:00:00.000">\n` +
      `    <property name="resource">${xmlEscape(filePath)}</property>\n` +
      `    <property name="mlt_service">avformat</property>\n` +
      `    <property name="trippedd:source_file_id">${xmlEscape(fileId)}</property>\n` +
      `  </producer>`
    );
  }

  let totalDuration = 0;
  for (const { scene, range } of items) {
    const pid = producerIdFor.get(range.sourceFileId)!;
    totalDuration += range.endTime - range.startTime;
    entries.push(
      `    <entry producer="${pid}" in="${tc(range.startTime, rate)}" out="${tc(range.endTime, rate)}">\n` +
      `      <property name="trippedd:scene">${xmlEscape(scene.proposedTitle)}</property>\n` +
      `      <property name="trippedd:scene_id">${xmlEscape(scene.id)}</property>\n` +
      `    </entry>`
    );
  }

  const xml =
`<?xml version="1.0" encoding="utf-8"?>
<mlt LC_NUMERIC="C" version="7.0.0" producer="main_bin" profile="automatic">
  <profile description="automatic" frame_rate_num="${rate}" frame_rate_den="1"
           width="1920" height="1080" display_aspect_num="16" display_aspect_den="9"
           sample_aspect_num="1" sample_aspect_den="1" colorspace="709" progressive="1"/>
${producers.join('\n')}
  <playlist id="playlist0">
${entries.join('\n')}
  </playlist>
  <tractor id="tractor0" title="${xmlEscape(opts.name ?? 'TRIPPEDD Edit')}">
    <track producer="playlist0"/>
  </tractor>
</mlt>
`;

  await writeFile(outputPath, xml);

  // Verify by having the REAL melt binary parse it. A project that melt cannot
  // consume is not a project, however well-formed the XML looks.
  let verified = false;
  let verifyDetail = 'melt not available; XML written but not verified';
  let provenance: ToolRunProvenance | undefined;

  const melt = opts.meltPath ?? '/usr/bin/melt';
  if (existsSync(melt)) {
    const r = await executeTool({
      tool: 'melt', version: 'verify', executablePath: melt,
      args: ['-consumer', 'xml:/dev/null', outputPath],
      sourceFileId: 'editorial-export', timeoutMs: 120_000,
      cwd: runnerRoot(),
    });
    provenance = r.provenance;
    verified = r.provenance.success;
    verifyDetail = verified
      ? 'melt parsed the project successfully'
      : `melt rejected the project: ${r.stderr.slice(0, 200)}`;
  }

  return {
    format: 'kdenlive',
    outputPath,
    clipCount: items.length,
    totalDuration: Number(totalDuration.toFixed(3)),
    provenance,
    verified,
    verifyDetail,
  };
}
