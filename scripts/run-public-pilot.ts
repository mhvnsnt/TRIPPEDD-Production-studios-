import fs from 'fs/promises';
import path from 'path';
import { downloadPublicDriveFolder } from '../src/server/publicDriveFolder';
import { queueManager } from '../src/server/queueManager';
import { toolManager } from '../src/server/toolManager';
import { ProductionProgressLedger } from '../src/server/productionProgress';
import { buildEp01FirstAssembly } from '../src/server/pilotRenderer';

const folderUrl = process.env.TRIPPEDD_DRIVE_FOLDER_URL || 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const cacheRoot = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media'));
const outputRoot = path.resolve(process.env.TRIPPEDD_OUTPUT_DIR || path.join(process.cwd(), 'public', 'production'));
const mediaExtensions = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp', '.wav', '.mp3', '.m4a']);
const cutMode = process.env.TRIPPEDD_CUT_MODE === 'AUTONOMOUS' ? 'AUTONOMOUS' : 'SHOWRUNNER';
const runId = process.env.TRIPPEDD_RUN_ID || [process.env.GITHUB_RUN_ID, process.env.GITHUB_RUN_ATTEMPT].filter(Boolean).join('-') || `${Date.now()}-${process.pid}`;
const expectedSourceFiles = Math.max(1, Number(process.env.TRIPPEDD_EXPECTED_SOURCE_FILES || 19));
const ledger = new ProductionProgressLedger({ episodeId: 'EP01', runId, rootDir: path.join(outputRoot, '.progress') });

function bar(percent: number, width = 28) {
  const filled = Math.round((Math.max(0, Math.min(100, percent)) / 100) * width);
  return `[${'#'.repeat(filled)}${'-'.repeat(width - filled)}] ${Math.round(percent)}%`;
}

async function report(stageId: string, completed: number, total: number, message: string, status: 'RUNNING' | 'COMPLETE' = 'RUNNING') {
  await ledger.update(stageId, { status, completed, total, message });
  const snapshot = ledger.getSnapshot();
  const stage = snapshot.stages.find(item => item.id === stageId);
  if (stage) console.log(`PRODUCTION_BAR stage=${stage.label} ${bar(stage.percent)} work=${stage.completed}/${stage.total} elapsed=${Math.round((stage.elapsedMs ?? 0) / 1000)}s rate=${(stage.ratePerSecond ?? 0).toFixed(3)}/s eta=${stage.etaLabel ?? 'UNKNOWN'} operation=${message}`);
  console.log(`PRODUCTION_TOTAL ${bar(snapshot.overallPercent)} work=${snapshot.overallCompleted}/${snapshot.overallTotal} current=${stage?.label ?? stageId}`);
}

