/**
 * Turn the creator's plain words into permanent source→scene mappings.
 *
 * He is watching the footage and will say things like:
 *     104742101 = cigar store
 *     110016345 = walk
 *     122211926 = bag argument
 *     160715990 != joe
 * That should cost him one line per clip, not a form. This reads that shorthand,
 * resolves the clip by any unambiguous fragment of its filename, resolves the
 * scene by name against the EP01 canon, and writes a HUMAN_CONFIRMED mapping
 * that no autonomous pass is allowed to overwrite.
 *
 * Nothing is renamed. Ever. The Drive file keeps the name the camera gave it;
 * this only records what the clip IS.
 *
 *   npx tsx scripts/confirm_clips.ts "104742101 = cigar store" "110016345 = walk"
 *   npx tsx scripts/confirm_clips.ts --file mappings.txt
 *   npx tsx scripts/confirm_clips.ts --list        # show the catalog
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { SourceCatalog, type SourceClipEntry } from '../src/core/editorial/sourceCatalog';
import { EPISODE_01, lockedOrder } from '../src/core/canon/episode01';
import { recordedAtFromFilename, calibrateClocks, resolveRecordedAt, buildPhysicalTimeline } from '../src/core/analysis/recordedAt';

const STORE = path.join(process.cwd(), '.trippedd_catalog.json');
const FOOTAGE = process.env.TRIPPEDD_FOOTAGE ?? 'footage';

/** Everything a creator might reasonably call a segment. */
const ALIASES: Record<string, string[]> = {
  EP01_COLD_OPEN: ['cold open', 'open', 'opening', 'teaser'],
  EP01_MOTEL: ['motel', 'room', 'hotel', 'motel room', 'chilling', 'motel clerk', 'clerk', 'front desk'],
  EP01_SHUMAFIED: ['shumafied', 'shuma', 'the pack', 'device'],
  EP01_SHUMAFIED_LETDOWN: ['letdown', 'disappointment', 'not doing shit', 'cigar setup', 'setup', 'decision'],
  EP01_LUCK_OF_THE_IRISH: ['luck of the irish', 'irish', 'commercial', 'ad', 'green'],
  EP01_CIGARS: ['cigars', 'cigar', 'cigar store', 'store', 'walk', 'walking', 'the walk', 'cigar trip', 'trip', 'shop'],
  EP01_BAG_SEQUENCE: ['bag', 'bag sequence', 'bag argument', 'bag interruption', 'bag return', 'argument'],
  EP01_JOE: ['joe', 'joe encounter', 'tic tacs', 'prayer'],
  EP01_TV: ['tv', 'television', 'harry potter', 'nickelodeon', 'channel'],
  EP01_CLOTHED_AND_CONFUSED: ['clothed and confused', 'clothed', 'survival', 'naked and afraid'],
  EP01_SMOKING: ['smoking', 'smoke', 'hanging out', 'hanging', 'closing'],
  // Not locked to a position, but real content the creator will want to assign.
  // Leaving these unassignable is how a Goodville gag gets lost.
  GOODVILLE: ['goodville', 'goodville geography', 'goodville cartoon', 'nashville', '45 minutes'],
  INTERSTITIALS: ['interstitial', 'transition', 'trippy', 'liminal'],
  UNUSED: ['unused', 'nothing', 'junk', 'discard', 'not usable', 'b-roll', 'broll'],
};

const EXTRA_TARGETS = ['GOODVILLE', 'INTERSTITIALS', 'UNUSED'];

function resolveSegment(text: string): { id?: string; ambiguous?: string[] } {
  const t = text.trim().toLowerCase();
  const upper = text.trim().toUpperCase();
  if (EPISODE_01.some((s) => s.id === upper) || EXTRA_TARGETS.includes(upper)) return { id: upper };

  // Longest alias first, so "cigar store" beats "store" and "bag argument"
  // beats "bag" — a short alias must never swallow a more specific one.
  const hits = Object.entries(ALIASES)
    .flatMap(([id, aliases]) => aliases.filter((a) => t === a || t.includes(a)).map((a) => ({ id, a })))
    .sort((x, y) => y.a.length - x.a.length);
  if (!hits.length) return {};
  const best = hits[0];
  const rivals = [...new Set(hits.filter((h) => h.a.length === best.a.length).map((h) => h.id))];
  return rivals.length > 1 ? { ambiguous: rivals } : { id: best.id };
}

// ── build (or reload) the catalog from what is on disk ───────────────────────
const catalog: SourceCatalog = existsSync(STORE)
  ? SourceCatalog.fromJSON(JSON.parse(readFileSync(STORE, 'utf8')))
  : new SourceCatalog();

