import { randomUUID } from 'crypto';

export type ComedySignalType = 'ESCALATION' | 'REACTION' | 'AWKWARD_SILENCE' | 'INTERRUPTION' | 'UNUSUAL_BEHAVIOR' | 'VISUAL_GAG' | 'DIALOGUE_DENSITY' | 'CALLBACK' | 'CONTINUITY' | 'CONTRADICTION' | 'SUBJECTIVITY_RUPTURE' | 'MUNDANE_BUTTON';
export interface ComedySignal { id: string; type: ComedySignalType; score: number; startTime?: number; endTime?: number; evidence: string; source: 'TRANSCRIPT' | 'SCENE' | 'VISUAL' | 'METADATA'; }
export interface GagCandidate { id: string; sourceFileId?: string; title: string; score: number; signals: ComedySignal[]; tags: string[]; callbackKeys: string[]; reviewState: 'MACHINE_SUGGESTED' | 'HUMAN_ACCEPTED' | 'HUMAN_REJECTED'; }
const clamp = (n: number) => Math.max(0, Math.min(1, n));

export function discoverComedy(input: { sourceFileId?: string; transcript?: { segments?: Array<{ start?: number; end?: number; text?: string }> } | null; scenes?: any[]; ocr?: string; }): GagCandidate[] {
  const candidates: GagCandidate[] = [];
  const segments = input.transcript?.segments ?? [];
  for (let i = 0; i < segments.length; i++) {
    const current = segments[i]; const text = String(current.text ?? '').trim(); if (!text) continue;
    const previous = segments[i - 1]; const gap = previous?.end != null && current.start != null ? current.start - previous.end : 0;
    const words = text.split(/\s+/).filter(Boolean).length; const signals: ComedySignal[] = [];
    if (gap >= 2) signals.push({ id: randomUUID(), type: 'AWKWARD_SILENCE', score: clamp(gap / 6), startTime: previous?.end, endTime: current.start, evidence: `${gap.toFixed(1)}s speech gap`, source: 'TRANSCRIPT' });
    if (words >= 35) signals.push({ id: randomUUID(), type: 'DIALOGUE_DENSITY', score: clamp(words / 70), startTime: current.start, endTime: current.end, evidence: `${words} words in one transcript segment`, source: 'TRANSCRIPT' });
    if (/[!?]{2,}|\b(what|why|no|wait|damn|shit|fuck)\b/i.test(text)) signals.push({ id: randomUUID(), type: 'REACTION', score: 0.62, startTime: current.start, endTime: current.end, evidence: text.slice(0, 180), source: 'TRANSCRIPT' });
    if (/\b(but|then|actually|except|instead|so now|turns out)\b/i.test(text)) signals.push({ id: randomUUID(), type: 'ESCALATION', score: 0.58, startTime: current.start, endTime: current.end, evidence: text.slice(0, 180), source: 'TRANSCRIPT' });
    if (/(interrupt|hold on|wait a second|let me|stop|shut up)/i.test(text)) signals.push({ id: randomUUID(), type: 'INTERRUPTION', score: 0.66, startTime: current.start, endTime: current.end, evidence: text.slice(0, 180), source: 'TRANSCRIPT' });
    if (/\b(doesn't|does not|isn't|is not|can't|cannot|impossible|normal|nothing happened|not a big deal|wasn't|was not)\b/i.test(text) && /\b(but|yet|still|actually|then|look|happened|saw|seeing)\b/i.test(text)) signals.push({ id: randomUUID(), type: 'CONTRADICTION', score: 0.72, startTime: current.start, endTime: current.end, evidence: `Possible character/world contradiction: ${text.slice(0, 180)}`, source: 'TRANSCRIPT' });
    if (/\b(dream|dreaming|trip|tripping|hallucinat|vision|seeing|saw|imagined|in my head|what the hell is happening|reality|world|everything changed)\b/i.test(text)) signals.push({ id: randomUUID(), type: 'SUBJECTIVITY_RUPTURE', score: 0.68, startTime: current.start, endTime: current.end, evidence: text.slice(0, 180), source: 'TRANSCRIPT' });
    if (/\b(just|anyway|whatever|never mind|it's fine|its fine|no big deal|wasn't shit|was not shit|nothing|forgot|lost|where is|can't find|cannot find)\b/i.test(text)) signals.push({ id: randomUUID(), type: 'MUNDANE_BUTTON', score: 0.56, startTime: current.start, endTime: current.end, evidence: `Possible anticlimactic/denial button: ${text.slice(0, 180)}`, source: 'TRANSCRIPT' });
    if (signals.length) candidates.push({ id: randomUUID(), sourceFileId: input.sourceFileId, title: text.length > 80 ? `${text.slice(0, 77)}...` : text, score: clamp(signals.reduce((sum, signal) => sum + signal.score, 0) / signals.length + (signals.length > 1 ? 0.12 : 0)), signals, tags: [...new Set(signals.map(signal => signal.type.toLowerCase()))], callbackKeys: extractCallbackKeys(text), reviewState: 'MACHINE_SUGGESTED' });
  }
  const ocr = String(input.ocr ?? '').trim();
  if (ocr) candidates.push({ id: randomUUID(), sourceFileId: input.sourceFileId, title: 'On-screen text / prop opportunity', score: 0.45, signals: [{ id: randomUUID(), type: 'VISUAL_GAG', score: 0.45, evidence: ocr.slice(0, 500), source: 'VISUAL' }], tags: ['ocr', 'visual-gag'], callbackKeys: extractCallbackKeys(ocr), reviewState: 'MACHINE_SUGGESTED' });
  return candidates.sort((a, b) => b.score - a.score);
}

function extractCallbackKeys(text: string): string[] {
  const normalized = text.toLowerCase().replace(/[^a-z0-9\s]/g, ' ');
  const words = normalized.split(/\s+/).filter(word => word.length >= 5);
  const stop = new Set(['there', 'their', 'about', 'would', 'could', 'should', 'because', 'really', 'thing', 'stuff', 'right', 'actually']);
  return [...new Set(words.filter(word => !stop.has(word)))].slice(0, 8);
}
