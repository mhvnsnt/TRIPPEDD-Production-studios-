#!/usr/bin/env tsx
/**
 * The acceptance test, run as the creator would experience it:
 *
 *   footage in -> TRIPPEDD picks a scene -> cuts it -> RENDERS A REAL VIDEO
 *   -> explains itself -> creator types a correction -> the cut actually
 *   changes -> re-renders -> creator approves -> next scene -> episode.
 */
import path from 'path';
import { statSync, existsSync, readdirSync } from 'fs';
import { copyFile } from 'fs/promises';
import { ToolProvisioner } from '../src/core/tools/provisioning/ToolProvisioner';
import { QueueManager } from '../src/server/evidenceQueue';
import { EditorialService } from '../src/server/editorialService';
import type { MediaJob } from '../src/core/types';

const DIR = process.argv.includes('--dir') ? process.argv[process.argv.indexOf('--dir') + 1] : '/tmp/stress';
const line = (c = '─') => console.log(c.repeat(76));
const H = (t: string) => { console.log(); line('═'); console.log(t); line('═'); };

(async () => {
  H('TRIPPEDD — MAKE THE SCENE');

  const prov = new ToolProvisioner({ enableTiers: ['ENHANCED', 'INTERCHANGE'] });
  await prov.initialize();

  const queue = new QueueManager({ provisioner: prov, retainMedia: true,
    downloadMedia: async (j: any, dest) => { await copyFile(j.__localSource, dest); return statSync(j.__localSource).size; } });

  const files = readdirSync(DIR).filter((f) => /\.mp4$/i.test(f));
  console.log(`\nFound ${files.length} clips. Watching them now…`);
  for (const f of files) {
    const src = path.join(DIR, f);
    const job: MediaJob = {
      id: `J_${f}`, fileId: f.replace(/\.mp4$/i, ''), originalName: f, mimeType: 'video/mp4',
      size: String(statSync(src).size), state: 'QUEUED', progress: 0, logs: [],
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), tools: {}, evidenceRefs: [],
    };
    (job as any).__localSource = src;
    queue.addJob(job);
  }
  for (const j of queue.getJobs()) if (j.state !== 'NEEDS_REVIEW') await queue.runPipeline(j);

  const ed = new EditorialService();
  ed.ingestFromJobs(queue.getJobs());
  const built = ed.build();
  console.log(`Understood ${built.observationCount} things across ${built.sourceFileCount} clips.`);
  console.log(`Found ${built.scenes.length} likely scene(s).`);

  const scene = ed.nextForReview();
  if (!scene) { console.log('\nNo scene could be built from this footage.'); process.exit(1); }

  // ---------------------------------------------------------------- SCENE 1
  H(`SCENE 1 — ${scene.proposedTitle}`);
  let r = await ed.renderScene(scene.id);
  if (!r.ok) { console.log('RENDER FAILED:', r.error); process.exit(1); }
  console.log(`▶  WATCH: ${r.outputPath}`);
  console.log(`   ${r.durationSec}s, ${r.segmentCount} shot(s)`);

  const x = ed.explain(scene.id)!;
  console.log(`\n${x.headline}\n`);
  console.log('WHAT I DID');
  for (const d of x.did) console.log(`  • ${d}`);
  if (x.unsure.length) {
    console.log('\nWHAT I\'M NOT SURE ABOUT');
    for (const u of x.unsure) console.log(`  ? ${u}`);
  }
  console.log('\nTHE CUT');
  for (const s of x.shots) console.log(`  ${s.label.padEnd(7)} ${String(s.seconds).padStart(5)}s  ${s.from}${s.line ? `  "${s.line}"` : ''}`);

  // ------------------------------------------------- CREATOR TALKS TO IT
  H('CREATOR CORRECTIONS');
  const says = [
    'Cut that camera shit.',
    'Hold on the ending longer.',
    'Make it shorter.',
    'Show me another version.',
    'Paint it purple with a trombone.',   // deliberately nonsense
  ];

  for (const said of says) {
    console.log(`\n  YOU: "${said}"`);
    const out = await ed.instruct(scene.id, said);
    console.log(`  TRIPPEDD: ${out.summary}`);
    if (out.problem) console.log(`            ${out.problem}`);
    if (out.render?.ok) {
      console.log(`            ▶ re-rendered v${out.render.version}: ${out.render.durationSec}s — ${out.render.outputPath}`);
    }
  }

  // ------------------------------------------------------------- APPROVE
  H('APPROVAL');
  console.log('  YOU: "That\'s good."');
  const ok = await ed.instruct(scene.id, "That's good.");
  console.log(`  TRIPPEDD: ${ok.summary}`);
  console.log(`  scene state: ${ed.getStore().get(scene.id)!.humanReviewState}`);

  // Locked scenes must not be quietly editable any more.
  try {
    await ed.instruct(scene.id, 'make it shorter');
    console.log('  !! a locked scene accepted an edit — that is wrong');
  } catch (e: any) {
    console.log(`  locked scene refuses further edits: ${e.message.split('—')[0].trim()}`);
  }

  // ------------------------------------------------------------ SCENE 2
  const next = ed.nextForReview();
  if (next) {
    H(`SCENE 2 — ${next.proposedTitle}`);
    const r2 = await ed.renderScene(next.id);
    console.log(r2.ok ? `▶  WATCH: ${r2.outputPath}  (${r2.durationSec}s)` : `render failed: ${r2.error}`);
    const x2 = ed.explain(next.id)!;
    console.log(`\n${x2.headline}`);
    for (const d of x2.did.slice(0, 3)) console.log(`  • ${d}`);
    await ed.instruct(next.id, "That's good.");
    console.log(`\n  approved -> ${ed.getStore().get(next.id)!.humanReviewState}`);
  }

  // ------------------------------------------------------------ EPISODE
  H('EPISODE');
  const status = ed.episodeStatus();
  console.log(`  ${status.approved} approved scene(s), ${status.runningTimeSec}s, ${status.waitingOnYou} still waiting on you`);
  for (const o of status.order) console.log(`   ${o.position}. ${o.title}  (${o.seconds}s)`);

  const ep = await ed.renderEpisode();
  if (ep.ok) console.log(`\n▶  WATCH THE EPISODE: ${ep.outputPath}  (${ep.durationSec}s from ${ep.sceneCount} scene(s))`);
  else console.log(`\n  episode not rendered: ${ep.error}`);

  H('DONE');
  process.exit(ep.ok ? 0 : 1);
})();
