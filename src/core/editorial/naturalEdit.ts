/**
 * Natural-language editing.
 *
 * The creator types what they want in their own words and the cut changes.
 * "Cut that camera shit", "hold on her longer", "start with the argument" —
 * these become real changes to real timestamps, then the scene is re-rendered.
 *
 * When an instruction is not understood it says so plainly and changes nothing.
 * Silently doing something adjacent is worse than admitting it did not follow.
 */
import type { EditorialSceneCandidate, SourceRange, EditorialExclusion } from './types';
import type { ObservationWithSource } from './reconciliation';

export type EditIntentKind =
  | 'SHORTEN' | 'LENGTHEN' | 'HOLD_LONGER' | 'TIGHTEN_ENDING'
  | 'CUT_CHATTER' | 'KEEP_MATERIAL' | 'REMOVE_PHRASE'
  | 'START_WITH' | 'END_WITH' | 'REORDER'
  | 'ALTERNATE' | 'APPROVE' | 'REJECT' | 'UNKNOWN';

export interface EditIntent {
  kind: EditIntentKind;
  /** What the creator typed, kept verbatim for the record. */
  raw: string;
  seconds?: number;
  fraction?: number;
  phrase?: string;
  where?: 'start' | 'end' | 'before' | 'after';
  targetScene?: string;
  /** Why the parser read it this way, so a wrong read is visible. */
  reading: string;
}

const num = (s: string): number | undefined => {
  const w: Record<string, number> = { a: 1, one: 1, two: 2, three: 3, four: 4, five: 5, ten: 10, fifteen: 15, twenty: 20, thirty: 30 };
  const m = s.match(/(\d+(?:\.\d+)?)\s*(?:second|sec|s\b)/i);
  if (m) return Number(m[1]);
  const wm = s.match(/\b(a|one|two|three|four|five|ten|fifteen|twenty|thirty)\s+(?:more\s+)?second/i);
  if (wm) return w[wm[1].toLowerCase()];
  const bare = s.match(/\bcut\s+(\d+(?:\.\d+)?)\b/i);
  if (bare) return Number(bare[1]);
  return undefined;
};

function quoted(s: string): string | undefined {
  const q = s.match(/["“”'‘’]([^"“”'‘’]{2,})["“”'‘’]/);
  if (q) return q[1].trim();
  return undefined;
}

/**
 * Reads the instruction. Deliberately rule-based: the creator should get the
 * same result for the same words every time, and an unrecognised phrase should
 * be reported rather than guessed at.
 */