if (existsSync(FOOTAGE)) {
  const files = readdirSync(FOOTAGE).filter((f) => /\.(mp4|mov|m4v|mkv|avi)$/i.test(f));
  const probed = files.map((name) => {
    let duration: number | undefined, creationTime: string | undefined;
    try {
      const out = execFileSync('ffprobe', ['-v', 'error', '-show_entries',
        'format=duration:format_tags=creation_time', '-of', 'json', path.join(FOOTAGE, name)], { encoding: 'utf8' });
      const f = JSON.parse(out).format ?? {};
      duration = f.duration ? Number(f.duration) : undefined;
      creationTime = f.tags?.creation_time;
    } catch { /* a clip we cannot probe still gets catalogued, just without timing */ }
    return { name, duration, creationTime };
  });

  const cal = calibrateClocks(probed.map((p) => ({
    filenameAt: recordedAtFromFilename(p.name).at, containerAt: p.creationTime, durationSec: p.duration,
  })));
  const { timeline } = buildPhysicalTimeline(probed.map((p) => ({
    fileId: p.name.replace(/\.[^.]+$/, ''), originalName: p.name,
    recordedAt: resolveRecordedAt(p.name, p.creationTime, { durationSec: p.duration, calibration: cal }),
    durationSec: p.duration,
  })));

  for (const t of timeline) {
    const sheet = path.join('public', 'contact', `${t.fileId}.jpg`);
    catalog.register({
      sourceId: t.fileId,
      originalFilename: t.originalName,
      recordedAt: t.recordedAt.at,
      sessionId: t.sessionId,
      durationSec: t.durationSec,
      contactSheet: existsSync(sheet) ? sheet : undefined,
    } as Partial<SourceClipEntry> as any);
  }
}

const save = () => writeFileSync(STORE, JSON.stringify(catalog.toJSON(), null, 2));

// ── listing ──────────────────────────────────────────────────────────────────
if (process.argv.includes('--list') || process.argv.length <= 2) {
  const segName = (id?: string) => id ? (EPISODE_01.find((s) => s.id === id)?.name ?? id) : '';
  console.log('\nSOURCE CATALOG   (the Drive files are NOT renamed — open them by ORIGINAL FILENAME)\n');
  console.log('  time     dur    original filename              assignment                    status');
  console.log('  ' + '─'.repeat(104));
  for (const e of catalog.all()) {
    const t = e.recordedAt ? new Date(e.recordedAt).toISOString().slice(11, 16) : '  ?  ';
    const d = e.durationSec ? `${Math.floor(e.durationSec / 60)}:${String(Math.round(e.durationSec % 60)).padStart(2, '0')}` : ' ? ';
    console.log(`  ${t}  ${d.padStart(5)}  ${e.originalFilename.padEnd(30)} ` +
      `${(segName(e.canonSegmentId) || '—').padEnd(29)} ${e.assignmentStatus}`);
    if (e.displayName) console.log(`                   CATALOG DISPLAY NAME: ${e.displayName}   (DRIVE FILE RENAMED: NO)`);
    if (e.rejectedSegmentIds.length) console.log(`                   ruled out: ${e.rejectedSegmentIds.join(', ')}`);
  }
  const confirmed = catalog.confirmedMappings().length;
  console.log(`\n  ${confirmed}/${catalog.all().length} confirmed by the creator.`);
  const covered = new Set(catalog.confirmedMappings().map((m) => m.canonSegmentId));
  const missing = lockedOrder().filter((id) => !covered.has(id));
  if (missing.length) console.log(`  locked segments with no confirmed clip: ${missing.map(segName).join(', ')}`);
  save();
  process.exit(0);
}

// ── applying confirmations ───────────────────────────────────────────────────
const fileArg = process.argv.indexOf('--file');
const lines = fileArg >= 0
  ? readFileSync(process.argv[fileArg + 1], 'utf8').split('\n')
  : process.argv.slice(2).filter((a) => !a.startsWith('--'));

let applied = 0, failed = 0;
for (const raw of lines) {
  const line = raw.split('#')[0].trim();
  if (!line) continue;

  const negative = line.includes('!=');
  const [lhs, rhs] = line.split(negative ? '!=' : '=').map((x) => x?.trim());
  if (!lhs || !rhs) { console.log(`  ? cannot read "${line}" — expected "<clip> = <scene>"`); failed++; continue; }

  const matches = catalog.all().filter((e) =>
    e.sourceId.includes(lhs) || e.originalFilename.includes(lhs));
  if (matches.length !== 1) {
    console.log(matches.length
      ? `  ? "${lhs}" matches ${matches.length} clips: ${matches.map((m) => m.originalFilename).join(', ')}`
      : `  ? no clip matching "${lhs}"`);
    failed++; continue;
  }

  const { id, ambiguous } = resolveSegment(rhs);
  if (!id) {
    console.log(ambiguous
      ? `  ? "${rhs}" could be ${ambiguous.join(' or ')} — name one`
      : `  ? no EP01 segment matching "${rhs}"`);
    failed++; continue;
  }

  const clip = matches[0];
  if (negative) {
    catalog.reject(clip.sourceId, id);
    console.log(`  ✗ ${clip.originalFilename}  is NOT  ${id}   (remembered, the guess cannot come back)`);
  } else {
    catalog.confirm(clip.sourceId, id, { note: `creator: "${line}"` });
    console.log(`  ✓ ${clip.originalFilename}  =  ${id}   HUMAN_CONFIRMED`);
  }
  applied++;
}

save();
console.log(`\n${applied} applied, ${failed} not understood. Catalog: ${STORE}`);
console.log('Drive files were NOT renamed. Original filenames are unchanged.');
