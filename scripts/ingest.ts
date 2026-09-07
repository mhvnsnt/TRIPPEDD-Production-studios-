#!/usr/bin/env tsx
/**
 * One-command Drive -> evidence -> scenes -> editable project.
 *
 *   npx tsx scripts/ingest.ts --token "ya29...."
 *   npx tsx scripts/ingest.ts --folder <id> --local ./clips
 *
 * Runs the SAME code the server runs — provisioning, the real analyzers, the
 * real reconciliation, the real assembler, the real exporters. Nothing here is
 * a parallel pipeline, so a green run means the app path works too.
 */
import path from 'path';
import { readdirSync, statSync, existsSync } from 'fs';
import { copyFile } from 'fs/promises';
import { ToolProvisioner } from '../src/core/tools/provisioning/ToolProvisioner';
import { QueueManager } from '../src/server/queueManager';
import { DriveWatcher, listDriveFiles } from '../src/server/driveWatcher';
import { driveCredentials } from '../src/server/driveCredentials';
import { EditorialService } from '../src/server/editorialService';
import { runnerRoot } from '../src/core/tools/execution/runnerRoot';
import type { MediaJob } from '../src/core/types';

function arg(name: string, fallback?: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  if (i >= 0 && process.argv[i + 1] && !process.argv[i + 1].startsWith('--')) return process.argv[i + 1];
  const eq = process.argv.find((a) => a.startsWith(`--${name}=`));
  if (eq) return eq.split('=').slice(1).join('=');
  return fallback;
}
const has = (n: string) => process.argv.includes(`--${n}`);

const FOLDER = arg('folder', process.env.TRIPPEDD_DRIVE_FOLDER || '1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI')!;
const TOKEN = arg('token', process.env.TRIPPEDD_DRIVE_TOKEN);
const LOCAL = arg('local');

const line = (c = '─') => console.log(c.repeat(78));
const VIDEO_EXT = /\.(mp4|mov|m4v|mkv|avi|webm)$/i;

