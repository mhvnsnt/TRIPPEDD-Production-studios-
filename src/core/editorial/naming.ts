/**
 * Human names for footage.
 *
 * "VID_20260906_105329690.mp4" tells you nothing six months from now.
 * "Bag Sequence 2 — Reaction" tells you exactly what you are looking at.
 *
 * The original filename and the immutable source id are ALWAYS kept. This is a
 * catalog layer over the raw media, never a destructive rename: the raw folder
 * stays exactly as it came off the camera.
 */
import type { ObservationWithSource } from './reconciliation';
import type { ReconciledBeat, StoryBeat } from './types';

export type ShotType = 'WIDE' | 'CLOSE_UP' | 'MEDIUM' | 'REACTION' | 'INSERT' | 'UNKNOWN';

export interface ClipName {
  /** Immutable. Never changes, whatever the name becomes. */
  sourceFileId: string;
  originalFilename: string;
  /** "Bag Sequence 2 — Reaction" */
  displayName: string;
  /** "BAG_SEQUENCE" */
  scene: string;
  sceneLabel: string;
  /** Which clip within that scene, in physical order. */
  indexInScene: number;
  shotType: ShotType;
  /** Why it landed in this scene, so a wrong guess is arguable. */
  reason: string;
  confidence: number;
  durationSec?: number;
}

/** Title-cases a beat id like 'walk.bag_interruption' -> 'Bag Interruption'. */
function labelFor(beat: StoryBeat | undefined, fallback: string): string {
  if (beat) return beat.title;
  return fallback.replace(/[._-]+/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()).trim();
}

/**
 * Shot type from what the frames and audio actually show.
 * OpenCV motion and the amount of speech separate a reaction from a wide.
 */
function shotTypeOf(obs: ObservationWithSource[], fileId: string, seconds: number): { type: ShotType; why: string } {
  const mine = obs.filter((o) => o.sourceFileId === fileId);
  const summary = mine.find((o) => o.type === 'VISUAL_SUMMARY');
  const motion = Number((summary?.data as any)?.motionMean ?? NaN);
  const lines = mine.filter((o) => o.type === 'TRANSCRIPT_SEGMENT' && o.text).length;
  const words = mine.filter((o) => o.type === 'WORD_TIMING').length;

  if (seconds <= 6 && lines <= 1) {
    return { type: 'INSERT', why: `${seconds.toFixed(0)}s with almost no dialogue` };
  }
  if (seconds <= 12 && lines <= 2 && Number.isFinite(motion) && motion < 3) {
    return { type: 'REACTION', why: 'short, still, and barely any dialogue — reads as a reaction' };
  }
  if (Number.isFinite(motion) && motion > 12) {
    return { type: 'WIDE', why: `a lot of movement in frame (motion ${motion.toFixed(1)})` };
  }
  if (Number.isFinite(motion) && motion < 4 && words > 30) {
    return { type: 'CLOSE_UP', why: 'steady frame with sustained talking' };
  }
  return { type: 'MEDIUM', why: 'ordinary coverage' };
}

export interface NamingInput {
  /** sourceFileId -> original filename. */
  files: Record<string, string>;
  /** sourceFileId -> duration in seconds, where known. */
  durations?: Record<string, number>;
  observations: ObservationWithSource[];
  reconciled: ReconciledBeat[];
  beats: StoryBeat[];
}

/**
 * Assigns every clip to the scene its evidence best supports, then numbers the
 * clips within each scene in physical order.
 */
export function nameClips(input: NamingInput): ClipName[] {
  const { files, observations, reconciled, beats } = input;

  // Strongest beat per file, by how much evidence points at it.
  const claim = new Map<string, { beatId: string; score: number }>();
  for (const rb of reconciled) {
    if (rb.state === 'NOT_FOUND' || rb.state === 'MISSING_SOURCE_MEDIA') continue;
    const perFile = new Map<string, number>();
    for (const e of rb.evidence) perFile.set(e.sourceFileId, (perFile.get(e.sourceFileId) ?? 0) + 1);
    for (const [fileId, hits] of perFile) {
      // Weight by how confident the reconciliation was, so a vaguely-matched
      // beat cannot outrank a well-supported one on raw hit count.
      const score = hits * (0.5 + rb.confidence);
      const cur = claim.get(fileId);
      if (!cur || score > cur.score) claim.set(fileId, { beatId: rb.beatId, score });
    }
  }

  const rows: ClipName[] = [];
  for (const [fileId, originalFilename] of Object.entries(files)) {
    const c = claim.get(fileId);
    const beat = c ? beats.find((b) => b.id === c.beatId) : undefined;
    const sceneKey = beat ? beat.id.split('.').pop()!.toUpperCase() : 'UNSORTED';
    const seconds = input.durations?.[fileId] ?? 0;
    const shot = shotTypeOf(observations, fileId, seconds);

    rows.push({
      sourceFileId: fileId,
      originalFilename,
      displayName: '',            // filled in once clips are grouped and counted
      scene: sceneKey,
      sceneLabel: labelFor(beat, sceneKey),
      indexInScene: 0,
      shotType: shot.type,
      reason: beat
        ? `dialogue and on-screen evidence in this clip match "${beat.title}" (${shot.why})`
        : `no beat matched this clip yet (${shot.why})`,
      confidence: c ? Math.min(0.95, c.score / 6) : 0,
      durationSec: seconds || undefined,
    });
  }

  // Number within each scene by physical order, which for camera files is the
  // filename timestamp — the closest thing to when it was actually shot.
  const byScene = new Map<string, ClipName[]>();
  for (const r of rows) {
    if (!byScene.has(r.scene)) byScene.set(r.scene, []);
    byScene.get(r.scene)!.push(r);
  }

  for (const [, list] of byScene) {
    list.sort((a, b) => a.originalFilename.localeCompare(b.originalFilename));
    list.forEach((r, i) => {
      r.indexInScene = i + 1;
      const suffix =
        r.shotType === 'CLOSE_UP' ? ' — Close-Up' :
        r.shotType === 'WIDE' ? ' — Wide' :
        r.shotType === 'REACTION' ? ' — Reaction' :
        r.shotType === 'INSERT' ? ' — Insert' : '';
      r.displayName = list.length > 1
        ? `${r.sceneLabel} ${r.indexInScene}${suffix}`
        : `${r.sceneLabel}${suffix}`;
    });
  }

  return rows.sort((a, b) =>
    a.scene === b.scene ? a.indexInScene - b.indexInScene : a.scene.localeCompare(b.scene));
}

/** A catalog line the creator can read at a glance. */
export function catalogLine(c: ClipName): string {
  const dur = c.durationSec ? `${(c.durationSec / 60).toFixed(1)}m` : '';
  return `${c.displayName.padEnd(34)} ${dur.padStart(6)}  ${c.originalFilename}`;
}
