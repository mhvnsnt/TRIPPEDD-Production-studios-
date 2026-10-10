import fs from 'fs/promises';
import path from 'path';

process.env.TRIPPEDD_ENABLE_WHISPER = 'false';
process.env.MEDIA_MAX_CONCURRENT = '1';
process.env.EP01_RENDER_CONCURRENCY = process.env.EP01_RENDER_CONCURRENCY || '4';

const { downloadPublicDriveFolder } = await import('../src/server/publicDriveFolder');
const { queueManager } = await import('../src/server/queueManager');
const { toolManager } = await import('../src/server/toolManager');
const { buildEp01FirstAssembly } = await import('../src/server/pilotRenderer');

const folderUrl = process.env.TRIPPEDD_DRIVE_FOLDER_URL || 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const cacheRoot = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media'));
const mediaExtensions = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp', '.wav', '.mp3', '.m4a']);
const cutMode = process.env.TRIPPEDD_CUT_MODE === 'AUTONOMOUS' ? 'AUTONOMOUS' : 'SHOWRUNNER';

async function waitForJob(fileId: string, timeoutMs = 20 * 60 * 1000) {
  const started = Date.now();
  for (;;) {
    const job = queueManager.getJob(fileId);
    if (!job) throw new Error(`Job disappeared: ${fileId}`);
    if (job.state === 'NEEDS_REVIEW' || job.state === 'EVIDENCE_READY' || job.state === 'FAILED') return job;
    if (Date.now() - started > timeoutMs) {
      queueManager.log(fileId, 'Bounded analysis timeout reached; source marked failed so the episode can continue with remaining evidence.');
      queueManager.updateJob(fileId, { state: 'FAILED', progress: 100 });
      return queueManager.getJob(fileId)!;
    }
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}

await toolManager.initialize();
await fs.mkdir(cacheRoot, { recursive: true });
console.log(`[EP01/${cutMode}] FAST first assembly: Whisper deferred; bounded source analysis enabled.`);
const downloaded = await downloadPublicDriveFolder(folderUrl, cacheRoot);
const media = downloaded.filter(file => mediaExtensions.has(path.extname(file).toLowerCase()));
console.log(`[EP01/${cutMode}] ${media.length} supported media file(s) available.`);
if (!media.length) throw new Error('The public Drive folder produced no supported media files.');

const jobs: string[] = [];
for (let sourceOrder = 0; sourceOrder < media.length; sourceOrder++) {
  const filePath = media[sourceOrder];
  const fileId = `PUBLIC_${Buffer.from(path.resolve(filePath)).toString('base64url').slice(-48)}`;
  const stat = await fs.stat(filePath);
  queueManager.setLocalSource(fileId, filePath);
  if (!queueManager.getJob(fileId)) {
    queueManager.addJob({ id: `JOB_${fileId}`, fileId, originalName: path.basename(filePath), mimeType: 'video/*', size: stat.size, state: 'QUEUED', progress: 0, logs: ['Credential-free public Drive source.', `Local source: ${filePath}`, `Cut mode: ${cutMode}`, 'FAST first-assembly mode: Whisper deferred.'], createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), tools: {}, evidenceRefs: [], sourceOrder } as any);
  } else {
    const existing = queueManager.getJob(fileId) as any;
    if (existing) existing.sourceOrder = sourceOrder;
    queueManager.setLocalSource(fileId, filePath);
  }
  jobs.push(fileId);
}

const results = await Promise.all(jobs.map(fileId => waitForJob(fileId)));
let failed = 0;
for (const job of results) {
  if (job.state === 'FAILED') {
    failed++;
    console.warn(`[EP01/${cutMode}] Skipping timed-out/failed source ${job.originalName}.`);
  } else console.log(`[EP01/${cutMode}] Analyzed ${job.originalName}`);
}
const usable = jobs.length - failed;
console.log(`[EP01/${cutMode}] Fast analysis batch complete: ${usable}/${jobs.length} source jobs usable.`);
if (!usable) throw new Error(`All ${jobs.length} source analyses failed; refusing to manufacture an assembly from missing evidence.`);

const comicTag = path.resolve('production/EP01/generated/comic/ep01_bastard_tag.mp4');
const legacyTag = path.resolve('production/EP01/generated/blender/ep01_bastard_tag.mp4');
try {
  await fs.access(comicTag);
  await fs.mkdir(path.dirname(legacyTag), { recursive: true });
  await fs.copyFile(comicTag, legacyTag);
  console.log('[EP01] Promoted validated 2D Bastard tag into the renderer compatibility path.');
} catch {
  console.warn('[EP01] 2D Bastard tag was not present; assembly will remain source-evidence-only for that generated beat.');
}

const manifest = await buildEp01FirstAssembly({ maxClips: Number(process.env.EP01_MAX_CLIPS || 24), clipPaddingSeconds: Number(process.env.EP01_CLIP_PADDING || 1.25) });
console.log(JSON.stringify(manifest, null, 2));
if (manifest.status !== 'ROUGH_CUT_READY') process.exitCode = 2;
