import fs from 'fs/promises';
import path from 'path';
import { downloadPublicDriveFolder } from '../src/server/publicDriveFolder';
import { queueManager } from '../src/server/queueManager';
import { toolManager } from '../src/server/toolManager';
import { buildEp01FirstAssembly } from '../src/server/pilotRenderer';

const folderUrl = process.env.TRIPPEDD_DRIVE_FOLDER_URL || 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const cacheRoot = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media'));
const mediaExtensions = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp', '.wav', '.mp3', '.m4a']);
const cutMode = process.env.TRIPPEDD_CUT_MODE === 'AUTONOMOUS' ? 'AUTONOMOUS' : 'SHOWRUNNER';

async function waitForJob(fileId: string) {
  for (;;) {
    const job = queueManager.getJob(fileId);
    if (!job) throw new Error(`Job disappeared: ${fileId}`);
    if (job.state === 'NEEDS_REVIEW' || job.state === 'EVIDENCE_READY' || job.state === 'FAILED') return job;
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}

async function main() {
  await toolManager.initialize();
  await fs.mkdir(cacheRoot, { recursive: true });
  console.log(`[EP01/${cutMode}] Downloading public Drive folder without API key: ${folderUrl}`);
  const downloaded = await downloadPublicDriveFolder(folderUrl, cacheRoot);
  const media = downloaded.filter(file => mediaExtensions.has(path.extname(file).toLowerCase()));
  console.log(`[EP01/${cutMode}] Downloaded ${media.length} media file(s).`);
  if (!media.length) throw new Error('The public Drive folder produced no supported media files.');

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

  const results = await Promise.all(jobs.map(fileId => waitForJob(fileId)));
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
  console.log(`[EP01/${cutMode}] Analysis batch complete: ${usable}/${jobs.length} source jobs usable.`);
  if (!usable) throw new Error(`All ${jobs.length} source analyses failed; refusing to manufacture an assembly from missing evidence.`);

  const manifest = await buildEp01FirstAssembly({ maxClips: Number(process.env.EP01_MAX_CLIPS || 24), clipPaddingSeconds: Number(process.env.EP01_CLIP_PADDING || 1.25) });
  console.log(JSON.stringify(manifest, null, 2));
  if (manifest.status !== 'ROUGH_CUT_READY') process.exitCode = 2;
}

main().catch(error => { console.error(error); process.exitCode = 1; });
