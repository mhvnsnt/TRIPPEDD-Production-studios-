/**
 * Explains a cut in the creator's language, not the machine's.
 *
 * Every sentence is derived from the edit that actually exists — the real
 * ranges, the real removals, the real transcript. Nothing here is a template
 * describing what the editor might have done.
 */
import type { EditorialSceneCandidate } from './types';
import type { ObservationWithSource } from './reconciliation';

export interface SceneExplanation {
  /** One line: what this scene is. */
  headline: string;
  /** "What I did" — the decisions, in order. */
  did: string[];
  /** "What I'm not sure about" — stated, never buried. */
  unsure: string[];
  /** Rough shape of the cut for the creator to skim. */
  shots: { label: string; seconds: number; from: string; line?: string }[];
}

const secs = (n: number) => `${n.toFixed(1)}s`;

function lineIn(obs: ObservationWithSource[], fileId: string, start: number, end: number): string | undefined {
  const hits = obs.filter((o) =>
    o.type === 'TRANSCRIPT_SEGMENT' && o.text && o.sourceFileId === fileId &&
    (o.endTime ?? 0) > start && (o.startTime ?? 0) < end);
  if (!hits.length) return undefined;
  // The longest line in the range is the one that characterises it.
  return hits.sort((a, b) => (b.text?.length ?? 0) - (a.text?.length ?? 0))[0].text?.trim();
}

export function explainScene(
  scene: EditorialSceneCandidate,
  observations: ObservationWithSource[]
): SceneExplanation {
  const did: string[] = [];
  const unsure: string[] = [];

  const total = scene.proposedDuration;
  const clips = new Set(scene.ranges.map((r) => r.sourceFileId));

  const opening = scene.ranges[0];
  const openingLine = opening && lineIn(observations, opening.sourceFileId, opening.startTime, opening.endTime);

  const headline =
    `${scene.proposedTitle} — ${secs(total)} cut from ${scene.ranges.length} piece${scene.ranges.length === 1 ? '' : 's'}` +
    ` of ${clips.size} clip${clips.size === 1 ? '' : 's'}.`;

  // Why it starts where it starts.
  if (opening) {
    did.push(
      openingLine
        ? `I started on "${openingLine.slice(0, 70)}" because it gives the scene a clean way in.`
        : `I started at ${secs(opening.startTime)} in ${opening.sourceFileId}, just before the action picks up.`
    );
  }

  // What got taken out, in the creator's terms.
  const chatter = scene.excludedMaterial.filter((e) =>
    e.classification === 'CAMERA_DIRECTION' || e.classification === 'SETUP' || e.classification === 'RESET');
  if (chatter.length) {
    const quotes = chatter.map((c) => c.excerpt?.trim()).filter(Boolean).slice(0, 2);
    did.push(
      `I took out the camera and setup talk${quotes.length ? ` (${quotes.map((q) => `"${q!.slice(0, 45)}"`).join(', ')})` : ''}` +
      ` — it is still in your raw footage, just not in the cut.`
    );
  }
  const deadAir = scene.excludedMaterial.filter((e) => e.classification === 'DEAD_AIR');
  if (deadAir.length) {
    const saved = deadAir.reduce((a, e) => a + (e.range.endTime - e.range.startTime), 0);
    did.push(`I pulled ${secs(saved)} of dead air out so it does not drag.`);
  }
  const other = scene.excludedMaterial.filter((e) => !chatter.includes(e) && !deadAir.includes(e));
  for (const o of other.slice(0, 2)) {
    did.push(`I left out ${o.excerpt ? `"${o.excerpt.slice(0, 45)}"` : 'a section'} — ${o.reason}.`);
  }

  // Why it's in this order.
  if (scene.ranges.length > 1) {
    did.push(`I cut it into ${scene.ranges.length} pieces so it moves instead of sitting on one long take.`);
  }
  if (scene.reorderReason) {
    did.push(`I put this scene earlier than it was actually filmed because it plays better here. The original filming order is still on record.`);
  }

  // The ending.
  const last = scene.ranges[scene.ranges.length - 1];
  const lastLine = last && lineIn(observations, last.sourceFileId, last.startTime, last.endTime);
  if (last) {
    did.push(
      lastLine
        ? `I ended on "${lastLine.slice(0, 70)}" — it gives the scene a button.`
        : `I ended at ${secs(last.endTime)} so it finishes on the action rather than trailing off.`
    );
  }

  // Honest uncertainty.
  if (scene.confidence < 0.5) {
    unsure.push(`I am not very confident this is a scene on its own — the footage supporting it is thin.`);
  }
  for (const a of scene.chronologyAssumptions.slice(0, 3)) unsure.push(a.statement);
  for (const l of scene.evidenceLimitations ?? []) {
    unsure.push(`${l.tool} could not run on this footage, so ${l.effect}.`);
  }
  if (scene.missingEvidence.length) {
    unsure.push(`Some of what you described for this beat did not turn up in the footage.`);
  }
  const lowConfWords = observations.filter((o) =>
    o.type === 'WORD_TIMING' && typeof (o.data as any)?.score === 'number' && (o.data as any).score < 0.4 &&
    scene.ranges.some((r) => r.sourceFileId === o.sourceFileId && (o.startTime ?? 0) >= r.startTime && (o.endTime ?? 0) <= r.endTime));
  if (lowConfWords.length) {
    unsure.push(
      `A few words in this scene were hard to hear (${lowConfWords.slice(0, 4).map((w) => `"${w.text}"`).join(', ')}), so the transcript may be wrong there.`
    );
  }

  const shots = scene.ranges.map((r, i) => ({
    label: i === 0 ? 'Opens' : i === scene.ranges.length - 1 ? 'Ends' : `Shot ${i + 1}`,
    seconds: Number((r.endTime - r.startTime).toFixed(1)),
    from: `${r.sourceFileId} @ ${secs(r.startTime)}`,
    line: lineIn(observations, r.sourceFileId, r.startTime, r.endTime)?.slice(0, 80),
  }));

  return { headline, did, unsure, shots };
}
