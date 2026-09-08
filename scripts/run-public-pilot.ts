import fs from 'fs/promises';
import path from 'path';
import { downloadPublicDriveFolder } from '../src/server/publicDriveFolder';
import { queueManager } from '../src/server/queueManager';
import { toolManager } from '../src/server/toolManager';
import { buildEp01FirstAssembly } from '../src/server/pilotRenderer';

const folderUrl = process.env.TRIPPEDD_DRIVE_FOLDER_URL || 'https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const cacheRoot = path.resolve(process.env.TRIPPEDD_MEDIA_CACHE || path.join(process.cwd(), '.trippedd', 'media'));
const mediaExtensions = new Set(['.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv', '.mpg', '.mpeg', '.3gp', '.wav', '.mp3', '.m4a']);

async function waitForJob(fileId: string) {
  for (;;) {
    const job = queueManager.getJob(fileId);
    if (!job) throw new Error(`Job disappeared: ${fileId}`);
    if (job.state === 'NEEDS_REVIEW' || job.state === 'EVIDENCE_READY') return job;
    if (job.state === 'FAILED') throw new Error(`Media job failed for ${job.originalName}:\n${job.logs.slice(-12).join('\n')}`);
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}

async function main() {
  await toolManager.initialize();
  await fs.mkdir(cacheRoot, { recursive: true });
  console.log(`[EP01] Downloading public Drive folder without API key: ${folderUrl}`);
  const downloaded = await downloadPublicDriveFolder(folderUrl, cacheRoot);
  const media = downloaded.filter(file => mediaExtensions.has(path.extname(file).toLowerCase()));
  console.log(`[EP01] Downloaded ${media.length} media file(s).`);
  if (!media.length) throw new Error('The public Drive folder produced no supported media files.');

  const jobs: string[] = [];
  for (const filePath of media) {
    const fileId = `PUBLIC_${Buffer.from(path.resolve(filePath)).toString('base64url').slice(-48)}`;
    const stat = await fs.stat(filePath);
    // Register the local source before queueing the job. QueueManager also guards
    // against the inverse order, but this is the canonical race-free path.
    queueManager.setLocalSource(fileId, filePath);
    if (!queueManager.getJob(fileId)) {
      queueManager.addJob({ id: `JOB_${fileId}`, fileId, originalName: path.basename(filePath), mimeType: 'video/*', size: stat.size, state: 'QUEUED', progress: 0, logs: ['Credential-free public Drive source.', `Local source: ${filePath}`], createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), tools: {}, evidenceRefs: [] } as any);
    } else {
      queueManager.setLocalSource(fileId, filePath);
    }
    jobs.push(fileId);
  }

  for (const fileId of jobs) {
    const job = await waitForJob(fileId);
    console.log(`[EP01] Analyzed ${job.originalName}`);
  }

  const manifest = await buildEp01FirstAssembly({ maxClips: Number(process.env.EP01_MAX_CLIPS || 24), clipPaddingSeconds: Number(process.env.EP01_CLIP_PADDING || 1.25) });
  console.log(JSON.stringify(manifest, null, 2));
  if (manifest.status !== 'ROUGH_CUT_READY') process.exitCode = 2;
}

main().catch(error => { console.error(error); process.exitCode = 1; });
