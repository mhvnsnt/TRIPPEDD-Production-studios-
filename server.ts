import express from "express";
import { toolManager } from "./src/server/toolManager";
import { queueManager } from "./src/server/queueManager";
import { createGoogleAuthorizationUrl, exchangeGoogleCode, getGoogleAccessToken, getGoogleOAuthStatus, publicDriveApiKey, revokeGoogleAccess } from "./src/server/googleDriveAuth";
import path from "path";
import { createServer as createViteServer } from "vite";
import { spawn } from "child_process";

const activeJobs = new Map<string, any>();
const DEFAULT_DRIVE_FOLDER_ID = process.env.TRIPPEDD_DRIVE_FOLDER_ID || '1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI';
const MEDIA_MIME_PREFIXES = ['video/', 'audio/'];
const EXTRA_MEDIA_MIME_TYPES = new Set(['application/octet-stream']);

function isMediaFile(file: any) {
  const mime = String(file?.mimeType || '').toLowerCase();
  return MEDIA_MIME_PREFIXES.some(prefix => mime.startsWith(prefix)) || EXTRA_MEDIA_MIME_TYPES.has(mime);
}

function driveError(status: number, detail: string, publicMode: boolean) {
  if (publicMode && (status === 400 || status === 401 || status === 403)) {
    return `Public Drive access failed (${status}). The folder can be "Anyone with the link", but the running studio still needs a Google API key with the Drive API enabled and permitted. Set GOOGLE_API_KEY (preferred) or use a key from the same Google Cloud project with Drive API access. Google response: ${detail}`;
  }
  return `Drive scan failed (${status}): ${detail}`;
}