async function main() {
  line('═');
  console.log('TRIPPEDD INGEST');
  line('═');

  // 1. Toolchain
  console.log('\n[1/6] Provisioning toolchain…');
  const prov = new ToolProvisioner({ enableTiers: has('enhanced') ? ['ENHANCED'] : [] });
  const tools = await prov.initialize();
  for (const t of tools) {
    const mark = t.state === 'AVAILABLE' ? '✓' : '·';
    console.log(`   ${mark} ${t.id.padEnd(16)} ${t.state.padEnd(18)} ${t.version ?? ''}`);
  }
  const available = tools.filter((t) => t.state === 'AVAILABLE');
  if (!available.some((t) => t.id === 'ffprobe')) {
    console.error('\nffprobe is unavailable — cannot inspect media. Stopping.');
    process.exit(2);
  }

  // 2. Discovery
  console.log('\n[2/6] Discovering source media…');
  const queue = new QueueManager({ provisioner: prov, retainMedia: true });
  queue.setMaxConcurrentJobs(Number(arg('jobs', '1')));

  let queued = 0;
  if (LOCAL) {
    const dir = path.resolve(LOCAL);
    if (!existsSync(dir)) { console.error(`   local folder not found: ${dir}`); process.exit(2); }
    const files = readdirSync(dir).filter((f) => VIDEO_EXT.test(f));
    console.log(`   local folder ${dir}: ${files.length} video file(s)`);
    for (const f of files) {
      const src = path.join(dir, f);
      const job: MediaJob = {
        id: `JOB_${f}`, fileId: f.replace(VIDEO_EXT, ''), originalName: f, mimeType: 'video/mp4',
        size: String(statSync(src).size), state: 'QUEUED', progress: 0,
        logs: [`Discovered in local folder ${dir}.`],
        createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
        tools: {}, evidenceRefs: [],
      };
      (job as any).__localSource = src;
      queue.addJob(job);
      queued++;
    }
    (queue as any).deps.downloadMedia = async (j: MediaJob, dest: string) => {
      await copyFile((j as any).__localSource, dest);
      return statSync((j as any).__localSource).size;
    };
  } else {
    if (TOKEN) driveCredentials.setBrowserToken(TOKEN);
    const cred = await driveCredentials.resolve();
    if (!cred) {
      const st = await driveCredentials.status();
      console.error('\n   DRIVE NOT CONNECTED — ' + st.detail);
      console.error('   ' + (st.missingCapability ?? ''));
      console.error('\n   Pass a token:   npx tsx scripts/ingest.ts --token "ya29...."');
      console.error('   Or a folder:    npx tsx scripts/ingest.ts --local ./clips');
      process.exit(3);
    }
    console.log(`   credential: ${cred.source}`);
    const watcher = new DriveWatcher(queue, { folderId: FOLDER });
    const scan = await watcher.scanOnce();
    if (scan.error) { console.error(`   Drive scan failed: ${scan.error}`); process.exit(4); }
    console.log(`   folder ${FOLDER}: ${scan.discovered} file(s), ${scan.enqueued} queued, ${scan.skippedNonVideo} non-video skipped`);
    const files = await listDriveFiles(FOLDER, cred.token);
    for (const f of files) console.log(`      ${f.id}  ${(f.mimeType || '').padEnd(16)} ${f.name}`);
    queued = scan.enqueued;
  }

  if (!queued) { console.log('\n   Nothing new to process.'); return; }

  // 3. Analysis
  console.log(`\n[3/6] Analysing ${queued} clip(s) with real tools…`);
  for (const job of queue.getJobs()) {
    if (job.state === 'NEEDS_REVIEW' || job.state === 'UNAVAILABLE') continue;
    const t0 = Date.now();
    await queue.runPipeline(job);
    const obs = (job as any).observations ?? [];
    const ran = Object.entries(job.tools)
      .filter(([, v]: any) => v?.status === 'COMPLETED')
      .map(([k]) => k);
    console.log(`   ${job.originalName}: ${job.state} · ${obs.length} observation(s) · ${((Date.now() - t0) / 1000).toFixed(1)}s`);
    console.log(`      executed: ${ran.join(', ') || 'none'}`);
    for (const [k, v] of Object.entries<any>(job.tools)) {
      if (v?.status !== 'COMPLETED') console.log(`      ${k}: ${v?.status}${v?.error ? ' — ' + String(v.error).slice(0, 90) : ''}`);
    }
  }

  // 4. Reconciliation
  console.log('\n[4/6] Reconciling described material against actual evidence…');
  const editorial = new EditorialService();
  editorial.ingestFromJobs(queue.getJobs());
  const narrative = arg('order')?.split(',').map((s) => s.trim()).filter(Boolean);
  if (narrative) editorial.setNarrativeOrder(narrative);
  const built = editorial.build();

  console.log(`   ${built.observationCount} observation(s) across ${built.sourceFileCount} file(s)`);
  line();
  for (const b of built.reconciliation.beats) {
    const mark = { FOUND: '✓', PARTIALLY_FOUND: '~', AMBIGUOUS_MATCH: '?', NOT_FOUND: '·', MISSING_SOURCE_MEDIA: '∅' }[b.state];
    console.log(`   ${mark} ${b.state.padEnd(21)} ${b.title.slice(0, 34).padEnd(35)} ${b.confidence ? 'conf ' + b.confidence : ''} ${b.candidateSourceFileIds.join(',')}`);
  }
  line();
  console.log(`   ${JSON.stringify(built.reconciliation.summary)}`);

  // 5. Assembly
  console.log(`\n[5/6] Assembling scenes…  ${built.scenes.length} candidate(s)`);
  for (const s of built.scenes) {
    console.log(`\n   #${s.proposedOrder} "${s.proposedTitle}"  ${s.proposedDuration}s  conf ${s.confidence}`);
    if (s.reorderReason) console.log(`      reorder: physical position was ${s.physicalOrder}`);
    for (const r of s.ranges) console.log(`      CUT     ${r.sourceFileId} ${r.startTime.toFixed(2)} → ${r.endTime.toFixed(2)}`);
    for (const e of s.excludedMaterial) console.log(`      EXCLUDE ${e.classification.padEnd(22)} "${(e.excerpt ?? '').slice(0, 44)}"`);
    for (const a of s.chronologyAssumptions) console.log(`      ASSUME  ${a.statement.slice(0, 88)}`);
  }

  // 6. Export
  if (!built.scenes.length) { console.log('\n   No scenes to export.'); return; }
  console.log('\n[6/6] Exporting editable projects…');
  for (const fmt of ['kdenlive', 'otio'] as const) {
    try {
      const r = await editorial.exportProject(fmt, { name: arg('name', 'working_cut') });
      console.log(`   ${fmt.padEnd(9)} ${r.outputPath}`);
      console.log(`             ${r.clipCount} clip(s), ${r.totalDuration.toFixed(2)}s · verified=${r.verified} · ${r.verifyDetail ?? ''}`);
    } catch (e: any) {
      console.log(`   ${fmt.padEnd(9)} FAILED — ${e.message}`);
    }
  }

  console.log(`\nMedia library: ${queue.getMediaLibraryDir()}`);
  console.log('Open the app and go to Editorial Review to approve scene by scene.');
  line('═');
}

main().catch((e) => { console.error('\nFATAL:', e?.message ?? e); process.exit(1); });
