import { describe, it, expect, beforeAll } from 'vitest';
import path from 'path';
import os from 'os';
import { mkdtempSync, existsSync, writeFileSync, readFileSync } from 'fs';
import { execFileSync } from 'child_process';
import { exportOTIO, exportKdenlive, MissingMediaError } from '../projectExport';
import { runnerRoot } from '../../tools/execution/runnerRoot';
import type { EditorialSceneCandidate } from '../types';

const PY = path.join(runnerRoot(), '.trippedd_venv', 'bin', 'python');
const MELT = '/usr/bin/melt';
const FFMPEG = '/usr/bin/ffmpeg';

const hasOtio = existsSync(PY) && (() => {
  try { execFileSync(PY, ['-c', 'import opentimelineio']); return true; } catch { return false; }
})();
const hasMelt = existsSync(MELT);
const hasFfmpeg = existsSync(FFMPEG);

let mediaDir: string;
let clipA: string;
let clipB: string;

beforeAll(() => {
  mediaDir = mkdtempSync(path.join(os.tmpdir(), 'ed-media-'));
  clipA = path.join(mediaDir, 'a.mp4');
  clipB = path.join(mediaDir, 'b.mp4');
  if (hasFfmpeg) {
    // Real media, so the exports reference files that genuinely exist.
    for (const p of [clipA, clipB]) {
      execFileSync(FFMPEG, ['-y', '-v', 'error', '-f', 'lavfi', '-i',
        'testsrc=size=320x240:rate=15', '-t', '15', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', p]);
    }
  } else {
    writeFileSync(clipA, 'x'); writeFileSync(clipB, 'x');
  }
});

let n = 0;
function scene(over: Partial<EditorialSceneCandidate> = {}): EditorialSceneCandidate {
  return {
    id: `sc${n++}`, productionUnitId: 'u', proposedTitle: 'A Scene', purpose: 'p',
    sourceEvidenceIds: [], sourceClipIds: ['a'], transcriptSegmentIds: [],
    visualObservationIds: [], referenceIds: [], storyBeatIds: ['b'],
    proposedOrder: 0, physicalOrder: 0,
    ranges: [{ sourceFileId: 'a', startTime: 2, endTime: 6, derivedFromObservationIds: ['o1'] }],
    proposedDuration: 4, beatMap: [], excludedMaterial: [], confidence: 0.8,
    editorialRationale: 'r', chronologyAssumptions: [], missingEvidence: [], evidenceLimitations: [],
    requiredAssets: [], generatedAssetIds: [], humanReviewState: 'PROPOSED',
    revisionHistory: [], createdAt: '', updatedAt: '', ...over,
  };
}

const resolver = (id: string) => ({ a: clipA, b: clipB }[id]);

describe('Project export — refuses to reference media that is not there', () => {
  it('throws MissingMediaError rather than emitting a project with a dead reference', async () => {
    const out = mkdtempSync(path.join(os.tmpdir(), 'ed-out-'));
    await expect(
      exportKdenlive([scene({ ranges: [{ sourceFileId: 'ghost', startTime: 0, endTime: 1, derivedFromObservationIds: [] }] })],
        () => undefined, out)
    ).rejects.toThrow(MissingMediaError);
  });
});

describe.skipIf(!hasMelt || !hasFfmpeg)('Kdenlive/MLT export — verified by the real melt binary', () => {
  it('produces a project melt can parse, referencing real files at real ranges', async () => {
    const out = mkdtempSync(path.join(os.tmpdir(), 'ed-out-'));
    const scenes = [
      scene({ proposedOrder: 0, ranges: [{ sourceFileId: 'a', startTime: 2, endTime: 6, derivedFromObservationIds: ['o1'] }] }),
      scene({ proposedOrder: 1, sourceClipIds: ['b'], ranges: [{ sourceFileId: 'b', startTime: 1.5, endTime: 4, derivedFromObservationIds: ['o2'] }] }),
    ];

    const res = await exportKdenlive(scenes, resolver, out, { name: 'test_ep' });

    expect(res.verified, res.verifyDetail).toBe(true);
    expect(res.clipCount).toBe(2);
    expect(existsSync(res.outputPath)).toBe(true);

    const xml = readFileSync(res.outputPath, 'utf8');
    // Real absolute media paths, not placeholders.
    expect(xml).toContain(clipA);
    expect(xml).toContain(clipB);
    // Real in/out points derived from the scene ranges.
    expect(xml).toContain('in="00:00:02.000"');
    expect(xml).toContain('out="00:00:06.000"');
    expect(xml).not.toMatch(/placeholder|TODO|dummy/i);
  }, 120_000);

  it('the exported project actually renders', async () => {
    const out = mkdtempSync(path.join(os.tmpdir(), 'ed-out-'));
    const res = await exportKdenlive([scene()], resolver, out, { name: 'render_ep' });
    const rendered = path.join(out, 'rendered.mp4');

    execFileSync(MELT, ['-consumer', `avformat:${rendered}`, res.outputPath], { stdio: 'ignore' });
    expect(existsSync(rendered)).toBe(true);

    // A project that renders to an empty file is not a working project.
    const probe = execFileSync('/usr/bin/ffprobe',
      ['-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', rendered]).toString();
    expect(Number(probe.trim())).toBeGreaterThan(1);
  }, 180_000);

  it('writes clips in editorial order, not physical order', async () => {
    const out = mkdtempSync(path.join(os.tmpdir(), 'ed-out-'));
    const scenes = [
      scene({ proposedOrder: 1, physicalOrder: 0, sourceClipIds: ['a'], ranges: [{ sourceFileId: 'a', startTime: 1, endTime: 3, derivedFromObservationIds: [] }] }),
      scene({ proposedOrder: 0, physicalOrder: 1, sourceClipIds: ['b'], ranges: [{ sourceFileId: 'b', startTime: 5, endTime: 7, derivedFromObservationIds: [] }] }),
    ];
    const res = await exportKdenlive(scenes, resolver, out, { name: 'order_ep' });
    const xml = readFileSync(res.outputPath, 'utf8');

    const entries = [...xml.matchAll(/<entry producer="(\w+)"/g)].map((m) => m[1]);
    const producerB = xml.match(new RegExp(`<producer id="(\\w+)"[^>]*>\\s*<property name="resource">${clipB.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`))?.[1];
    // The editorially-first scene (clip b) is laid down first.
    expect(entries[0]).toBe(producerB);
  }, 120_000);
});

describe.skipIf(!hasOtio || !hasFfmpeg)('OTIO export — verified by the real otio library', () => {
  it('writes a timeline the library reads back with the same clip count', async () => {
    const out = mkdtempSync(path.join(os.tmpdir(), 'ed-out-'));
    const scenes = [
      scene({ proposedOrder: 0, ranges: [{ sourceFileId: 'a', startTime: 2, endTime: 6, derivedFromObservationIds: ['o1'] }] }),
      scene({ proposedOrder: 1, sourceClipIds: ['b'], ranges: [{ sourceFileId: 'b', startTime: 1, endTime: 3, derivedFromObservationIds: ['o2'] }] }),
    ];

    const res = await exportOTIO(scenes, resolver, out, { name: 'otio_ep', pythonPath: PY });

    expect(res.verified, res.verifyDetail).toBe(true);
    expect(res.clipCount).toBe(2);
    expect(res.provenance?.executionState).toBe('EXECUTED');
    expect(res.provenance?.exitCode).toBe(0);

    // Real media targets survive the round trip.
    const doc = JSON.parse(readFileSync(res.outputPath, 'utf8'));
    const clips = doc.tracks.children.flatMap((t: any) => t.children);
    expect(clips.length).toBe(2);
    const urls = clips.map((c: any) =>
      c.media_reference?.target_url ??
      c.media_references?.[c.active_media_reference_key ?? 'DEFAULT_MEDIA']?.target_url);
    expect(urls).toContain(clipA);
    expect(urls).toContain(clipB);

    // Real frame-accurate ranges, not zeros.
    for (const c of clips) {
      expect(c.source_range.duration.value).toBeGreaterThan(0);
      expect(c.source_range.start_time.rate).toBe(30);
    }
  }, 180_000);
});
