/**
 * The day, in the order it was actually recorded.
 *
 * The camera stamped the recording time into every filename and this pipeline
 * spent its whole build treating that as an opaque id. It is the one piece of
 * evidence that survives every ASR failure, and it is what separates two visits
 * to the same store: not their content, which is nearly identical, but the
 * hours between them.
 *
 *   npx tsx scripts/physical_timeline.ts [footage-dir] [--gap 600]
 */
import { readdirSync, statSync } from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import {
  resolveRecordedAt, recordedAtFromFilename, calibrateClocks,
  buildPhysicalTimeline, sessionsOf, type ClipTiming,
} from '../src/core/analysis/recordedAt';

const dir = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'footage';
const gapArg = process.argv.indexOf('--gap');
const sessionGap = gapArg >= 0 ? Number(process.argv[gapArg + 1]) : 600;

const files = readdirSync(dir).filter((f) => /\.(mp4|mov|m4v|mkv|avi)$/i.test(f)).sort();
if (!files.length) { console.log(`no media in ${dir}`); process.exit(0); }

function probe(p: string): { duration?: number; creationTime?: string } {
  try {
    const out = execFileSync('ffprobe', ['-v', 'error', '-show_entries',
      'format=duration:format_tags=creation_time', '-of', 'json', p], { encoding: 'utf8' });
    const f = JSON.parse(out).format ?? {};
    return { duration: f.duration ? Number(f.duration) : undefined, creationTime: f.tags?.creation_time };
  } catch { return {}; }
}

const probed = files.map((name) => ({ name, ...probe(path.join(dir, name)) }));

// Work out how the camera's two clocks relate BEFORE calling anything a
// disagreement. Naive comparison flags every clip on this shoot.
const calibration = calibrateClocks(probed.map((p) => ({
  filenameAt: recordedAtFromFilename(p.name).at,
  containerAt: p.creationTime,
  durationSec: p.duration,
})));

if (calibration) {
  const sign = calibration.utcOffsetHours >= 0 ? '+' : '';
  console.log(
    `clock calibration (measured on ${calibration.sampleSize} clips): filenames are local time ` +
    `UTC${sign}${calibration.utcOffsetHours}, container creation_time is UTC and is written at the ` +
    `${calibration.containerStampsEndOfRecording ? 'END' : 'START'} of recording. ` +
    `Residual after both: ${calibration.residualSeconds}s.`);
}

const clips: ClipTiming[] = probed.map(({ name, duration, creationTime }) => ({
  fileId: name.replace(/\.[^.]+$/, ''),
  originalName: name,
  recordedAt: resolveRecordedAt(name, creationTime, { durationSec: duration, calibration }),
  durationSec: duration,
}));

const { timeline, undated } = buildPhysicalTimeline(clips, sessionGap);
const hhmm = (iso: string) => new Date(iso).toISOString().slice(11, 19);
const mmss = (s?: number) => s === undefined ? '  ?  ' : `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
const gapStr = (s?: number) => s === undefined ? '' :
  s < 90 ? `+${s}s` : s < 3600 ? `+${Math.round(s / 60)}m` : `+${(s / 3600).toFixed(1)}h`;

console.log('═'.repeat(96));
console.log(`PHYSICAL TIMELINE — ${timeline.length} clips, session gap ${sessionGap}s`);
console.log('═'.repeat(96));

for (const s of sessionsOf(timeline)) {
  const mins = (new Date(s.endedAt).getTime() - new Date(s.startedAt).getTime()) / 60000;
  console.log(`\n${s.sessionId}   ${hhmm(s.startedAt)} → ${hhmm(s.endedAt)}   (${mins.toFixed(0)} min, ${s.clips.length} clip${s.clips.length === 1 ? '' : 's'})`);
  console.log('─'.repeat(96));
  for (const c of s.clips) {
    console.log(
      `  #${String(c.physicalIndex + 1).padStart(2)}  ${hhmm(c.recordedAt.at!)}  ${mmss(c.durationSec).padStart(6)}  ` +
      `${String(gapStr(c.gapFromPreviousSec)).padStart(6)}  ${c.originalName}`
    );
    if (c.recordedAt.disagreement) {
      const d = c.recordedAt.disagreement;
      console.log(`        NOTE filename says ${hhmm(d.filename)}, container says ${hhmm(d.container)} — ${d.deltaSeconds}s apart. Filename used.`);
    }
  }
}

if (undated.length) {
  console.log(`\nNO ESTABLISHABLE RECORDING TIME (${undated.length}) — kept in input order, never given a time they do not have:`);
  for (const u of undated) console.log(`  ${u.originalName}`);
}

const total = timeline.reduce((a, c) => a + (c.durationSec ?? 0), 0);
const span = timeline.length
  ? (new Date(timeline[timeline.length - 1].recordedAt.at!).getTime() - new Date(timeline[0].recordedAt.at!).getTime()) / 3600000
  : 0;
console.log('\n' + '─'.repeat(96));
console.log(`${(total / 60).toFixed(1)} min of footage recorded across ${span.toFixed(1)} hours, in ${sessionsOf(timeline).length} sessions.`);
console.log('A session boundary is a real gap in filming. Two clips in different sessions are different');
console.log('moments even when they look and sound identical — which is what separates repeat visits.');