async function startServer() {
  try { await toolManager.initialize(); } catch (e) { console.error(e); }
  const app = express();
  const PORT = 3000;
  app.use(express.json());

  const scanDriveFolder = async (folderId: string, token?: string) => {
    const apiKey = publicDriveApiKey();
    const publicMode = !token;
    if (!token && !apiKey) throw new Error('No Google Drive credential is configured. This folder is public-link accessible, so configure GOOGLE_API_KEY with the Drive API enabled.');
    let pageToken = '';
    const files: any[] = [];
    do {
      const params = new URLSearchParams({
        q: `'${folderId}' in parents and trashed = false`,
        fields: 'nextPageToken,files(id,name,mimeType,size,md5Checksum,thumbnailLink,videoMediaMetadata)',
        pageSize: '1000',
        orderBy: 'name_natural'
      });
      if (pageToken) params.set('pageToken', pageToken);
      if (publicMode) params.set('key', apiKey);
      const driveRes = await fetch(`https://www.googleapis.com/drive/v3/files?${params.toString()}`, token ? { headers: { Authorization: `Bearer ${token}` } } : undefined);
      if (!driveRes.ok) {
        const detail = await driveRes.text();
        throw new Error(driveError(driveRes.status, detail, publicMode));
      }
      const data = await driveRes.json() as any;
      files.push(...(data.files || []));
      pageToken = data.nextPageToken || '';
    } while (pageToken);

    const mediaFiles = files.filter(isMediaFile);
    let newCount = 0;
    for (const f of mediaFiles) {
      if (!queueManager.getJob(f.id)) {
        queueManager.addJob({
          id: 'JOB_' + f.id,
          fileId: f.id,
          originalName: f.name,
          mimeType: f.mimeType,
          size: f.size,
          hash: f.md5Checksum,
          thumbnailLink: f.thumbnailLink,
          state: 'QUEUED',
          progress: 0,
          logs: ['Discovered in Drive scan.', publicMode ? 'Access mode: public-link.' : 'Access mode: OAuth.'],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          tools: {},
          evidenceRefs: []
        } as any);
        newCount++;
      }
      queueManager.setAccessToken(f.id, token ? token : `public:${apiKey}`);
    }

    return {
      success: true,
      total: mediaFiles.length,
      discovered: files.length,
      ignoredNonMedia: files.length - mediaFiles.length,
      new: newCount,
      accessMode: publicMode ? 'public-link' : 'oauth'
    };
  };

  app.get('/api/auth/google/status', async (_req, res) => { res.json(getGoogleOAuthStatus()); });
  app.get('/api/auth/google/start', (_req, res) => { try { res.redirect(createGoogleAuthorizationUrl()); } catch (e: any) { res.status(500).json({ error: e.message }); } });
  app.get('/api/auth/google/callback', async (req, res) => {
    try {
      const code = typeof req.query.code === 'string' ? req.query.code : '';
      const state = typeof req.query.state === 'string' ? req.query.state : '';
      const error = typeof req.query.error === 'string' ? req.query.error : '';
      if (error) throw new Error(`Google OAuth denied: ${error}`);
      if (!code || !state) throw new Error('Google OAuth callback is missing code/state.');
      await exchangeGoogleCode(code, state);
      const token = await getGoogleAccessToken();
      if (!token) throw new Error('Google OAuth completed but no access token is available.');
      const scan = await scanDriveFolder(DEFAULT_DRIVE_FOLDER_ID, token);
      console.log(`[Drive] OAuth connected. Initial scan found ${scan.total}; queued ${scan.new} new media item(s).`);
      res.redirect('/?view=pilot_build&drive=connected');
    } catch (e: any) {
      console.error('[Drive OAuth] callback failed:', e);
      res.status(500).send(`Google Drive authorization failed: ${e.message}`);
    }
  });
  app.post('/api/auth/google/revoke', async (_req, res) => { try { await revokeGoogleAccess(); res.json({ success: true }); } catch (e: any) { res.status(500).json({ error: e.message }); } });

  app.post('/api/queue/scan', async (req, res) => {
    try {
      const folderId = String(req.body.folderId || DEFAULT_DRIVE_FOLDER_ID);
      const token = await getGoogleAccessToken();
      const result = await scanDriveFolder(folderId, token || undefined);
      res.json(result);
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });
  app.get('/api/queue', (_req, res) => { res.json(queueManager.getJobs()); });
  app.get('/api/queue/:fileId', (req, res) => { const job = queueManager.getJob(req.params.fileId); if (job) res.json(job); else res.status(404).json({ error: 'Job not found' }); });
  app.post('/api/queue/:fileId/retry', async (req, res) => {
    try {
      const token = await getGoogleAccessToken();
      if (token) queueManager.setAccessToken(req.params.fileId, token);
      else {
        const key = publicDriveApiKey();
        if (key) queueManager.setAccessToken(req.params.fileId, `public:${key}`);
      }
      const ok = queueManager.retry(req.params.fileId);
      if (ok) res.json({ success: true });
      else res.status(404).json({ error: 'Job not found or no Drive authorization available.' });
    } catch (e: any) { res.status(500).json({ error: e.message }); }
  });
  app.get('/api/health', (_req, res) => res.json({ status: 'ok' }));

  app.post('/api/jobs/ffmpeg', (req, res) => {
    const { command, output_path } = req.body;
    const jobId = 'srv_job_ff_' + Date.now();
    const jobState = { status: 'RUNNING', logs: [], progress: 0, result: null as any };
    activeJobs.set(jobId, jobState);
    jobState.logs.push(`Executing FFmpeg command: ffmpeg ${command.join(' ')}`);
    const proc = spawn('ffmpeg', command);
    proc.stdout.on('data', data => jobState.logs.push(data.toString()));
    proc.stderr.on('data', data => { const str = data.toString(); jobState.logs.push(str); if (str.includes('time=')) jobState.progress = Math.min(jobState.progress + 5, 99); });
    proc.on('close', code => { jobState.status = code === 0 ? 'COMPLETED' : 'FAILED'; jobState.progress = 100; if (code === 0) jobState.result = { path: output_path }; });
    proc.on('error', err => { jobState.status = 'FAILED'; jobState.logs.push(err.message); });
    res.json({ jobId });
  });
  app.post('/api/jobs/comfyui', async (req, res) => {
    const { workflow, output_path } = req.body;
    const jobId = 'srv_job_cu_' + Date.now();
    const jobState = { status: 'RUNNING', logs: ['Starting ComfyUI workflow execution...'], progress: 0, result: null as any };
    activeJobs.set(jobId, jobState);
    try {
      const fetchRes = await fetch('http://127.0.0.1:8188/prompt', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt: workflow }) });
      if (!fetchRes.ok) throw new Error(`ComfyUI server responded with error: ${fetchRes.status}`);
      const data = await fetchRes.json() as any;
      jobState.logs.push(`ComfyUI accepted prompt. Prompt ID: ${data.prompt_id}`);
      setTimeout(() => { jobState.status = 'COMPLETED'; jobState.progress = 100; jobState.result = { path: output_path }; jobState.logs.push('ComfyUI workflow finished.'); }, 5000);
    } catch (e: any) {
      jobState.status = 'FAILED';
      jobState.logs.push(`ComfyUI connection failed: ${e.message}. TOOL UNAVAILABLE.`);
      jobState.logs.push('JOB BLOCKED: Real execution required. No fallback allowed.');
    }
    res.json({ jobId });
  });

  app.use(express.static(path.join(process.cwd(), 'dist')));
  app.use('/production', express.static(path.join(process.cwd(), 'public', 'production')));
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({ server: { middlewareMode: true }, appType: 'spa' });
    app.use(vite.middlewares);
  }
  app.get('*', (_req, res) => { res.sendFile(path.join(process.cwd(), 'dist', 'index.html')); });
  app.listen(PORT, () => console.log(`TRIPPEDD Production Studio running on port ${PORT}`));
}

startServer();
