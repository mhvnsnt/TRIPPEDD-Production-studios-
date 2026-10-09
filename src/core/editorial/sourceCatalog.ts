/**
 * THE SOURCE CATALOG — what each clip IS, and who says so.
 *
 * The creator's rule, and it is absolute: THE ORIGINAL FILE IS NEVER RENAMED.
 * A clip's identity is the filename the camera wrote and the Drive id it
 * arrived with, and both are immutable for the life of the production. A
 * display name is a LABEL LAID OVER that identity, never a replacement for it,
 * and this module refuses to hand back a display name where a filename is
 * wanted.
 *
 * The other half is provenance of the ASSIGNMENT itself. A machine guess and a
 * decision the creator made after watching the footage are not the same kind of
 * claim and must never be stored in the same field with the same weight:
 *
 *   UNASSIGNED      nothing has claimed it
 *   AI_CANDIDATE    the pipeline's proposal. Freely replaced by a better pass.
 *   HUMAN_CONFIRMED the creator watched it and said what it is. This is ground
 *                   truth. No autonomous pass may overwrite it, ever — that is
 *                   the whole reason he only has to say it once.
 *   HUMAN_REJECTED  the creator said it is NOT that. Also permanent, and also
 *                   information: it stops the same wrong guess coming back.
 */

export type AssignmentStatus = 'UNASSIGNED' | 'AI_CANDIDATE' | 'HUMAN_CONFIRMED' | 'HUMAN_REJECTED';

/** How sure the pipeline is, per evidence channel. Kept separate on purpose. */
export interface ChannelConfidence {
  /** Frames, shot boundaries, on-screen text. */
  visual?: 'HIGH' | 'MEDIUM' | 'LOW' | 'NONE';
  /** Transcript. On this footage it is frequently the WEAKER channel. */
  audio?: 'HIGH' | 'MEDIUM' | 'LOW' | 'NONE';
  /** Recording time and neighbours. Strong even when everything else fails. */
  chronology?: 'HIGH' | 'MEDIUM' | 'LOW' | 'NONE';
}

export interface SourceClipEntry {
  /** Immutable. Derived from the original filename, never from a display name. */
  sourceId: string;
  /** Immutable. Exactly what the camera wrote. */
  originalFilename: string;
  /** Immutable. What Drive calls it, when known. */
  driveFileId?: string;

  /**
   * A human-readable label. NEVER written back to disk or to Drive; this is a
   * catalog entry, not a rename.
   */
  displayName?: string;
  displayNameStatus: AssignmentStatus;

  /** Which EP01 canon segment this clip belongs to. */
  canonSegmentId?: string;
  assignmentStatus: AssignmentStatus;
  /** Why — a beat id, a phrase, or the creator's own words. */
  assignmentReason?: string;
  confirmedAt?: string;

  /** Segments the creator has explicitly ruled OUT for this clip. */
  rejectedSegmentIds: string[];

  recordedAt?: string;
  sessionId?: string;
  durationSec?: number;
  /** Path to the frame strip, so a clip can be identified by looking at it. */
  contactSheet?: string;
  transcriptExcerpt?: string;
  transcriptLineCount: number;
  confidence: ChannelConfidence;
}

/** What the UI shows for one clip. Identity and label are never conflated. */
export interface CatalogView {
  sourceId: string;
  /** The filename to search for in Drive. Always the original. */
  openInDriveAs: string;
  driveFileRenamed: false;
  catalogDisplayName?: string;
  assignment: { canonSegmentId?: string; status: AssignmentStatus; reason?: string };
}

export class SourceCatalog {
  private entries = new Map<string, SourceClipEntry>();

  constructor(entries: SourceClipEntry[] = []) {
    for (const e of entries) this.entries.set(e.sourceId, e);
  }

  all(): SourceClipEntry[] {
    return [...this.entries.values()].sort((a, b) =>
      (a.recordedAt ?? a.originalFilename).localeCompare(b.recordedAt ?? b.originalFilename));
  }
  get(sourceId: string): SourceClipEntry | undefined { return this.entries.get(sourceId); }

