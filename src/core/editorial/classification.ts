/**
 * Editorial classification of real source material.
 *
 * Raw footage is full of "the camera's rolling", "cut", setup chatter and dead
 * air. None of it is deleted: the physical timeline keeps every second. This
 * layer only proposes how each stretch should be TREATED in an audience-facing
 * cut, and every proposal is a candidate a human can overturn.
 *
 * A phrase is a signal, not a verdict — "let's go" is a camera cue in one clip
 * and real dialogue in another, so ambiguous hits are marked UNCERTAIN rather
 * than silently cut.
 */
import type { MachineObservation } from '../analysis/analyzers';
import type { EditorialClassification } from './types';

interface Rule {
  classification: EditorialClassification;
  phrases: string[];
  /** Phrases so specific they are almost never real dialogue. */
  unambiguous?: boolean;
}

const RULES: Rule[] = [
  {
    classification: 'CAMERA_DIRECTION',
    unambiguous: true,
    phrases: [
      "camera's rolling", 'camera is rolling', 'we are rolling', "we're rolling",
      'rolling', 'stop the camera', 'stop recording', 'cut the camera',
      'is it recording', 'are you recording', 'the recording is going',
      'start recording', 'turn it off', 'turn the camera off',
    ],
  },
  {
    classification: 'SETUP',
    phrases: ['hold on', 'wait a second', 'let me get', 'one second', 'give me a sec', 'ready', 'you ready'],
  },
  {
    classification: 'RESET',
    phrases: ['from the top', 'again', 'do it again', 'one more time', 'run it back'],
  },
  {
    classification: 'TECHNICAL_INTERRUPTION',
    phrases: ['battery', 'memory card', 'it died', 'no signal', 'the mic', 'audio is', 'i lost it'],
  },
  {
    classification: 'OUTTAKE',
    phrases: ['my bad', 'i messed up', 'scratch that', 'sorry sorry', 'i forgot my line'],
  },
];

/**
 * Phrases that read as a camera cue but are common real speech. A bare "cut" is
 * the classic case: it is the standard call to stop a take, and also an
 * ordinary word ("cut it out", "a cut on my hand"). Treating it as an
 * unambiguous artifact would silently drop real dialogue, so it is flagged for
 * a human instead of acted on.
 */
const AMBIGUOUS = ["let's go", 'lets go', 'go ahead', 'here we go', 'alright', 'cut', 'stop', 'okay go'];

export interface ClassifiedSegment {
  observationId: string;
  sourceFileId: string;
  startTime: number;
  endTime: number;
  text: string;
  classification: EditorialClassification;
  reason: string;
  /** True when the phrase could legitimately be program dialogue. */
  ambiguous: boolean;
  matchedPhrase?: string;
}

function norm(s: string): string {
  return s.toLowerCase().replace(/[^\w\s']/g, ' ').replace(/\s+/g, ' ').trim();
}

/** Dead air: a gap between consecutive speech longer than this reads as a hole. */
export const DEAD_AIR_SECONDS = 4;

export function classifySegment(
  o: MachineObservation & { sourceFileId: string }
): ClassifiedSegment | undefined {
  if (o.type !== 'TRANSCRIPT_SEGMENT' || !o.text) return undefined;
  const text = norm(o.text);
  const base = {
    observationId: o.id, sourceFileId: o.sourceFileId,
    startTime: o.startTime ?? 0, endTime: o.endTime ?? (o.startTime ?? 0),
    text: o.text,
  };

  for (const rule of RULES) {
    for (const p of rule.phrases) {
      if (!text.includes(norm(p))) continue;
      return {
        ...base,
        classification: rule.classification,
        reason: `matched production-artifact phrase "${p}"`,
        ambiguous: !rule.unambiguous,
        matchedPhrase: p,
      };
    }
  }

  for (const p of AMBIGUOUS) {
    if (text.includes(norm(p))) {
      return {
        ...base,
        classification: 'UNCERTAIN',
        reason: `"${p}" can be a camera cue or real dialogue — needs a human`,
        ambiguous: true,
        matchedPhrase: p,
      };
    }
  }

  return { ...base, classification: 'PROGRAM_CONTENT', reason: 'no production-artifact signal', ambiguous: false };
}

export function classifyAll(
  observations: (MachineObservation & { sourceFileId: string })[]
): ClassifiedSegment[] {
  const speech = observations
    .filter((o) => o.type === 'TRANSCRIPT_SEGMENT' && o.text)
    .sort((a, b) => (a.startTime ?? 0) - (b.startTime ?? 0));

  const out: ClassifiedSegment[] = [];
  for (const o of speech) {
    const c = classifySegment(o);
    if (c) out.push(c);
  }

  // Gaps between speech become explicit DEAD_AIR candidates, per source file.
  const byFile = new Map<string, ClassifiedSegment[]>();
  for (const c of out) (byFile.get(c.sourceFileId) ?? byFile.set(c.sourceFileId, []).get(c.sourceFileId)!).push(c);

  const gaps: ClassifiedSegment[] = [];
  for (const [fileId, segs] of byFile) {
    const ordered = [...segs].sort((a, b) => a.startTime - b.startTime);
    for (let i = 1; i < ordered.length; i++) {
      const gap = ordered[i].startTime - ordered[i - 1].endTime;
      if (gap >= DEAD_AIR_SECONDS) {
        gaps.push({
          observationId: `deadair_${fileId}_${i}`,
          sourceFileId: fileId,
          startTime: ordered[i - 1].endTime,
          endTime: ordered[i].startTime,
          text: '',
          classification: 'DEAD_AIR',
          reason: `${gap.toFixed(1)}s with no detected speech`,
          ambiguous: true,
        });
      }
    }
  }

  return [...out, ...gaps];
}
