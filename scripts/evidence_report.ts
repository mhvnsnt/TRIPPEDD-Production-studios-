/**
 * What the footage actually contains, measured — not what anyone remembers
 * being in it.
 *
 * Per clip: duration, how many transcript lines came back, shot boundaries, and
 * two failure signals that are invisible in a summary and fatal in an edit —
 * a transcript that came back EMPTY, and an ASR repetition loop (the same line
 * over and over, or one "segment" spanning minutes) which is a hallucination
 * that silently swallows real dialogue.
 *
 * Then: which remembered beats the evidence actually supports, and what the
 * autonomous assembly built from it.
 *
 *   npx tsx scripts/evidence_report.ts [--server http://localhost:3000] [--transcripts]
 */
import { EditorialService } from '../src/server/editorialService';

const arg = (k: string, d: string) => {
  const i = process.argv.indexOf(k);
  return i >= 0 ? process.argv[i + 1] : d;
};
const server = arg('--server', 'http://localhost:3000');
const showTranscripts = process.argv.includes('--transcripts');

const jobs: any[] = await (await fetch(`${server}/api/queue`)).json();
if (!jobs.length) { console.log('no clips in the queue'); process.exit(0); }

console.log('═'.repeat(100));
console.log('EVIDENCE REPORT');
console.log('═'.repeat(100));

type Row = ReturnType<typeof rowFor>;
function rowFor(j: any) {
  const obs = j.observations ?? [];
  const tr = obs.filter((o: any) => o.type === 'TRANSCRIPT_SEGMENT');
  const dur = Math.max(0, ...obs.map((o: any) => o.endTime ?? 0));

  // A hallucination loop: the same line repeated, or one "segment" that runs
  // for a large share of the clip. Either way real dialogue is being lost.
  let maxRun = 1, run = 1;
  for (let i = 1; i < tr.length; i++) {
    if (tr[i].text?.trim() === tr[i - 1].text?.trim()) { run++; maxRun = Math.max(maxRun, run); } else run = 1;
  }
  const longestSeg = Math.max(0, ...tr.map((t: any) => (t.endTime ?? 0) - (t.startTime ?? 0)));

  return {
    fileId: j.fileId, name: j.originalName, state: j.state, dur,
    lines: tr.length, shots: obs.filter((o: any) => o.type === 'SHOT_BOUNDARY').length,
    words: obs.filter((o: any) => o.type === 'WORD_TIMING').length,
    ocr: obs.filter((o: any) => o.type === 'ON_SCREEN_TEXT').length,
    maxRun, longestSeg,
    silent: tr.length === 0,
    looped: maxRun >= 3 || (dur > 0 && longestSeg > dur * 0.25 && longestSeg > 20),
    first: tr[0]?.text ?? '',
    transcript: tr,
  };
}

const rows: Row[] = jobs.map(rowFor).sort((a, b) => a.name.localeCompare(b.name));

console.log('\nclip                            dur  lines shots  words  loop longestSeg  first line heard');
console.log('─'.repeat(100));
for (const r of rows) {
  const flag = r.silent ? ' SILENT' : r.looped ? ' LOOP' : '';
  console.log(
    `${r.name.padEnd(30)} ${String(Math.round(r.dur)).padStart(4)}s ${String(r.lines).padStart(5)} ` +
    `${String(r.shots).padStart(5)} ${String(r.words).padStart(6)} ${String(r.maxRun).padStart(5)} ` +
    `${r.longestSeg.toFixed(0).padStart(9)}s  ${r.first.slice(0, 44)}${flag}`
  );
}

const totalDur = rows.reduce((a, r) => a + r.dur, 0);
const silent = rows.filter((r) => r.silent);
const looped = rows.filter((r) => r.looped);
console.log('─'.repeat(100));
console.log(`${rows.length} clips · ${(totalDur / 60).toFixed(1)} min · ${rows.reduce((a, r) => a + r.lines, 0)} transcript lines`);
if (silent.length) console.log(`SILENT (no transcript at all): ${silent.length} — ${silent.map((r) => r.name).join(', ')}`);
if (looped.length) console.log(`ASR LOOP (dialogue being lost):  ${looped.length} — ${looped.map((r) => r.name).join(', ')}`);

// ── what the evidence supports ────────────────────────────────────────────
const svc = new EditorialService();
svc.ingestFromJobs(jobs as any);
const built = svc.build();

console.log('\n' + '═'.repeat(100));
console.log('REMEMBERED MATERIAL vs EVIDENCE');
console.log('═'.repeat(100));
for (const b of built.reconciliation.beats) {
  console.log(`${b.state.padEnd(18)} conf ${b.confidence.toFixed(2)}  ${b.beatId.padEnd(30)} ${b.evidence.length} piece(s)`);
}

console.log('\n' + '═'.repeat(100));
console.log(`AUTONOMOUS ASSEMBLY — ${built.scenes.length} candidate(s)`);
console.log('═'.repeat(100));
const names: Record<string, string> = Object.fromEntries(jobs.map((j) => [j.fileId, j.originalName]));
for (const s of [...built.scenes].sort((a, b) => a.proposedOrder - b.proposedOrder)) {
  console.log(`\n${s.proposedOrder}. [${s.kind}] "${s.proposedTitle}"  ${s.proposedDuration}s  conf ${s.confidence}`);
  console.log(`   canon: ${s.canonSegmentId ?? '(not tied to a canon segment)'}`);
  console.log(`   beats: ${s.storyBeatIds.join(', ') || '(none)'}`);
  for (const r of s.ranges) {
    console.log(`   cut:   ${names[r.sourceFileId] ?? r.sourceFileId}  ${r.startTime.toFixed(1)}s–${r.endTime.toFixed(1)}s`);
  }
}

// Locked segments with nothing behind them yet.
const canon = svc.canonCheck();
if (canon.absentLockedSegments.length) {
  console.log(`\nlocked EP01 segments with no candidate yet: ${canon.absentLockedSegments.length}`);
  for (const a of canon.advisories) console.log(`   ${a.found}`);
}

if (showTranscripts) {
  console.log('\n' + '═'.repeat(100));
  console.log('TRANSCRIPTS');
  console.log('═'.repeat(100));
  for (const r of rows) {
    console.log(`\n── ${r.name}  (${r.lines} lines)`);
    for (const t of r.transcript) console.log(`   ${t.startTime?.toFixed(1)}–${t.endTime?.toFixed(1)}  ${t.text}`);
  }
}
