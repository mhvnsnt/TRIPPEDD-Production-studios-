#!/usr/bin/env tsx
/**
 * Real multi-clip stress test.
 *
 * Actual processes, actual media, actual filesystem. Nothing about disk or RSS
 * is mocked: the numbers reported at the end are read from statfs and /proc
 * during the run. The point is to prove the pipeline stays inside its budget
 * and cleans up after itself, not that it can finish in ideal conditions.
 */
import path from 'path';
import { readdirSync, statSync } from 'fs';
import { copyFile } from 'fs/promises';
import { ToolProvisioner } from '../src/core/tools/provisioning/ToolProvisioner';
import { QueueManager } from '../src/server/evidenceQueue';
import { ResourceGovernor } from '../src/core/scheduler/ResourceGovernor';
import { EditorialService } from '../src/server/editorialService';
import { runnerRoot } from '../src/core/tools/execution/runnerRoot';
import type { MediaJob } from '../src/core/types';

function arg(n: string, d?: string) {
  const i = process.argv.indexOf(`--${n}`);
  if (i >= 0 && process.argv[i + 1]) return process.argv[i + 1];
  const eq = process.argv.find((a) => a.startsWith(`--${n}=`));
  return eq ? eq.split('=').slice(1).join('=') : d;
}

const DIR = arg('dir', '/tmp/stress')!;
const DISK_QUOTA = Number(arg('quota', '512'));
const HEAVY = Number(arg('heavy', '2'));
const line = (c = '─') => console.log(c.repeat(76));

