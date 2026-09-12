/**
 * WHEN each clip was recorded — the spine of the physical timeline.
 *
 * The camera stamps the recording start into the filename:
 *   VID_20260906_104742101.mp4  ->  2026-09-06 10:47:42.101
 * That is real evidence, it costs nothing to read, and it survives every ASR
 * failure in this project. The catalog treated it as an opaque id for the whole
 * of the build so far, which is why two separate trips to the same store looked
 * like one event: nothing in the pipeline knew they were four hours apart.
 *
 * Provenance is recorded, never assumed. A filename stamp is what the camera
 * wrote; a container creation_time is what the file system or the encoder
 * wrote; they can disagree, and when they do the difference is reported rather
 * than silently resolved.
 */

export type RecordedAtSource = 'FILENAME' | 'CONTAINER_METADATA' | 'UNKNOWN';

export interface RecordedAt {
  /** ISO instant the recording started, when it could be established. */
  at?: string;
  source: RecordedAtSource;
  /** The raw thing that was parsed, so a wrong read is visible. */
  raw?: string;
  /** Set when filename and container metadata disagree by more than a minute. */
  disagreement?: { filename: string; container: string; deltaSeconds: number };
}

/**
 * Camera filename conventions. Android (VID_/PXL_/IMG_), and the
 * YYYY-MM-DD HH.MM.SS shape other phones and screen recorders use.
 */
const PATTERNS: { re: RegExp; label: string }[] = [
  // VID_20260906_104742101 — trailing 3 digits are milliseconds
  { re: /(?:^|[^\d])(\d{8})[_-](\d{6})(\d{3})(?:[^\d]|$)/, label: 'YYYYMMDD_HHMMSSmmm' },
  // VID_20260906_104742 / PXL_20260906_104742
  { re: /(?:^|[^\d])(\d{8})[_-](\d{6})(?:[^\d]|$)/, label: 'YYYYMMDD_HHMMSS' },
  // 2026-09-06 10.47.42 / 2026-09-06_10-47-42
  { re: /(\d{4})-(\d{2})-(\d{2})[ _T](\d{2})[.\-:](\d{2})[.\-:](\d{2})/, label: 'YYYY-MM-DD HH.MM.SS' },
];

