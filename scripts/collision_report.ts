/**
 * WHICH CLIPS, not which categories.
 *
 * The creator asked for the collisions and got category names back, which is
 * useless when the job is to open the real files and say what they are. This
 * prints, for every EP01 segment that more than one piece of evidence points
 * at, the actual clips: original filename (the thing to search for in Drive),
 * recording time, duration, the transcript that caused the match, and WHY the
 * pipeline thinks it belongs there.
 *
 * It asserts nothing. Every assignment shown is a machine guess until the
 * creator says otherwise with scripts/confirm_clips.ts.
 *
 *   npx tsx scripts/collision_report.ts
 */
import { existsSync, readFileSync, readdirSync } from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { EditorialService } from '../src/server/editorialService';
import { EPISODE_01 } from '../src/core/canon/episode01';
import { resolveCanonSegment } from '../src/core/canon/canonCompliance';
import { SourceCatalog } from '../src/core/editorial/sourceCatalog';
import { recordedAtFromFilename, calibrateClocks, resolveRecordedAt, buildPhysicalTimeline } from '../src/core/analysis/recordedAt';

const SERVER = process.env.TRIPPEDD_SERVER ?? 'http://localhost:3000';
const FOOTAGE = process.env.TRIPPEDD_FOOTAGE ?? 'footage';
const STORE = path.join(process.cwd(), '.trippedd_catalog.json');

const jobs: any[] = await (await fetch(`${SERVER}/api/queue`)).json();
const byFileId = new Map(jobs.map((j) => [j.fileId, j]));

// Recording times, so every clip can be placed in the day.
const probed = readdirSync(FOOTAGE).filter((f) => /\.(mp4|mov|m4v|mkv|avi)$/i.test(f)).map((name) => {
  let duration: number | undefined, creationTime: string | undefined;
  try {
    const f = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_entries',
      'format=duration:format_tags=creation_time', '-of', 'json', path.join(FOOTAGE, name)],
      { encoding: 'utf8' })).format ?? {};
    duration = f.duration ? Number(f.duration) : undefined;
    creationTime = f.tags?.creation_time;
  } catch { /* still listed, just without timing */ }
  return { name, duration, creationTime };
});
const cal = calibrateClocks(probed.map((p) => ({
  filenameAt: recordedAtFromFilename(p.name).at, containerAt: p.creationTime, durationSec: p.duration })));
const { timeline } = buildPhysicalTimeline(probed.map((p) => ({
  fileId: p.name.replace(/\.[^.]+$/, ''), originalName: p.name,
  recordedAt: resolveRecordedAt(p.name, p.creationTime, { durationSec: p.duration, calibration: cal }),
  durationSec: p.duration })));
const timing = new Map(timeline.map((t) => [t.fileId, t]));

const catalog: SourceCatalog = existsSync(STORE)
  ? SourceCatalog.fromJSON(JSON.parse(readFileSync(STORE, 'utf8'))) : new SourceCatalog();

const svc = new EditorialService();
svc.ingestFromJobs(jobs as any);
const built = svc.build();