(async () => {
  line('═'); console.log('TRIPPEDD RESOURCE STRESS TEST'); line('═');

  const prov = new ToolProvisioner({ enableTiers: ['ENHANCED', 'INTERCHANGE'] });
  const tools = await prov.initialize();
  const avail = tools.filter((t) => t.state === 'AVAILABLE').map((t) => t.id);
  console.log(`\ntools available: ${avail.join(', ')}`);
  const purge = prov.getModelPurge();
  console.log(`model artifact sweep: ${purge?.removed.length ?? 0} removed, ${((purge?.bytesReclaimed ?? 0) / 1048576).toFixed(0)}MB reclaimed`);

  // A deliberately tight budget so the governor has to actually govern.
  const governor = new ResourceGovernor({
    workspacePath: runnerRoot(),
    limits: { diskQuotaMB: DISK_QUOTA, HEAVY, MEDIUM: 2, LIGHT: 4 },
  });
  const queue = new QueueManager({
    provisioner: prov, governor, retainMedia: true,
    resourceRetryMs: 1500, maxResourceWaits: 20,
    downloadMedia: async (j: any, dest) => {
      await copyFile(j.__localSource, dest);
      return statSync(j.__localSource).size;
    },
  });
  queue.setMaxConcurrentJobs(Number(arg('jobs', '3')));

  const files = readdirSync(DIR).filter((f) => /\.mp4$/i.test(f));
  console.log(`clips: ${files.length}   disk quota: ${DISK_QUOTA}MB   heavy limit: ${HEAVY}   concurrent jobs: ${arg('jobs', '3')}`);

  for (const f of files) {
    const src = path.join(DIR, f);
    const job: MediaJob = {
      id: `JOB_${f}`, fileId: f.replace(/\.mp4$/i, ''), originalName: f, mimeType: 'video/mp4',
      size: String(statSync(src).size), state: 'QUEUED', progress: 0, logs: [],
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
      tools: {}, evidenceRefs: [],
    };
    (job as any).__localSource = src;
    queue.addJob(job);
  }

  // Sample real resource state throughout, rather than reporting one snapshot.
  let peakReservedMB = 0, peakHeavy = 0, peakDiskUsedMB = 0, minDiskFreeMB = Infinity;
  let breaches = 0, samples = 0;
  const startFree = await governor.diskFreeMB();

  const sampler = setInterval(async () => {
    const s = await governor.snapshot();
    samples++;
    peakReservedMB = Math.max(peakReservedMB, s.reservedMB);
    peakHeavy = Math.max(peakHeavy, s.active.HEAVY);
    minDiskFreeMB = Math.min(minDiskFreeMB, s.diskFreeMB);
    peakDiskUsedMB = Math.max(peakDiskUsedMB, startFree - s.diskFreeMB);
    if (s.reservedMB > DISK_QUOTA) breaches++;
    if (s.active.HEAVY > HEAVY) breaches++;
  }, 200);

  const t0 = Date.now();
  // Wait for the queue to settle, including any resource waits.
  for (;;) {
    await new Promise((r) => setTimeout(r, 1000));
    const jobs = queue.getJobs();
    const busy = jobs.filter((j) =>
      ['QUEUED', 'PROBING', 'ANALYZING', 'DOWNLOADING/STREAMING', 'RESOURCE_WAIT'].includes(j.state));
    if (!busy.length) break;
    if (Date.now() - t0 > 30 * 60_000) { console.log('\n! timed out'); break; }
  }
  clearInterval(sampler);
  const elapsed = (Date.now() - t0) / 1000;

  const jobs = queue.getJobs();
  const counts = queue.getCounts();
  const waits = queue.getResourceWaits();
  const totalWaits = Object.values(waits).reduce((a, b) => a + b, 0);

  // Peak RSS actually observed, per tool, from real ToolRuns.
  const obs = governor.getObservations();
  const peakRss = Math.max(0, ...Object.values(obs).map((o: any) => o.peakRssMB));

  const usage = queue.getLifecycle().usage();
  // Read the real byte counts off the lifecycle rather than re-parsing logs.
  const lifecycle = queue.getLifecycle();
  const released = lifecycle.all().filter((a) => a.releasedAt);
  const reclaimedBytes = released.reduce((a, x) => a + x.sizeBytes, 0);
  const fmtB = (n: number) =>
    n < 1024 ? `${n} B` : n < 1048576 ? `${(n / 1024).toFixed(1)} KB` : `${(n / 1048576).toFixed(1)} MB`;

  console.log('\n'); line('═'); console.log('MEASURED RESULTS'); line('═');
  console.log(`clips completed              ${counts.processed}/${files.length}`);
  console.log(`failed                       ${counts.failed}`);
  console.log(`elapsed                      ${elapsed.toFixed(1)}s`);
  console.log(`peak temp disk RESERVED      ${peakReservedMB} MB   (quota ${DISK_QUOTA} MB)`);
  console.log(`peak actual disk consumed    ${peakDiskUsedMB} MB`);
  console.log(`min free disk during run     ${(minDiskFreeMB / 1024).toFixed(2)} GB`);
  console.log(`max concurrent HEAVY         ${peakHeavy}        (limit ${HEAVY})`);
  console.log(`budget breaches              ${breaches}        (samples ${samples})`);
  console.log(`resource waits               ${totalWaits}`);
  console.log(`cleanup reclaimed            ${fmtB(reclaimedBytes)} across ${released.length} artifact(s)`);
  console.log(`live artifacts by policy     ${Object.entries(usage).filter(([, v]: any) => v.count).map(([k, v]: any) => `${k}=${v.count}/${(v.bytes / 1048576).toFixed(1)}MB`).join(' ') || 'none'}`);
  console.log(`peak RSS observed (real)     ${peakRss} MB`);
  console.log(`per-tool measured RSS        ${Object.entries(obs).map(([k, v]: any) => `${k}=${v.peakRssMB}MB`).join(' ')}`);
  console.log(`model artifacts              ${prov.getModels().getRecords().length ? 'checked' : 'swept at boot'}`);

  console.log('\nper-clip:');
  for (const j of jobs) {
    const ran = Object.entries(j.tools).filter(([, v]: any) => v?.status === 'COMPLETED').map(([k]) => k);
    const blk = (j as any).resourceBlockedTools ?? [];
    console.log(`  ${j.originalName.padEnd(14)} ${j.state.padEnd(14)} ${ran.length} tools · ${(j as any).observations?.length ?? 0} obs${blk.length ? ` · blocked: ${blk.join(',')}` : ''}`);
  }

  // Feed the evidence forward so the editorial layer is exercised too.
  const ed = new EditorialService();
  ed.ingestFromJobs(jobs);
  const built = ed.build();
  console.log(`\neditorial: ${built.scenes.length} scene(s) from ${built.observationCount} observations across ${built.sourceFileCount} files`);
  console.log(`reconciliation: ${JSON.stringify(built.reconciliation.summary)}`);
  for (const s of built.scenes) {
    const lim = s.evidenceLimitations?.length ? ` · LIMITED: ${s.evidenceLimitations.map((l) => l.tool).join(',')}` : '';
    console.log(`  #${s.proposedOrder} "${s.proposedTitle.slice(0, 44)}" ${s.proposedDuration}s conf ${s.confidence}${lim}`);
  }

  // A run that stayed inside its budget by doing no work is not a pass. The
  // first version of this script reported success while every heavy analyzer
  // was resource-blocked and the editorial layer produced nothing.
  const heavyRan = jobs.some((j) =>
    ['whisper', 'demucs', 'whisperx'].some((t) => (j.tools as any)[t]?.status === 'COMPLETED'));
  const producedEvidence = jobs.every((j) => ((j as any).observations?.length ?? 0) > 0);
  const producedScenes = built.scenes.length > 0;

  const checks: [string, boolean][] = [
    ['no budget breaches', breaches === 0],
    ['no failed jobs', counts.failed === 0],
    [`heavy concurrency <= ${HEAVY}`, peakHeavy <= HEAVY],
    [`reserved disk <= ${DISK_QUOTA}MB`, peakReservedMB <= DISK_QUOTA],
    ['all clips completed', counts.processed === files.length],
    ['heavy analyzers actually ran', heavyRan],
    ['every clip produced evidence', producedEvidence],
    ['editorial produced scenes', producedScenes],
  ];

  line();
  for (const [name, ok] of checks) console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}`);
  const pass = checks.every(([, ok]) => ok);
  line('═');
  console.log(pass ? 'STRESS TEST PASSED' : 'STRESS TEST FAILED');
  line('═');
  queue.stop();
  process.exit(pass ? 0 : 1);
})();