function iso(y: number, mo: number, d: number, h: number, mi: number, s: number, ms = 0): string | undefined {
  if (mo < 1 || mo > 12 || d < 1 || d > 31 || h > 23 || mi > 59 || s > 59) return undefined;
  const t = Date.UTC(y, mo - 1, d, h, mi, s, ms);
  const dt = new Date(t);
  // Reject a date the calendar rounded (31 February and friends).
  if (dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return undefined;
  return dt.toISOString();
}

/** Reads the recording instant out of a camera filename. */
export function recordedAtFromFilename(filename: string): RecordedAt {
  const base = filename.replace(/\.[A-Za-z0-9]+$/, '');

  for (const { re, label } of PATTERNS) {
    const m = base.match(re);
    if (!m) continue;

    let at: string | undefined;
    if (label.startsWith('YYYYMMDD')) {
      const [d8, hms, mmm] = [m[1], m[2], m[3]];
      at = iso(+d8.slice(0, 4), +d8.slice(4, 6), +d8.slice(6, 8),
               +hms.slice(0, 2), +hms.slice(2, 4), +hms.slice(4, 6), mmm ? +mmm : 0);
    } else {
      at = iso(+m[1], +m[2], +m[3], +m[4], +m[5], +m[6]);
    }
    if (at) return { at, source: 'FILENAME', raw: m[0].replace(/^[^\d]|[^\d]$/g, '') };
  }
  return { source: 'UNKNOWN' };
}

/**
 * How the camera's two clocks relate, MEASURED across the whole shoot rather
 * than assumed per file.
 *
 * A phone writes the filename in LOCAL time and the container creation_time in
 * UTC, and Android stamps creation_time when recording STOPS. So on this
 * footage every container time sits at filename + 5h + the clip's own duration.
 * Comparing the two naively reports a five-hour disagreement on every single
 * clip — nineteen alarms that are all wrong, and that would bury a real one.
 *
 * Calibrating on the set makes the residual meaningful: once the shared offset
 * and the end-stamp are accounted for, anything left over is a genuine
 * disagreement worth showing.
 */
export interface ClockCalibration {
  /** Whole-hour offset between filename local time and container UTC. */
  utcOffsetHours: number;
  /** True when creation_time is written at the END of the recording. */
  containerStampsEndOfRecording: boolean;
  /** Median leftover after both are accounted for. Near zero = the clocks agree. */
  residualSeconds: number;
  /** How many clips the calibration was derived from. */
  sampleSize: number;
}

const median = (xs: number[]): number => {
  if (!xs.length) return 0;
  const s = [...xs].sort((a, b) => a - b);
  const m = s.length >> 1;
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

/**
 * Derives the clock relationship from the shoot itself. Returns undefined when
 * there is not enough evidence — a guess about clocks is worse than no claim.
 */
export function calibrateClocks(
  samples: { filenameAt?: string; containerAt?: string; durationSec?: number }[]
): ClockCalibration | undefined {
  const usable = samples.filter((s) => s.filenameAt && s.containerAt);
  if (usable.length < 3) return undefined;

  const raw = usable.map((s) =>
    (new Date(s.containerAt!).getTime() - new Date(s.filenameAt!).getTime()) / 1000);

  // Test both hypotheses and keep whichever leaves the smaller spread. Whether
  // the stamp lands at the start or the end of the recording is a fact about
  // the camera, so it is measured, not assumed.
  const atStart = raw;
  const atEnd = usable.map((s, i) => raw[i] - (s.durationSec ?? 0));
  const spread = (xs: number[]) => {
    const m = median(xs);
    return median(xs.map((x) => Math.abs(x - m)));
  };
  const useEnd = spread(atEnd) < spread(atStart);
  const deltas = useEnd ? atEnd : atStart;

  const offsetHours = Math.round(median(deltas) / 3600);
  const residual = median(deltas.map((d) => Math.abs(d - offsetHours * 3600)));

  return {
    utcOffsetHours: -offsetHours, // container = local + (-offset) => local is UTC+offsetHours behind
    containerStampsEndOfRecording: useEnd,
    residualSeconds: Math.round(residual),
    sampleSize: usable.length,
  };
}

/**
 * Combines the filename stamp with a container creation_time. The filename wins
 * — a file copied through Drive can pick up a new container time, while the name
 * the camera wrote travels with it — but a real disagreement is reported.
 *
 * Pass the calibration from calibrateClocks() so the shared timezone offset and
 * end-of-recording stamp are subtracted before anything is called a
 * disagreement.
 */
export function resolveRecordedAt(
  filename: string,
  containerCreationTime?: string,
  opts: { durationSec?: number; calibration?: ClockCalibration } = {}
): RecordedAt {
  const fromName = recordedAtFromFilename(filename);
  const container = containerCreationTime ? new Date(containerCreationTime) : undefined;
  const containerOk = container && !Number.isNaN(container.getTime());

  if (!fromName.at) {
    return containerOk
      ? { at: container!.toISOString(), source: 'CONTAINER_METADATA', raw: containerCreationTime }
      : { source: 'UNKNOWN' };
  }
  if (!containerOk) return fromName;

  const cal = opts.calibration;
  const expectedShiftSec = cal
    ? (-cal.utcOffsetHours) * 3600 + (cal.containerStampsEndOfRecording ? (opts.durationSec ?? 0) : 0)
    : 0;

  const deltaSeconds = Math.round(
    Math.abs(container!.getTime() - new Date(fromName.at).getTime() - expectedShiftSec * 1000) / 1000);

  return deltaSeconds > 60
    ? { ...fromName, disagreement: { filename: fromName.at, container: container!.toISOString(), deltaSeconds } }
    : fromName;
}

export interface ClipTiming {
  fileId: string;
  originalName: string;
  recordedAt: RecordedAt;
  durationSec?: number;
}

export interface TimelineEntry extends ClipTiming {
  /** Position in the day, by recording time. */
  physicalIndex: number;
  /** Seconds between the END of the previous clip and the START of this one. */
  gapFromPreviousSec?: number;
  /** Clips separated by a long gap are different events, not one long scene. */
  sessionId: string;
}

/** Gap that ends a session. Ten minutes of not filming is a different moment. */
export const DEFAULT_SESSION_GAP_SEC = 10 * 60;

/**
 * The day, in the order it was actually recorded, split into sessions by real
 * gaps. This is what separates two visits to the same store: not their content,
 * which is nearly identical, but the four hours between them.
 *
 * Clips with no establishable time keep their input order and are placed at the
 * end in a session of their own, rather than being given a time they don't have.
 */
export function buildPhysicalTimeline(
  clips: ClipTiming[],
  sessionGapSec: number = DEFAULT_SESSION_GAP_SEC
): { timeline: TimelineEntry[]; undated: ClipTiming[] } {
  const dated = clips.filter((c) => c.recordedAt.at);
  const undated = clips.filter((c) => !c.recordedAt.at);

  dated.sort((a, b) => a.recordedAt.at!.localeCompare(b.recordedAt.at!));

  const timeline: TimelineEntry[] = [];
  let session = 0;
  let prevEndMs: number | undefined;

  dated.forEach((c, i) => {
    const startMs = new Date(c.recordedAt.at!).getTime();
    const gap = prevEndMs === undefined ? undefined : Math.round((startMs - prevEndMs) / 1000);
    if (gap !== undefined && gap > sessionGapSec) session++;

    timeline.push({
      ...c,
      physicalIndex: i,
      gapFromPreviousSec: gap,
      sessionId: `S${String(session + 1).padStart(2, '0')}`,
    });
    prevEndMs = startMs + Math.round((c.durationSec ?? 0) * 1000);
  });

  return { timeline, undated };
}

/** Clips grouped by session, for reasoning about one moment at a time. */
export function sessionsOf(timeline: TimelineEntry[]): { sessionId: string; clips: TimelineEntry[]; startedAt: string; endedAt: string }[] {
  const by = new Map<string, TimelineEntry[]>();
  for (const t of timeline) {
    if (!by.has(t.sessionId)) by.set(t.sessionId, []);
    by.get(t.sessionId)!.push(t);
  }
  return [...by.entries()].map(([sessionId, clips]) => {
    const last = clips[clips.length - 1];
    return {
      sessionId, clips,
      startedAt: clips[0].recordedAt.at!,
      endedAt: new Date(new Date(last.recordedAt.at!).getTime() + (last.durationSec ?? 0) * 1000).toISOString(),
    };
  });
}