export function parseInstruction(input: string): EditIntent {
  const t = input.trim();
  const s = t.toLowerCase();
  const raw = t;

  if (/^(that'?s good|good|perfect|yes|yep|approve|lock it|keep it|ship it)\b/.test(s)) {
    return { kind: 'APPROVE', raw, reading: 'you approved the scene' };
  }
  if (/^(no|nah|reject|scrap|throw (it|this) (out|away)|delete this)\b/.test(s) && !/start|begin|use|put/.test(s)) {
    return { kind: 'REJECT', raw, reading: 'you rejected this version of the scene' };
  }
  if (/(another|different|other)\s+(version|cut|take|option)|try again|show me another/.test(s)) {
    return { kind: 'ALTERNATE', raw, reading: 'you want a different version of this scene' };
  }

  // Production chatter — the creator's own phrasing included.
  if (/(camera|production)\s*(shit|chatter|talk|stuff|bullshit)|cut the camera|camera'?s rolling|stop the camera|rolling bit|setup (talk|chatter)/.test(s)) {
    return { kind: 'CUT_CHATTER', raw, reading: 'remove the camera/production talk from the cut' };
  }
  if (/(leave|keep|put back|restore)\b.*(silence|pause|quiet|that in|it in|that bit)/.test(s)) {
    return { kind: 'KEEP_MATERIAL', raw, phrase: quoted(t), reading: 'put removed material back into the cut' };
  }

  if (/(hold|stay|linger|sit)\b.*(longer|more)|longer on|more time on/.test(s)) {
    const where: 'start' | 'end' = /begin|start|opening|first/.test(s) ? 'start' : 'end';
    return {
      kind: 'HOLD_LONGER', raw, seconds: num(s) ?? 1.5, where,
      reading: `hold the ${where === 'start' ? 'opening' : 'final'} shot about ${num(s) ?? 1.5}s longer`,
    };
  }

  if (/(shorter|tighten|trim|cut it down|too long|speed it up|snappier)/.test(s) || /^cut \d+/.test(s)) {
    const sec = num(s);
    return {
      kind: 'SHORTEN', raw, seconds: sec, fraction: sec ? undefined : 0.15,
      reading: sec ? `take about ${sec}s out` : 'tighten the scene by roughly 15%',
    };
  }
  if (/(longer|extend|more room|let it breathe|slow it down)/.test(s) && !/hold/.test(s)) {
    return { kind: 'LENGTHEN', raw, seconds: num(s) ?? 1.5, reading: `give the scene about ${num(s) ?? 1.5}s more room` };
  }
  if (/(ending|end|last bit|button|finish)\b.*(harder|stronger|punch|hit|tighter|snappier)/.test(s)) {
    return { kind: 'TIGHTEN_ENDING', raw, reading: 'make the ending land harder by cutting the trailing slack' };
  }

  // "start with her walking in" / "begin on the argument"
  const startM = t.match(/(?:start|begin|open)\s+(?:with|on|from)\s+(.+)/i);
  if (startM) {
    return { kind: 'START_WITH', raw, phrase: (quoted(t) ?? startM[1]).replace(/[.!?]+$/, '').trim(), where: 'start',
      reading: `begin the scene at "${(quoted(t) ?? startM[1]).trim()}"` };
  }
  const endM = t.match(/(?:end|finish|close)\s+(?:with|on)\s+(.+)/i);
  if (endM) {
    return { kind: 'END_WITH', raw, phrase: (quoted(t) ?? endM[1]).replace(/[.!?]+$/, '').trim(), where: 'end',
      reading: `end the scene on "${(quoted(t) ?? endM[1]).trim()}"` };
  }

  // "cut the bit where he says X" / "take out X"
  const rmM = t.match(/(?:cut|remove|take out|drop|lose)\s+(?:the\s+)?(?:bit|part|line|section)?\s*(?:where|when|about)?\s*(.+)/i);
  if (rmM && !/chatter|camera/.test(s)) {
    const phrase = (quoted(t) ?? rmM[1]).replace(/[.!?]+$/, '').trim();
    if (phrase.length > 2) {
      return { kind: 'REMOVE_PHRASE', raw, phrase, reading: `remove the part containing "${phrase}"` };
    }
  }

  // "put this before the motel scene" / "move it after Joe"
  const ordM = t.match(/(?:put|move|place)\s+(?:this|it|that|the\s+\w+(?:\s+\w+)?)\s+(before|after|first|last)\s*(.*)/i);
  if (ordM) {
    const where = /first/i.test(ordM[1]) ? 'before' : /last/i.test(ordM[1]) ? 'after' : (ordM[1].toLowerCase() as 'before' | 'after');
    return { kind: 'REORDER', raw, where, targetScene: ordM[2]?.replace(/[.!?]+$/, '').trim() || undefined,
      reading: `move this scene ${ordM[1].toLowerCase()}${ordM[2] ? ` ${ordM[2].trim()}` : ''}` };
  }
  if (/(put|move)\s+the\s+(.+?)\s+(first|earlier)/i.test(t)) {
    const m = t.match(/(put|move)\s+the\s+(.+?)\s+(first|earlier)/i)!;
    return { kind: 'START_WITH', raw, phrase: m[2].trim(), where: 'start', reading: `lead with the ${m[2].trim()}` };
  }

  return {
    kind: 'UNKNOWN', raw,
    reading: 'I did not understand that one — nothing was changed',
  };
}

// ------------------------------------------------------------------ applying

export interface EditContext {
  observations: ObservationWithSource[];
  /** Alternative material available but not currently in the cut. */
  excluded: EditorialExclusion[];
}

export interface EditOutcome {
  changed: boolean;
  ranges: SourceRange[];
  excluded: EditorialExclusion[];
  /** Plain-English account of what actually changed. */
  summary: string;
  /** Set when the instruction was understood but could not be carried out. */
  problem?: string;
}

const dur = (rs: SourceRange[]) => rs.reduce((a, r) => a + (r.endTime - r.startTime), 0);
const clone = (rs: SourceRange[]) => rs.map((r) => ({ ...r, derivedFromObservationIds: [...r.derivedFromObservationIds] }));

/** Finds where a phrase is actually spoken, so "start with X" lands on real audio. */
function findPhrase(ctx: EditContext, phrase: string, files: string[]) {
  const want = phrase.toLowerCase().replace(/[^\w\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const words = want.split(' ').filter((w) => w.length > 2);
  let best: { o: ObservationWithSource; score: number } | undefined;

  for (const o of ctx.observations) {
    if (o.type !== 'TRANSCRIPT_SEGMENT' || !o.text) continue;
    if (files.length && !files.includes(o.sourceFileId)) continue;
    const hay = o.text.toLowerCase();
    let score = hay.includes(want) ? 10 : 0;
    for (const w of words) if (hay.includes(w)) score += 1;
    if (score > 0 && (!best || score > best.score)) best = { o, score };
  }
  return best?.o;
}

export function applyInstruction(
  scene: EditorialSceneCandidate, intent: EditIntent, ctx: EditContext
): EditOutcome {
  let ranges = clone(scene.ranges);
  let excluded = scene.excludedMaterial.map((e) => ({ ...e, range: { ...e.range } }));
  const before = dur(ranges);
  const files = scene.sourceClipIds;

  const done = (summary: string): EditOutcome => ({ changed: true, ranges, excluded, summary });
  const nochange = (problem: string): EditOutcome =>
    ({ changed: false, ranges: scene.ranges, excluded: scene.excludedMaterial, summary: 'Nothing changed.', problem });

  switch (intent.kind) {
    case 'CUT_CHATTER': {
      // Anything the classifier already flagged is already out. This catches
      // chatter still sitting inside the cut.
      const removed: string[] = [];
      const next: SourceRange[] = [];
      for (const r of ranges) {
        const chatter = ctx.observations.find((o) =>
          o.type === 'TRANSCRIPT_SEGMENT' && o.sourceFileId === r.sourceFileId && o.text &&
          /rolling|recording|stop the camera|cut the camera|you ready|is it on/i.test(o.text) &&
          (o.startTime ?? 0) < r.endTime && (o.endTime ?? 0) > r.startTime);
        if (chatter) {
          removed.push(chatter.text!.slice(0, 50));
          excluded.push({
            range: { sourceFileId: r.sourceFileId, startTime: Math.max(r.startTime, chatter.startTime ?? r.startTime), endTime: Math.min(r.endTime, chatter.endTime ?? r.endTime), derivedFromObservationIds: [chatter.id] },
            classification: 'CAMERA_DIRECTION', reason: 'creator asked for the camera talk to go',
            preservedInPhysicalTimeline: true, excerpt: chatter.text,
          });
          // Keep whatever is left either side of the chatter.
          const cs = Math.max(r.startTime, chatter.startTime ?? r.startTime);
          const ce = Math.min(r.endTime, chatter.endTime ?? r.endTime);
          if (cs - r.startTime > 0.3) next.push({ ...r, endTime: cs });
          if (r.endTime - ce > 0.3) next.push({ ...r, startTime: ce });
        } else next.push(r);
      }
      if (!removed.length) return nochange('I could not find any camera or production talk left in this cut — it may already be out.');
      ranges = next;
      return done(`Took out the camera talk (${removed.map((r) => `"${r}"`).join(', ')}). The footage is still in your source, just not in the cut.`);
    }

    case 'KEEP_MATERIAL': {
      if (!excluded.length) return nochange('There is nothing currently removed from this scene to put back.');
      const put = excluded.shift()!;
      ranges.push(put.range);
      ranges.sort((a, b) => a.sourceFileId === b.sourceFileId ? a.startTime - b.startTime : a.sourceFileId.localeCompare(b.sourceFileId));
      return done(`Put back the ${put.classification.toLowerCase().replace(/_/g, ' ')}${put.excerpt ? ` ("${put.excerpt.slice(0, 40)}")` : ''}.`);
    }

    case 'HOLD_LONGER': {
      const extra = intent.seconds ?? 1.5;
      const i = intent.where === 'start' ? 0 : ranges.length - 1;
      const r = ranges[i];
      if (!r) return nochange('There is no shot to hold.');
      if (intent.where === 'start') r.startTime = Math.max(0, r.startTime - extra);
      else r.endTime = r.endTime + extra;
      return done(`Held the ${intent.where === 'start' ? 'opening' : 'last'} shot ${extra}s longer.`);
    }

    case 'SHORTEN': {
      const target = intent.seconds ?? before * (intent.fraction ?? 0.15);
      if (target >= before) return nochange(`That would remove the whole scene — it is only ${before.toFixed(1)}s long.`);
      // Trim proportionally from the tail of each piece, which takes the slack
      // out rather than cutting into the start of anybody's line.
      const per = target / ranges.length;
      let removed = 0;
      for (const r of ranges) {
        const can = Math.max(0, (r.endTime - r.startTime) - 0.4);
        const take = Math.min(per, can);
        r.endTime -= take;
        removed += take;
      }
      if (removed < 0.05) return nochange('The pieces are already as tight as they can be without losing dialogue.');
      return done(`Tightened the scene by ${removed.toFixed(1)}s — it is now ${dur(ranges).toFixed(1)}s.`);
    }

    case 'LENGTHEN': {
      const extra = (intent.seconds ?? 1.5) / ranges.length;
      for (const r of ranges) r.endTime += extra;
      return done(`Gave the scene ${(extra * ranges.length).toFixed(1)}s more room — now ${dur(ranges).toFixed(1)}s.`);
    }

    case 'TIGHTEN_ENDING': {
      const last = ranges[ranges.length - 1];
      if (!last) return nochange('There is no ending to tighten.');
      const cut = Math.min(1.2, Math.max(0, (last.endTime - last.startTime) - 0.5));
      if (cut < 0.1) return nochange('The ending is already tight.');
      last.endTime -= cut;
      return done(`Cut ${cut.toFixed(1)}s of slack off the end so it lands harder.`);
    }

    case 'START_WITH': {
      const hit = findPhrase(ctx, intent.phrase!, files);
      if (!hit) return nochange(`I could not find "${intent.phrase}" anywhere in this scene's footage. If it is in another clip, it may not be part of this scene yet.`);
      const start = Math.max(0, (hit.startTime ?? 0) - 0.4);
      // Reorder so the piece containing that moment leads.
      const idx = ranges.findIndex((r) => r.sourceFileId === hit.sourceFileId && start < r.endTime && (hit.endTime ?? 0) > r.startTime);
      if (idx >= 0) {
        const [lead] = ranges.splice(idx, 1);
        lead.startTime = start;
        ranges.unshift(lead);
      } else {
        ranges.unshift({ sourceFileId: hit.sourceFileId, startTime: start, endTime: (hit.endTime ?? start) + 0.5, derivedFromObservationIds: [hit.id] });
      }
      return done(`Started the scene on "${hit.text?.slice(0, 45)}" at ${start.toFixed(1)}s.`);
    }

    case 'END_WITH': {
      const hit = findPhrase(ctx, intent.phrase!, files);
      if (!hit) return nochange(`I could not find "${intent.phrase}" in this scene's footage.`);
      const end = (hit.endTime ?? 0) + 0.5;
      const idx = ranges.findIndex((r) => r.sourceFileId === hit.sourceFileId && (hit.startTime ?? 0) < r.endTime && end > r.startTime);
      if (idx >= 0) {
        const [tail] = ranges.splice(idx, 1);
        tail.endTime = end;
        ranges.push(tail);
      } else {
        ranges.push({ sourceFileId: hit.sourceFileId, startTime: Math.max(0, (hit.startTime ?? 0) - 0.3), endTime: end, derivedFromObservationIds: [hit.id] });
      }
      return done(`Ended the scene on "${hit.text?.slice(0, 45)}".`);
    }

    case 'REMOVE_PHRASE': {
      const hit = findPhrase(ctx, intent.phrase!, files);
      if (!hit) return nochange(`I could not find "${intent.phrase}" in this scene.`);
      const hs = hit.startTime ?? 0, he = hit.endTime ?? hs;
      const next: SourceRange[] = [];
      let touched = false;
      for (const r of ranges) {
        if (r.sourceFileId !== hit.sourceFileId || hs >= r.endTime || he <= r.startTime) { next.push(r); continue; }
        touched = true;
        if (hs - r.startTime > 0.3) next.push({ ...r, endTime: hs });
        if (r.endTime - he > 0.3) next.push({ ...r, startTime: he });
      }
      if (!touched) return nochange(`"${intent.phrase}" is not inside the current cut.`);
      excluded.push({
        range: { sourceFileId: hit.sourceFileId, startTime: hs, endTime: he, derivedFromObservationIds: [hit.id] },
        classification: 'PROGRAM_CONTENT', reason: 'creator asked for it to come out',
        preservedInPhysicalTimeline: true, excerpt: hit.text,
      });
      ranges = next;
      return done(`Cut "${hit.text?.slice(0, 45)}" out of the scene.`);
    }

    case 'ALTERNATE': {
      // Offer a genuinely different shape: lead with the strongest moment.
      if (ranges.length < 2) return nochange('There is only one piece in this scene, so there is no other way to order it.');
      const strongest = ranges.reduce((a, b) => b.derivedFromObservationIds.length > a.derivedFromObservationIds.length ? b : a, ranges[0]);
      ranges = [strongest, ...ranges.filter((r) => r !== strongest)];
      return done('Here is another version — it opens on the strongest moment instead of the chronological start.');
    }

    case 'REORDER':
      // Handled by the caller, which knows about the other scenes.
      return { changed: false, ranges: scene.ranges, excluded: scene.excludedMaterial, summary: intent.reading };

    default:
      return nochange(`I did not understand "${intent.raw}". Try something like "make it shorter", "cut the camera talk", "hold on the ending longer", or "start with the argument".`);
  }
}