  /** Registers a clip. Identity fields are set once and never changed after. */
  register(e: Omit<SourceClipEntry, 'displayNameStatus' | 'assignmentStatus' | 'rejectedSegmentIds' | 'confidence' | 'transcriptLineCount'>
    & Partial<Pick<SourceClipEntry, 'displayNameStatus' | 'assignmentStatus' | 'rejectedSegmentIds' | 'confidence' | 'transcriptLineCount'>>): SourceClipEntry {
    const existing = this.entries.get(e.sourceId);
    if (existing) {
      // Refresh only the measured fields. A confirmed assignment survives a
      // re-ingest — re-running analysis is not the creator changing his mind.
      Object.assign(existing, {
        recordedAt: e.recordedAt ?? existing.recordedAt,
        sessionId: e.sessionId ?? existing.sessionId,
        durationSec: e.durationSec ?? existing.durationSec,
        contactSheet: e.contactSheet ?? existing.contactSheet,
        transcriptExcerpt: e.transcriptExcerpt ?? existing.transcriptExcerpt,
        transcriptLineCount: e.transcriptLineCount ?? existing.transcriptLineCount,
        confidence: e.confidence ?? existing.confidence,
      });
      return existing;
    }
    const entry: SourceClipEntry = {
      displayNameStatus: 'UNASSIGNED',
      assignmentStatus: 'UNASSIGNED',
      rejectedSegmentIds: [],
      transcriptLineCount: 0,
      confidence: {},
      ...e,
    };
    this.entries.set(entry.sourceId, entry);
    return entry;
  }

  /**
   * A machine proposal. REFUSES to touch anything the creator has settled —
   * that refusal is the entire value of the confirmed state.
   */
  propose(sourceId: string, canonSegmentId: string, reason: string, displayName?: string): 'APPLIED' | 'REFUSED_HUMAN_CONFIRMED' | 'REFUSED_HUMAN_REJECTED' | 'NO_SUCH_CLIP' {
    const e = this.entries.get(sourceId);
    if (!e) return 'NO_SUCH_CLIP';
    if (e.assignmentStatus === 'HUMAN_CONFIRMED') return 'REFUSED_HUMAN_CONFIRMED';
    if (e.rejectedSegmentIds.includes(canonSegmentId)) return 'REFUSED_HUMAN_REJECTED';

    e.canonSegmentId = canonSegmentId;
    e.assignmentStatus = 'AI_CANDIDATE';
    e.assignmentReason = reason;
    if (displayName && e.displayNameStatus !== 'HUMAN_CONFIRMED') {
      e.displayName = displayName;
      e.displayNameStatus = 'AI_CANDIDATE';
    }
    return 'APPLIED';
  }

  /** The creator watched it and said what it is. Ground truth from here on. */
  confirm(sourceId: string, canonSegmentId: string, opts: { displayName?: string; note?: string } = {}): SourceClipEntry {
    const e = this.entries.get(sourceId);
    if (!e) throw new Error(`no clip "${sourceId}" in the catalog`);
    e.canonSegmentId = canonSegmentId;
    e.assignmentStatus = 'HUMAN_CONFIRMED';
    e.assignmentReason = opts.note ?? 'confirmed by the creator after watching the footage';
    e.confirmedAt = new Date().toISOString();
    e.rejectedSegmentIds = e.rejectedSegmentIds.filter((id) => id !== canonSegmentId);
    if (opts.displayName) { e.displayName = opts.displayName; e.displayNameStatus = 'HUMAN_CONFIRMED'; }
    return e;
  }

  /** The creator said it is NOT that. Remembered, so the guess cannot return. */
  reject(sourceId: string, canonSegmentId: string): SourceClipEntry {
    const e = this.entries.get(sourceId);
    if (!e) throw new Error(`no clip "${sourceId}" in the catalog`);
    if (!e.rejectedSegmentIds.includes(canonSegmentId)) e.rejectedSegmentIds.push(canonSegmentId);
    if (e.canonSegmentId === canonSegmentId && e.assignmentStatus !== 'HUMAN_CONFIRMED') {
      e.canonSegmentId = undefined;
      e.assignmentStatus = 'UNASSIGNED';
      e.assignmentReason = undefined;
    }
    return e;
  }

  /** Only what the creator settled. This is what assembly should trust. */
  confirmedMappings(): { sourceId: string; canonSegmentId: string }[] {
    return this.all()
      .filter((e) => e.assignmentStatus === 'HUMAN_CONFIRMED' && e.canonSegmentId)
      .map((e) => ({ sourceId: e.sourceId, canonSegmentId: e.canonSegmentId! }));
  }

  /**
   * How to find this clip. The Drive file was never renamed, and the view says
   * so explicitly rather than leaving anyone to assume a display name is a
   * filename they can search for.
   */
  view(sourceId: string): CatalogView | undefined {
    const e = this.entries.get(sourceId);
    if (!e) return undefined;
    return {
      sourceId: e.sourceId,
      openInDriveAs: e.originalFilename,
      driveFileRenamed: false,
      catalogDisplayName: e.displayName,
      assignment: { canonSegmentId: e.canonSegmentId, status: e.assignmentStatus, reason: e.assignmentReason },
    };
  }

  toJSON(): SourceClipEntry[] { return this.all(); }
  static fromJSON(raw: unknown): SourceCatalog {
    return new SourceCatalog(Array.isArray(raw) ? (raw as SourceClipEntry[]) : []);
  }
}