const hhmm = (iso?: string) => iso ? new Date(iso).toISOString().slice(11, 16) : ' ?  ';
const mmss = (s?: number) => s === undefined ? ' ? ' : `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
const segName = (id?: string) => id ? (EPISODE_01.find((s) => s.id === id)?.name ?? id) : '(none)';

// Group every candidate by the canon segment it currently maps to.
const groups = new Map<string, typeof built.scenes>();
for (const s of built.scenes) {
  const m = resolveCanonSegment({ id: s.id, proposedTitle: s.proposedTitle,
    proposedOrder: s.proposedOrder, physicalOrder: s.physicalOrder,
    storyBeatIds: s.storyBeatIds, canonSegmentId: s.canonSegmentId });
  const key = m.canonSegmentId ?? '(unmapped)';
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key)!.push(s);
}

console.log('═'.repeat(100));
console.log('COLLISION REPORT — every clip currently pointing at the same EP01 segment');
console.log('Nothing here is decided. These are machine guesses awaiting your call.');
console.log('DRIVE FILES WERE NOT RENAMED — search Drive by the ORIGINAL FILENAME shown.');
console.log('═'.repeat(100));

for (const [canonId, scenes] of [...groups.entries()]) {
  const collision = scenes.length > 1 && canonId !== '(unmapped)';
  console.log(`\n${collision ? '>>> COLLISION  ' : '    '}${segName(canonId)}   [${canonId}]   ${scenes.length} candidate(s)`);
  console.log('    ' + '─'.repeat(94));

  for (const s of scenes.sort((a, b) => a.proposedOrder - b.proposedOrder)) {
    console.log(`\n    CANDIDATE "${s.proposedTitle}"   [${s.kind}]  ${s.proposedDuration}s  confidence ${s.confidence}`);
    console.log(`      matched via story beats: ${s.storyBeatIds.join(', ') || '(none)'}`);
    console.log(`      why: ${s.editorialRationale?.slice(0, 150) ?? '(no rationale recorded)'}`);

    const clipIds = [...new Set(s.ranges.map((r) => r.sourceFileId))];
    for (const id of clipIds) {
      const job = byFileId.get(id);
      const t = timing.get(id);
      const cat = catalog.get(id);
      const ranges = s.ranges.filter((r) => r.sourceFileId === id);
      console.log(`\n      SOURCE ID              ${id}`);
      console.log(`      ORIGINAL FILENAME      ${job?.originalName ?? `${id}.mp4`}   <-- open THIS in Drive`);
      console.log(`      DRIVE FILE RENAMED     NO`);
      console.log(`      CATALOG DISPLAY NAME   ${cat?.displayName ?? '(none assigned)'}`);
      console.log(`      RECORDED AT            ${hhmm(t?.recordedAt.at)}  (session ${t?.sessionId ?? '?'}, physical #${(t?.physicalIndex ?? -1) + 1} of the day)`);
      console.log(`      DURATION               ${mmss(t?.durationSec)}`);
      console.log(`      USED RANGES            ${ranges.map((r) => `${r.startTime.toFixed(1)}-${r.endTime.toFixed(1)}s`).join(', ')}`);
      console.log(`      ASSIGNMENT STATUS      ${cat?.assignmentStatus ?? 'UNASSIGNED'}`);

      const tr = (job?.observations ?? []).filter((o: any) => o.type === 'TRANSCRIPT_SEGMENT');
      const inRange = tr.filter((o: any) => ranges.some((r) => o.startTime < r.endTime && o.endTime > r.startTime));
      console.log(`      TRANSCRIPT (${inRange.length} of ${tr.length} lines fall in the used ranges)`);
      for (const o of (inRange.length ? inRange : tr).slice(0, 6)) {
        const conf = o.avgLogprob !== undefined ? ` [logprob ${Number(o.avgLogprob).toFixed(2)}]` : '';
        console.log(`         ${Number(o.startTime).toFixed(1).padStart(6)}s  ${String(o.text).slice(0, 66)}${conf}`);
      }
      if (!tr.length) console.log('         (no speech found in this clip — identify it visually)');
    }
  }
}

// Clips with no candidate at all. They are footage too.
const used = new Set(built.scenes.flatMap((s) => s.ranges.map((r) => r.sourceFileId)));
const orphans = timeline.filter((t) => !used.has(t.fileId));
if (orphans.length) {
  console.log('\n' + '═'.repeat(100));
  console.log(`CLIPS NO CANDIDATE USES (${orphans.length}) — real footage the assembly has not placed`);
  console.log('═'.repeat(100));
  for (const t of orphans) {
    const job = byFileId.get(t.fileId);
    const tr = (job?.observations ?? []).filter((o: any) => o.type === 'TRANSCRIPT_SEGMENT');
    console.log(`\n  ${hhmm(t.recordedAt.at)}  ${mmss(t.durationSec).padStart(5)}  ${t.originalName}   (session ${t.sessionId})`);
    if (!tr.length) console.log('      no speech found — identify visually');
    for (const o of tr.slice(0, 3)) console.log(`      ${Number(o.startTime).toFixed(1).padStart(6)}s  ${String(o.text).slice(0, 70)}`);
  }
}

console.log('\n' + '─'.repeat(100));
console.log('To settle any of these, one line each:');
console.log('  npx tsx scripts/confirm_clips.ts "104742101 = cigar store" "110016345 = walk" "160715990 != joe"');