async function waitForJob(fileId: string) {
  for (;;) {
    const job = queueManager.getJob(fileId);
    if (!job) throw new Error(`Job disappeared: ${fileId}`);
    if (job.state === 'NEEDS_REVIEW' || job.state === 'EVIDENCE_READY' || job.state === 'FAILED') return job;
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}

async function main() {
  await fs.mkdir(cacheRoot, { recursive: true });
  await ledger.init([
    { id: 'drive-ingest', label: 'Drive ingest', total: expectedSourceFiles },
    { id: 'source-analysis', label: 'Source analysis', total: 1 },
    { id: 'editorial-assembly', label: 'Editorial assembly', total: 1 }
  ]);
  await report('drive-ingest', 0, expectedSourceFiles, 'Initializing public Drive ingest.');
  await toolManager.initialize();
  console.log(`[EP01/${cutMode}] Downloading public Drive folder with resumable per-file ingest: ${folderUrl}`);

  let lastDriveProgress = '';
  const downloaded = await downloadPublicDriveFolder(folderUrl, cacheRoot, progress => {
    const total = Math.max(1, progress.total || expectedSourceFiles);
    const status = progress.phase === 'COMPLETE' && progress.failed === 0 ? 'COMPLETE' : 'RUNNING';
    const current = progress.current ? ` Current=${progress.current}.` : '';
    const failures = progress.failed ? ` Failed=${progress.failed}.` : '';
    const fingerprint = `${progress.phase}|${progress.completed}|${progress.failed}|${progress.current ?? ''}`;
    // Do not emit artificial heartbeats. If the underlying ingest stops
    // changing, watch-progress must be able to detect the stall.
    if (fingerprint !== lastDriveProgress) {
      lastDriveProgress = fingerprint;
      void report('drive-ingest', Math.min(progress.completed, total), total, `${progress.phase}: ${progress.completed}/${total} source files materialized.${failures}${current}`, status).catch(() => undefined);
    }
  });

  const media = downloaded.filter(file => mediaExtensions.has(path.extname(file).toLowerCase()));
  console.log(`[EP01/${cutMode}] Materialized ${media.length} supported media file(s).`);
  if (media.length < expectedSourceFiles) {
    await report('drive-ingest', media.length, expectedSourceFiles, `SOURCE BLOCKED: only ${media.length}/${expectedSourceFiles} media files are available; refusing to manufacture a complete episode.`, 'RUNNING');
    throw new Error(`EP01 source ingest is incomplete: ${media.length}/${expectedSourceFiles} media files available.`);
  }
  await report('drive-ingest', media.length, expectedSourceFiles, `Materialized ${media.length}/${expectedSourceFiles} supported media file(s).`, 'COMPLETE');

  await ledger.update('source-analysis', { status: 'RUNNING', completed: 0, total: media.length, message: `Analyzing ${media.length} source files.` });
  const jobs: string[] = [];
  for (let sourceOrder = 0; sourceOrder < media.length; sourceOrder++) {
    const filePath = media[sourceOrder];
    const fileId = `PUBLIC_${Buffer.from(path.resolve(filePath)).toString('base64url').slice(-48)}`;
    const stat = await fs.stat(filePath);
    queueManager.setLocalSource(fileId, filePath);
    if (!queueManager.getJob(fileId)) {
      queueManager.addJob({ id: `JOB_${fileId}`, fileId, originalName: path.basename(filePath), mimeType: 'video/*', size: stat.size, state: 'QUEUED', progress: 0, logs: ['Credential-free public Drive source.', `Local source: ${filePath}`, `Cut mode: ${cutMode}`], createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), tools: {}, evidenceRefs: [], sourceOrder } as any);
    } else {
      const existing = queueManager.getJob(fileId) as any;
      if (existing) existing.sourceOrder = sourceOrder;
      queueManager.setLocalSource(fileId, filePath);
    }
    jobs.push(fileId);
  }

  let lastAnalysisFingerprint = '';
  const analysisMonitor = setInterval(() => {
    const jobsNow = jobs.map(fileId => queueManager.getJob(fileId)).filter(Boolean) as any[];
    const completed = jobsNow.reduce((sum, job) => sum + (['NEEDS_REVIEW', 'EVIDENCE_READY', 'FAILED'].includes(job.state) ? 1 : Math.max(0, Math.min(1, Number(job.progress || 0) / 100))), 0);
    const current = jobsNow.find(job => !['NEEDS_REVIEW', 'EVIDENCE_READY', 'FAILED'].includes(job.state));
    const fingerprint = `${completed.toFixed(3)}|${current?.fileId ?? 'none'}|${current?.state ?? 'none'}|${current?.progress ?? 0}`;
    if (fingerprint !== lastAnalysisFingerprint) {
      lastAnalysisFingerprint = fingerprint;
      void report('source-analysis', completed, jobs.length, current ? `Analyzing ${current.originalName}; state=${current.state}, source progress=${Math.round(Number(current.progress || 0))}%.` : 'Finalizing analyzed source evidence.').catch(() => undefined);
    }
  }, 2000);

  let results: any[];
  try {
    results = await Promise.all(jobs.map(fileId => waitForJob(fileId)));
  } finally {
    clearInterval(analysisMonitor);
  }
  let failed = 0;
  for (const job of results) {
    if (job.state === 'FAILED') {
      failed++;
      console.warn(`[EP01/${cutMode}] Skipping failed source ${job.originalName}; continuing with remaining footage.`);
    } else {
      console.log(`[EP01/${cutMode}] Analyzed ${job.originalName}`);
    }
  }
  const usable = jobs.length - failed;
  if (!usable) throw new Error(`All ${jobs.length} source analyses failed; refusing to manufacture an assembly from missing evidence.`);
  await report('source-analysis', jobs.length, jobs.length, `Analysis batch complete: ${usable}/${jobs.length} source jobs usable.`, 'COMPLETE');

  await report('editorial-assembly', 0, 1, 'Handing measured source evidence to editorial assembly.');
  const manifest = await buildEp01FirstAssembly({ maxClips: Number(process.env.EP01_MAX_CLIPS || 24), clipPaddingSeconds: Number(process.env.EP01_CLIP_PADDING || 1.25) });
  console.log(JSON.stringify(manifest, null, 2));
  await report('editorial-assembly', manifest.status === 'ROUGH_CUT_READY' ? 1 : 0, 1, manifest.status === 'ROUGH_CUT_READY' ? 'Editorial assembly produced a rough cut.' : 'Editorial assembly waiting for evidence.', manifest.status === 'ROUGH_CUT_READY' ? 'COMPLETE' : 'RUNNING');
  if (manifest.status !== 'ROUGH_CUT_READY') process.exitCode = 2;
}

main().catch(async error => {
  console.error(error);
  try { await ledger.update('editorial-assembly', { status: 'FAILED', message: error instanceof Error ? error.message : String(error) }); } catch { /* preserve original failure */ }
  process.exitCode = 1;
});
