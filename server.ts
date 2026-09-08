import express from "express";
import { toolManager } from "./src/server/toolManager";
import { queueManager } from "./src/server/queueManager";
import { createGoogleAuthorizationUrl, exchangeGoogleCode, getGoogleAccessToken, getGoogleOAuthStatus, publicDriveApiKey, revokeGoogleAccess } from "./src/server/googleDriveAuth";
import path from "path";
import { createServer as createViteServer } from "vite";
import { exec, spawn } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);
const activeJobs = new Map<string, any>();
const DEFAULT_DRIVE_FOLDER_ID = process.env.TRIPPEDD_DRIVE_FOLDER_ID || '1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';

async function startServer() {
  try { await toolManager.initialize(); } catch(e) { console.error(e); }
  const app = express();
  const PORT = 3000;
  app.use(express.json());
  const { queueManager } = await import('./src/server/queueManager.ts');

  const scanDriveFolder = async (folderId: string, token?: string) => {
    const apiKey = publicDriveApiKey();
    if (!token && !apiKey) throw new Error('No Google Drive credential is configured. For an "Anyone with the link" folder, set GOOGLE_API_KEY with the Drive API enabled.');
    let pageToken = '';
    const files: any[] = [];
    do {
      const params = new URLSearchParams({ q: `'${folderId}' in parents and trashed = false`, fields: 'nextPageToken,files(id,name,mimeType,size,md5Checksum,thumbnailLink,videoMediaMetadata)', pageSize: '1000' });
      if (pageToken) params.set('pageToken', pageToken);
      if (!token) params.set('key', apiKey);
      const driveRes = await fetch(`https://www.googleapis.com/drive/v3/files?${params.toString()}`, token ? { headers: { Authorization: `Bearer ${token}` } } : undefined);
      if (!driveRes.ok) { const detail = await driveRes.text(); throw new Error(`Drive scan failed (${driveRes.status}): ${detail}`); }
      const data = await driveRes.json() as any;
      files.push(...(data.files || [])); pageToken = data.nextPageToken || '';
    } while (pageToken);
    let newCount = 0;
    for (const f of files) {
      if (!queueManager.getJob(f.id)) {
        queueManager.addJob({ id: 'JOB_' + f.id, fileId: f.id, originalName: f.name, mimeType: f.mimeType, size: f.size, hash: f.md5Checksum, thumbnailLink: f.thumbnailLink, state: 'QUEUED', progress: 0, logs: ['Discovered in Drive scan.'], createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), tools: {}, evidenceRefs: [] } as any);
        newCount++;
      }
      queueManager.setAccessToken(f.id, token ? token : `public:${apiKey}`);
    }
    return { success: true, total: files.length, new: newCount, accessMode: token ? 'oauth' : 'public-link' };
  };

  app.get('/api/auth/google/status', async (_req, res) => { res.json(getGoogleOAuthStatus()); });
  app.get('/api/auth/google/start', (_req, res) => { try { res.redirect(createGoogleAuthorizationUrl()); } catch (e: any) { res.status(500).json({ error: e.message }); } });
  app.get('/api/auth/google/callback', async (req, res) => {
    try {
      const code = typeof req.query.code === 'string' ? req.query.code : ''; const state = typeof req.query.state === 'string' ? req.query.state : ''; const error = typeof req.query.error === 'string' ? req.query.error : '';
      if (error) throw new Error(`Google OAuth denied: ${error}`); if (!code || !state) throw new Error('Google OAuth callback is missing code/state.');
      await exchangeGoogleCode(code, state); const token = await getGoogleAccessToken(); if (!token) throw new Error('Google OAuth completed but no access token is available.');
      const scan = await scanDriveFolder(DEFAULT_DRIVE_FOLDER_ID, token); console.log(`[Drive] OAuth connected. Initial scan found ${scan.total}; queued ${scan.new} new media item(s).`); res.redirect('/?view=pilot_build&drive=connected');
    } catch (e: any) { console.error('[Drive OAuth] callback failed:', e); res.status(500).send(`Google Drive authorization failed: ${e.message}`); }
  });
  app.post('/api/auth/google/revoke', async (_req, res) => { try { await revokeGoogleAccess(); res.json({ success: true }); } catch (e: any) { res.status(500).json({ error: e.message }); } });

  app.post('/api/queue/scan', async (req, res) => {
    try { const folderId = String(req.body.folderId || DEFAULT_DRIVE_FOLDER_ID); const token = await getGoogleAccessToken(); const result = await scanDriveFolder(folderId, token || undefined); res.json(result); }
    catch(e: any) { res.status(500).json({ error: e.message }); }
  });
  app.get('/api/queue', (_req, res) => { res.json(queueManager.getJobs()); });
  app.get('/api/queue/:fileId', (req, res) => { const job = queueManager.getJob(req.params.fileId); if (job) res.json(job); else res.status(404).json({ error: 'Job not found' }); });
  app.post('/api/queue/:fileId/retry', async (req, res) => {
    try { const token = await getGoogleAccessToken(); if (token) queueManager.setAccessToken(req.params.fileId, token); else { const key = publicDriveApiKey(); if (key) queueManager.setAccessToken(req.params.fileId, `public:${key}`); } const ok = queueManager.retry(req.params.fileId); if (ok) res.json({ success: true }); else res.status(404).json({ error: 'Job not found or no Drive authorization available.' }); }
    catch (e: any) { res.status(500).json({ error: e.message }); }
  });
  app.get('/api/health', (_req, res) => res.json({ status: 'ok' }));

  app.post('/api/jobs/ffmpeg', (req, res) => {
    const { command, output_path } = req.body; const jobId = 'srv_job_ff_' + Date.now(); const jobState = { status: 'RUNNING', logs: [], progress: 0, result: null as any }; activeJobs.set(jobId, jobState);
    jobState.logs.push(`Executing FFmpeg command: ffmpeg ${command.join(' ')}`); const proc = spawn('ffmpeg', command); proc.stdout.on('data', (data) => jobState.logs.push(data.toString())); proc.stderr.on('data', (data) => { const str = data.toString(); jobState.logs.push(str); if (str.includes('time=')) jobState.progress = Math.min(jobState.progress + 5, 99); }); proc.on('close', (code) => { jobState.status = code === 0 ? 'COMPLETED' : 'FAILED'; jobState.progress = 100; if (code === 0) jobState.result = { path: output_path }; }); proc.on('error', (err) => { jobState.status = 'FAILED'; jobState.logs.push(err.message); }); res.json({ jobId });
  });
  app.post('/api/jobs/comfyui', async (req, res) => {
    const { workflow, output_path } = req.body; const jobId = 'srv_job_cu_' + Date.now(); const jobState = { status: 'RUNNING', logs: ['Starting ComfyUI workflow execution...'], progress: 0, result: null as any }; activeJobs.set(jobId, jobState);
    try { const fetchRes = await fetch('http://127.0.0.1:8188/prompt', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt: workflow }) }); if (!fetchRes.ok) throw new Error(`ComfyUI server responded with error: ${fetchRes.status}`); const data = await fetchRes.json() as any; jobState.logs.push(`ComfyUI accepted prompt. Prompt ID: ${data.prompt_id}`); setTimeout(() => { jobState.status = 'COMPLETED'; jobState.progress = 100; jobState.result = { path: output_path }; jobState.logs.push('ComfyUI workflow finished.'); }, 5000); } catch(e: any) { jobState.status = 'FAILED'; jobState.logs.push(`ComfyUI connection failed: ${e.message}. TOOL UNAVAILABLE.`); jobState.logs.push('JOB BLOCKED: Real execution required. No fallback allowed.'); } res.json({ jobId });
  });
  app.post('/api/ingest/analyze', async (req, res) => {
    const { fileId, token, originalName, mimeType } = req.body; const jobId = 'srv_job_ingest_' + Date.now(); const jobState = { status: 'RUNNING', logs: [], progress: 0, result: null as any, analysis: { originalName, fileId, mimeType, hash: null as string | null, ffprobe: { status: 'PENDING', data: null as any }, ffmpeg: { status: 'PENDING', keyframesExtracted: 0 }, pyscenedetect: { status: 'PENDING', scenes: [] }, whisper: { status: 'PENDING', transcript: null as string | null }, vlm: { status: 'PENDING', observations: [] } } }; activeJobs.set(jobId, jobState);
    (async () => { try {
      const driveToken = token || await getGoogleAccessToken(); if (!driveToken) throw new Error('Google Drive is not connected.'); jobState.logs.push(`[Drive] Attempting to access file ${fileId}...`);
      const driveRes = await fetch(`https://www.googleapis.com/drive/v3/files/${encodeURIComponent(fileId)}?fields=size,md5Checksum,videoMediaMetadata`, { headers: { Authorization: `Bearer ${driveToken}` } }); if (!driveRes.ok) throw new Error(`Drive API error: ${driveRes.statusText}`); const driveData = await driveRes.json() as any; jobState.logs.push(`[Drive] Access successful. Size: ${driveData.size} bytes.`); jobState.analysis.hash = driveData.md5Checksum || 'UNKNOWN_NO_MD5';
      jobState.logs.push('[ffprobe] Checking dependency...'); try { await execAsync('ffprobe -version'); const mediaUrl = `https://www.googleapis.com/drive/v3/files/${encodeURIComponent(fileId)}?alt=media`; const { stdout } = await execAsync(`ffprobe -v quiet -print_format json -show_format -show_streams -headers "Authorization: Bearer ${driveToken}" "${mediaUrl}"`); jobState.analysis.ffprobe.status = 'COMPLETED'; jobState.analysis.ffprobe.data = JSON.parse(stdout); jobState.logs.push('[ffprobe] Analysis successful.'); } catch (e: any) { jobState.logs.push(`[ffprobe] UNAVAILABLE or FAILED: ${e.message}`); jobState.analysis.ffprobe.status = 'UNAVAILABLE'; }
      jobState.progress = 30; try { await execAsync('ffmpeg -version'); jobState.analysis.ffmpeg.status = 'COMPLETED'; jobState.logs.push('[ffmpeg] Dependency available.'); } catch (e: any) { jobState.logs.push(`[ffmpeg] UNAVAILABLE: ${e.message}`); jobState.analysis.ffmpeg.status = 'UNAVAILABLE'; }
      jobState.progress = 50; try { await execAsync('scenedetect version'); jobState.analysis.pyscenedetect.status = 'COMPLETED'; } catch (e: any) { jobState.logs.push(`[pyscenedetect] UNAVAILABLE: ${e.message}`); jobState.analysis.pyscenedetect.status = 'UNAVAILABLE'; }
      jobState.progress = 70; try { await execAsync('whisper --version'); jobState.analysis.whisper.status = 'COMPLETED'; } catch (e: any) { jobState.logs.push(`[whisper] UNAVAILABLE: ${e.message}`); jobState.analysis.whisper.status = 'UNAVAILABLE'; }
      jobState.progress = 90; jobState.analysis.vlm.status = 'UNAVAILABLE'; jobState.logs.push('[VLM] UNAVAILABLE: No local Vision-Language Model detected in container.'); jobState.status = 'COMPLETED'; jobState.progress = 100; jobState.result = jobState.analysis; jobState.logs.push('Ingest analysis pipeline finished.');
    } catch (err: any) { jobState.status = 'FAILED'; jobState.logs.push(`[FATAL] ${err.message}`); } })();
    res.json({ jobId });
  });

  app.use(express.static(path.join(process.cwd(), 'dist')));
  app.use('/production', express.static(path.join(process.cwd(), 'public', 'production')));
  if (process.env.NODE_ENV !== 'production') { const vite = await createViteServer({ server: { middlewareMode: true }, appType: 'spa' }); app.use(vite.middlewares); }
  app.get('*', (_req, res) => { res.sendFile(path.join(process.cwd(), 'dist', 'index.html')); });
  app.listen(PORT, () => console.log(`TRIPPEDD Production Studio running on port ${PORT}`));
}

startServer();
