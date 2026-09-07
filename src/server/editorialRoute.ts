/**
 * Editorial REST surface.
 *
 * Thin transport over EditorialService — all the rules (evidence provenance,
 * lock immutability, refusing to export missing media) live in the core layer,
 * so they hold no matter which caller reaches them.
 */
import express from 'express';
import { editorialService } from './editorialService';
import { queueManager } from './queueManager';
import { LockedSceneError, InvalidTransitionError } from '../core/editorial/approval';
import { MissingMediaError } from '../core/editorial/projectExport';

export const editorialRouter = express.Router();

function fail(res: express.Response, e: any) {
  if (e instanceof LockedSceneError) return res.status(409).json({ error: e.message, code: 'SCENE_LOCKED' });
  if (e instanceof InvalidTransitionError) return res.status(400).json({ error: e.message, code: 'INVALID_TRANSITION' });
  if (e instanceof MissingMediaError) return res.status(409).json({ error: e.message, code: 'MISSING_MEDIA' });
  return res.status(500).json({ error: e?.message ?? String(e) });
}

/** Pull evidence off finished jobs and (re)assemble. */
editorialRouter.post('/build', (req, res) => {
  try {
    const added = editorialService.ingestFromJobs(queueManager.getJobs());
    if (req.body?.narrativeOrder) editorialService.setNarrativeOrder(req.body.narrativeOrder);
    const result = editorialService.build();
    res.json({ observationsAdded: added, ...result });
  } catch (e) { fail(res, e); }
});

editorialRouter.get('/state', (_req, res) => {
  const store = editorialService.getStore();
  const scenes = store.all();
  res.json({
    builtAt: editorialService.getLastBuiltAt() ?? null,
    reconciliation: editorialService.getReconciliation() ?? null,
    observationCount: editorialService.getObservations().length,
    counts: {
      total: scenes.length,
      proposed: scenes.filter((s) => s.humanReviewState === 'PROPOSED').length,
      awaitingRevision: scenes.filter((s) => s.humanReviewState === 'REVISION_REQUESTED').length,
      approved: scenes.filter((s) => s.humanReviewState === 'APPROVED').length,
      locked: scenes.filter((s) => s.humanReviewState === 'LOCKED').length,
      rejected: scenes.filter((s) => s.humanReviewState === 'REJECTED').length,
    },
    preferences: store.learnedPreferences(),
    media: editorialService.getMediaMap(),
  });
});

editorialRouter.get('/scenes', (_req, res) => {
  res.json(editorialService.getStore().all());
});

/** The scene-by-scene workflow: whatever is next awaiting a decision. */
editorialRouter.get('/scenes/next', (_req, res) => {
  const scene = editorialService.nextForReview();
  if (!scene) return res.json({ scene: null, done: true });
  res.json({
    scene,
    done: false,
    transcript: editorialService.transcriptFor(scene),
    remaining: editorialService.reviewQueue().length,
    mediaPath: editorialService.getMediaPath(scene.sourceClipIds[0]) ?? null,
  });
});

editorialRouter.get('/scenes/:id', (req, res) => {
  const scene = editorialService.getStore().get(req.params.id);
  if (!scene) return res.status(404).json({ error: 'unknown scene' });
  res.json({
    scene,
    transcript: editorialService.transcriptFor(scene),
    mediaPath: editorialService.getMediaPath(scene.sourceClipIds[0]) ?? null,
  });
});

editorialRouter.post('/scenes/:id/approve', (req, res) => {
  try { res.json(editorialService.getStore().lock(req.params.id, req.body?.note)); }
  catch (e) { fail(res, e); }
});

editorialRouter.post('/scenes/:id/revise', (req, res) => {
  try {
    const note = req.body?.note;
    if (!note) return res.status(400).json({ error: 'a revision note is required' });
    res.json(editorialService.getStore().requestRevision(req.params.id, note));
  } catch (e) { fail(res, e); }
});

editorialRouter.post('/scenes/:id/reject', (req, res) => {
  try {
    const note = req.body?.note ?? 'rejected by creator';
    res.json(editorialService.getStore().reject(req.params.id, note));
  } catch (e) { fail(res, e); }
});

/** Manual creator edit of the cut. Refused on a locked scene by the store. */
editorialRouter.post('/scenes/:id/ranges', (req, res) => {
  try {
    const ranges = req.body?.ranges;
    if (!Array.isArray(ranges) || !ranges.length) {
      return res.status(400).json({ error: 'ranges must be a non-empty array' });
    }
    const updated = editorialService.getStore().applyMachineEdit(
      req.params.id,
      (s) => {
        s.ranges = ranges;
        s.proposedDuration = Number(ranges.reduce((a: number, r: any) => a + (r.endTime - r.startTime), 0).toFixed(3));
      },
      req.body?.note ?? 'creator adjusted the cut'
    );
    res.json(updated);
  } catch (e) { fail(res, e); }
});

/** Cut the scene together into a watchable file. */
editorialRouter.post('/scenes/:id/render', async (req, res) => {
  try { res.json(await editorialService.renderScene(req.params.id)); }
  catch (e) { fail(res, e); }
});

/** Plain-English account of what the editor did. */
editorialRouter.get('/scenes/:id/explain', (req, res) => {
  const x = editorialService.explain(req.params.id);
  if (!x) return res.status(404).json({ error: 'unknown scene' });
  res.json(x);
});

/**
 * The creator types what they want changed. This is the main way the show gets
 * made — everything else is scaffolding around it.
 */
editorialRouter.post('/scenes/:id/instruct', async (req, res) => {
  const text = (req.body?.text ?? '').toString().trim();
  if (!text) return res.status(400).json({ error: 'tell me what to change' });
  try { res.json(await editorialService.instruct(req.params.id, text)); }
  catch (e) { fail(res, e); }
});

/** The catalog: what each clip actually is, in plain names. */
editorialRouter.get('/catalog', (_req, res) => {
  res.json({ clips: editorialService.getClipNames() });
});

editorialRouter.get('/episode', (_req, res) => {
  res.json(editorialService.episodeStatus());
});

/** The canon gate, readable before you spend a render on a cut that will fail. */
editorialRouter.get('/canon', (_req, res) => {
  res.json(editorialService.canonCheck());
});

editorialRouter.post('/episode/render', async (_req, res) => {
  try { res.json(await editorialService.renderEpisode()); }
  catch (e) { fail(res, e); }
});

editorialRouter.post('/export/:format', async (req, res) => {
  const format = req.params.format as 'otio' | 'kdenlive';
  if (format !== 'otio' && format !== 'kdenlive') {
    return res.status(400).json({ error: 'format must be otio or kdenlive' });
  }
  try {
    res.json(await editorialService.exportProject(format, {
      onlyApproved: !!req.body?.onlyApproved,
      name: req.body?.name,
    }));
  } catch (e) { fail(res, e); }
});

editorialRouter.get('/reconciliation', (_req, res) => {
  const r = editorialService.getReconciliation();
  if (!r) return res.json({ built: false, beats: [] });
  res.json({ built: true, ...r });
});
