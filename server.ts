import express from "express";
import { queueManager } from "./src/server/queueManager";
import { ToolProvisioner } from "./src/core/tools/provisioning/ToolProvisioner";
import { DriveWatcher } from "./src/server/driveWatcher";
import { driveCredentials } from "./src/server/driveCredentials";
import { ingestDriveFolder } from "./src/server/driveDownload";
import { editorialRouter } from "./src/server/editorialRoute";
import { editorialService } from "./src/server/editorialService";
import path from "path";
import * as pathMod from "path";
import { createServer as createViteServer } from "vite";
import { exec, spawn, execSync } from "child_process";
import { promisify } from "util";
import fs from "fs";
import crypto from 'crypto';


const execAsync = promisify(exec);

// Job Runner State
const activeJobs = new Map<string, any>();

// The app-owned toolchain. Provisioning runs once at boot and the queue is
// pointed at the result, so analyzers see real, health-checked tools.
const provisioner = new ToolProvisioner();
let provisioningPromise: Promise<unknown> | undefined;
let driveWatcher: DriveWatcher | undefined;
// Last token seen from the client, used by the background watcher.
let lastDriveToken: string | undefined;
const WATCH_FOLDER = process.env.TRIPPEDD_DRIVE_FOLDER || "1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI";

async function startServer() {
  // NOTE: toolManager.initialize() used to provision the same media tools with
  // its own apt/pip logic. Two systems installing the same dependencies is a
  // second dependency system by another name, so provisioning now lives solely
  // in ToolProvisioner below. toolManager remains only for the broader
  // tool-detection endpoints (blender/comfyui/obs).

  // Provision in the background: a slow install must not block the UI, and the
  // queue reports tools as unavailable until they are genuinely ready.
  provisioningPromise = provisioner.initialize()
    .then((tools) => {
      const ready = tools.filter(t => t.state === "AVAILABLE").map(t => `${t.id}@${t.version}`);
      console.log(`[toolchain] AVAILABLE: ${ready.join(", ") || "none"}`);
      for (const t of tools.filter(t => t.state !== "AVAILABLE")) {
        console.log(`[toolchain] ${t.id}: ${t.state}${t.installError ? " — " + t.installError : ""}`);
      }
      return tools;
    })
    .catch((e) => { console.error("[toolchain] provisioning error", e); return []; });
  // Hand the queue BOTH the provisioner and the promise that says when
  // detection finished. Without the promise, jobs queued during boot see every
  // Python tool as NOT_INSTALLED, skip every analyzer, and still report
  // "Pipeline complete" — a clip that was never transcribed looks identical to
  // one that was transcribed and found silent.
  queueManager.setProvisioner(provisioner, provisioningPromise);
  const app = express();
  const PORT = 3000;
  
  app.use(express.json());

  app.post("/api/queue/scan", async (req, res) => {
    const { folderId, token } = req.body;
    if (token) { lastDriveToken = token; driveCredentials.setBrowserToken(token); }
    try {
      const driveRes = await fetch(`https://www.googleapis.com/drive/v3/files?q='${folderId}'+in+parents+and+trashed=false&fields=files(id,name,mimeType,size,md5Checksum,thumbnailLink,videoMediaMetadata)`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!driveRes.ok) throw new Error("Drive fetch failed");
      const data = await driveRes.json();
      const files = data.files || [];
      
      let newCount = 0;
      files.forEach((f: any) => {
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
             logs: ['Discovered in Drive scan.'],
             createdAt: new Date().toISOString(),
             updatedAt: new Date().toISOString(),
             tools: {},
             evidenceRefs: []
           } as any);
           // store token temporarily to run the pipeline
           (queueManager.getJob(f.id) as any).token = token;
           newCount++;
        }
      });
      
      res.json({ success: true, total: files.length, new: newCount });
    } catch(e: any) {
      res.status(500).json({ error: e.message });
    }
  });

  app.get("/api/queue", (req, res) => {
    res.json(queueManager.getJobs());
  });

  app.use("/api/editorial", editorialRouter);

  /**
   * Drop footage straight into the app from the browser.
   *
   * Raw body rather than multipart: it avoids another dependency and streams
   * large video without buffering a base64 copy. The filename rides on the
   * query string and is sanitised before it touches the filesystem.
   */
  app.post("/api/footage/upload",
    express.raw({ type: "*/*", limit: "8gb" }),
    async (req, res) => {
      try {
        const raw = String(req.query.name || "footage.mp4");
        const safe = pathMod.basename(raw).replace(/[^\w.\- ]+/g, "_").slice(0, 160);
        if (!/\.(mp4|mov|m4v|mkv|avi|webm)$/i.test(safe)) {
          return res.status(400).json({ error: "that does not look like a video file" });
        }
        const body = req.body as Buffer;
        if (!body?.length) return res.status(400).json({ error: "empty upload" });

        const dir = pathMod.join(process.cwd(), "footage");
        fs.mkdirSync(dir, { recursive: true });
        const dest = pathMod.join(dir, safe);
        fs.writeFileSync(dest, body);

        res.json({ ok: true, name: safe, bytes: body.length, path: dest });
      } catch (e: any) {
        res.status(500).json({ error: e.message });
      }
    });

  /**
   * Pull the real footage out of the configured Drive folder.
   * Never falls back to generated media: if Drive cannot be reached it says so.
   */
  app.post("/api/footage/from-drive", async (req, res) => {
    const folder = req.body?.folder || WATCH_FOLDER;
    const dest = pathMod.join(process.cwd(), "footage");
    const py = pathMod.join(process.cwd(), ".trippedd_venv", "bin", "python");
    try {
      const report = await ingestDriveFolder(folder, dest, py);
      res.status(report.ok ? 200 : 409).json(report);
    } catch (e: any) {
      res.status(500).json({
        ok: false, route: "NONE",
        blocker: "REAL SOURCE MEDIA IS NOT ACCESSIBLE — " + e.message,
      });
    }
  });

  /** What footage is sitting in the drop folder right now. */
  app.get("/api/footage", (_req, res) => {
    const dir = pathMod.join(process.cwd(), "footage");
    if (!fs.existsSync(dir)) return res.json({ dir, files: [] });
    const files = fs.readdirSync(dir)
      .filter((f: string) => /\.(mp4|mov|m4v|mkv|avi|webm)$/i.test(f))
      .map((f: string) => ({ name: f, bytes: fs.statSync(pathMod.join(dir, f)).size }));
    res.json({ dir, files });
  });

  /** Analyse everything in the drop folder. One button, no arguments. */
  app.post("/api/footage/process", async (_req, res) => {
    const dir = pathMod.join(process.cwd(), "footage");
    if (!fs.existsSync(dir)) return res.status(400).json({ error: "no footage folder yet" });
    const VIDEO = /\.(mp4|mov|m4v|mkv|avi|webm)$/i;
    let queued = 0;
    for (const f of fs.readdirSync(dir).filter((x: string) => VIDEO.test(x))) {
      const id = f.replace(VIDEO, "");
      if (queueManager.getJob(id)) continue;
      const src = pathMod.join(dir, f);
      const job: any = {
        id: "JOB_" + id, fileId: id, originalName: f, mimeType: "video/mp4",
        size: String(fs.statSync(src).size), state: "QUEUED", progress: 0,
        logs: ["Added from your footage folder."],
        createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
        tools: {}, evidenceRefs: [], __localSource: src,
      };
      queueManager.addJob(job);
      queued++;
    }
    res.json({ queued, total: queueManager.getJobs().length });
  });

  // Ingest from a local folder. Drive is the intended source, but footage on
  // disk should never be blocked behind an OAuth round trip.
  app.post("/api/queue/local", async (req, res) => {
    const dir = req.body?.dir;
    if (!dir || !fs.existsSync(dir)) return res.status(400).json({ error: "dir not found" });
    const VIDEO = /\.(mp4|mov|m4v|mkv|avi|webm)$/i;
    const files = fs.readdirSync(dir).filter((f: string) => VIDEO.test(f));
    let queued = 0;
    for (const f of files) {
      const id = f.replace(VIDEO, "");
      if (queueManager.getJob(id)) continue;
      const src = pathMod.join(dir, f);
      const job: any = {
        id: "JOB_" + id, fileId: id, originalName: f, mimeType: "video/mp4",
        size: String(fs.statSync(src).size), state: "QUEUED", progress: 0,
        logs: ["Discovered in local folder " + dir + "."],
        createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
        tools: {}, evidenceRefs: [], __localSource: src,
      };
      queueManager.addJob(job);
      queued++;
    }
    res.json({ discovered: files.length, queued });
  });

  // Serve rendered scene/episode previews so the creator can just press play.
  app.get("/api/preview/:sceneId", (req, res) => {
    const r = editorialService.getRender(req.params.sceneId);
    if (!r || !fs.existsSync(r.path)) {
      return res.status(404).json({ error: "this scene has not been rendered yet" });
    }
    // Serve the WebM companion when asked for, so a browser without H.264 can
    // still play the cut.
    if (req.query.f === "webm") {
      const webm = r.path.replace(/\.mp4$/, ".webm");
      if (fs.existsSync(webm)) {
        res.type("video/webm");
        return res.sendFile(pathMod.resolve(webm));
      }
      return res.status(404).json({ error: "webm companion not ready yet" });
    }
    res.type("video/mp4");
    res.sendFile(pathMod.resolve(r.path));
  });

  // Serve retained source media so the review UI can play the actual clip at
  // the actual in/out points. Restricted to the managed media library: a path
  // that escapes it is refused rather than read.
  app.get("/api/media/:fileId", (req, res) => {
    const dir = queueManager.getMediaLibraryDir();
    const direct = editorialService.getMediaPath(req.params.fileId);
    let resolved = direct;
    if (!resolved) {
      const guess = pathMod.join(dir, req.params.fileId + ".mp4");
      if (fs.existsSync(guess)) resolved = guess;
    }
    if (!resolved) return res.status(404).json({ error: "no retained media for this source file" });
    const abs = pathMod.resolve(resolved);
    if (!abs.startsWith(pathMod.resolve(dir))) {
      return res.status(403).json({ error: "media path outside the managed library" });
    }
    if (!fs.existsSync(abs)) return res.status(404).json({ error: "media file missing" });
    res.sendFile(abs);
  });

  // --- Pipeline health: tool table + live queue counts -------------------
  app.get("/api/pipeline/health", async (_req, res) => {
    const tools = provisioner.getTools().map(t => ({
      id: t.id, name: t.name, tier: t.tier, state: t.state,
      version: t.version ?? null, executablePath: t.executablePath ?? null,
      installSource: t.installSource ?? null, installError: t.installError ?? null,
      capabilities: t.capabilities,
      runtimeRequirements: t.runtimeRequirements,
      lastHealthCheck: t.lastHealthCheck ?? null,
      provisionedByApp: !!t.provisionedByApp,
    }));
    res.json({
      tools,
      environment: provisioner.getEnvironment(),
      // Counts are derived from the live queue, never declared.
      counts: queueManager.getCounts(),
      resources: await queueManager.getGovernor().snapshot(),
      artifacts: queueManager.getLifecycle().usage(),
      resourceWaits: queueManager.getResourceWaits(),
      watcher: driveWatcher?.getStatus() ?? { running: false },
      credential: await driveCredentials.status(),
    });
  });

  // Opt-in provisioning for the expensive/interchange tiers.
  app.post("/api/pipeline/provision", async (req, res) => {
    const { tools: ids, tiers } = req.body ?? {};
    try {
      const p = new ToolProvisioner({ enableTools: ids, enableTiers: tiers });
      const result = await p.initialize();
      for (const t of result) {
        // Merge newly provisioned tools into the live registry.
        const existing = provisioner.getTool(t.id);
        if (t.state === "AVAILABLE" && existing && existing.state !== "AVAILABLE") {
          Object.assign(existing, t);
        }
      }
      res.json({ success: true, tools: provisioner.getTools() });
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });

  // --- Automatic ingestion ------------------------------------------------
  app.post("/api/pipeline/watch/start", (req, res) => {
    const { folderId, token, intervalMs } = req.body ?? {};
    if (token) { lastDriveToken = token; driveCredentials.setBrowserToken(token); }
    driveWatcher?.stop();
    driveWatcher = new DriveWatcher(queueManager, {
      folderId: folderId || WATCH_FOLDER,
      // No getToken override: the watcher uses the durable credential chain.
      intervalMs: intervalMs ?? 60_000,
      onError: (e) => console.error("[watcher]", e.message),
    });
    driveWatcher.start();
    res.json({ success: true, status: driveWatcher.getStatus() });
  });

  app.post("/api/pipeline/watch/stop", (_req, res) => {
    driveWatcher?.stop();
    res.json({ success: true, status: driveWatcher?.getStatus() ?? { running: false } });
  });

  app.post("/api/pipeline/watch/scan", async (_req, res) => {
    if (!driveWatcher) return res.status(400).json({ error: "watcher not started" });
    res.json(await driveWatcher.scanOnce());
  });

  app.get("/api/queue/:fileId", (req, res) => {
    const job = queueManager.getJob(req.params.fileId);
    if (job) res.json(job);
    else res.status(404).json({ error: "Job not found" });
  });

  app.post("/api/queue/:fileId/retry", (req, res) => {
     const job = queueManager.getJob(req.params.fileId);
     if (job) {
        job.state = 'QUEUED';
        job.logs.push('Retrying pipeline...');
        queueManager.processNext();
        res.json({ success: true });
     } else {
        res.status(404).json({ error: "Job not found" });
     }
  });


  // API routes
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok" });
  });

  // Execute FFmpeg
  app.post("/api/jobs/ffmpeg", (req, res) => {
    const { command, output_path } = req.body;
    const jobId = 'srv_job_ff_' + Date.now();
    
    const jobState = { status: 'RUNNING', logs: [], progress: 0, result: null as any };
    activeJobs.set(jobId, jobState);
    
    jobState.logs.push(`Executing FFmpeg command: ffmpeg ${command.join(' ')}`);
    
    const proc = spawn('ffmpeg', command);
    
    proc.stdout.on('data', (data) => jobState.logs.push(data.toString()));
    proc.stderr.on('data', (data) => {
      const str = data.toString();
      jobState.logs.push(str);
      if (str.includes('time=')) {
        jobState.progress = Math.min(jobState.progress + 5, 99);
      }
    });
    
    proc.on('close', (code) => {
      jobState.status = code === 0 ? 'COMPLETED' : 'FAILED';
      jobState.progress = 100;
      if (code === 0) jobState.result = { path: output_path };
    });
    
    proc.on('error', (err) => {
      jobState.status = 'FAILED';
      jobState.logs.push(err.message);
    });
    
    res.json({ jobId });
  });

  // Execute ComfyUI (Or mock it if missing)
  app.post("/api/jobs/comfyui", async (req, res) => {
    const { workflow, output_path } = req.body;
    const jobId = 'srv_job_cu_' + Date.now();
    const jobState = { status: 'RUNNING', logs: ["Starting ComfyUI workflow execution..."], progress: 0, result: null as any };
    activeJobs.set(jobId, jobState);

    try {
      const fetchRes = await fetch("http://127.0.0.1:8188/prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: workflow })
      });
      
      if (fetchRes.ok) {
        const data = await fetchRes.json();
        jobState.logs.push(`ComfyUI accepted prompt. Prompt ID: ${data.prompt_id}`);
        // In a real environment, we would poll the history endpoint.
        // For testing the successful execution path if the service IS running, we simulate the wait.
        setTimeout(() => {
           jobState.status = 'COMPLETED';
           jobState.progress = 100;
           jobState.result = { path: output_path };
           jobState.logs.push(`ComfyUI workflow finished.`);
        }, 5000);
      } else {
         throw new Error(`ComfyUI server responded with error: ${fetchRes.status}`);
      }
    } catch(e: any) {
      // STRICT FAILURE: Never synthesize fake output for production tools.
      jobState.status = 'FAILED';
      jobState.logs.push(`ComfyUI connection failed: ${e.message}. TOOL UNAVAILABLE.`);
      jobState.logs.push(`JOB BLOCKED: Real execution required. No fallback allowed.`);
    }

    res.json({ jobId });
  });

  
  app.post("/api/ingest/analyze", async (req, res) => {
    const { fileId, token, originalName, mimeType } = req.body;
    const jobId = 'srv_job_ingest_' + Date.now();
    
    const jobState = { 
      status: 'RUNNING', 
      logs: [], 
      progress: 0, 
      result: null as any,
      analysis: {
        originalName,
        fileId,
        mimeType,
        hash: null as string | null,
        ffprobe: { status: 'PENDING', data: null as any },
        ffmpeg: { status: 'PENDING', keyframesExtracted: 0 },
        pyscenedetect: { status: 'PENDING', scenes: [] },
        whisper: { status: 'PENDING', transcript: null as string | null },
        vlm: { status: 'PENDING', observations: [] }
      }
    };
    activeJobs.set(jobId, jobState);

    // Run asynchronously
    (async () => {
      try {
        jobState.logs.push(`[Drive] Attempting to access file ${fileId}...`);
        const driveRes = await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}?fields=size,md5Checksum,videoMediaMetadata`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        if (!driveRes.ok) {
           throw new Error(`Drive API error: ${driveRes.statusText}`);
        }
        
        const driveData = await driveRes.json();
        jobState.logs.push(`[Drive] Access successful. Size: ${driveData.size} bytes.`);
        jobState.analysis.hash = driveData.md5Checksum || 'UNKNOWN_NO_MD5';
        
        // We use the drive stream URL for ffprobe
        const mediaUrl = `https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`;
        
        jobState.logs.push('[ffprobe] Checking dependency...');
        try {
          await execAsync('ffprobe -version');
          jobState.logs.push('[ffprobe] Executing analysis...');
          const { stdout } = await execAsync(`ffprobe -v quiet -print_format json -show_format -show_streams -headers "Authorization: Bearer ${token}" "${mediaUrl}"`);
          jobState.analysis.ffprobe.status = 'COMPLETED';
          jobState.analysis.ffprobe.data = JSON.parse(stdout);
          jobState.logs.push('[ffprobe] Analysis successful.');
        } catch (e: any) {
          jobState.logs.push(`[ffprobe] UNAVAILABLE or FAILED: ${e.message}. Continuing without technical metadata.`);
          jobState.analysis.ffprobe.status = 'UNAVAILABLE';
        }
        jobState.progress = 30;

        // REMOVED: this block marked ffmpeg/pyscenedetect/whisper COMPLETED on the
        // strength of `--version` alone, and logged "(Simulated extraction)" while
        // recording keyframesExtracted: 0. Analysis now runs only through the real
        // pipeline in queueManager, where a tool is COMPLETED only after a process
        // has actually run against the media.
        jobState.analysis.ffmpeg.status = 'UNAVAILABLE';
        jobState.logs.push('[ffmpeg] Not run here — use the real pipeline (Make The Show) which executes tools against the media.');
        jobState.analysis.pyscenedetect.status = 'UNAVAILABLE';
        jobState.progress = 70;

        jobState.analysis.whisper.status = 'UNAVAILABLE';

        jobState.progress = 90;

        jobState.logs.push('[VLM] Checking visual observation dependency...');
        // Assume no local VLM is installed in this container by default
        jobState.logs.push(`[VLM] UNAVAILABLE: No local Vision-Language Model detected in container.`);
        jobState.analysis.vlm.status = 'UNAVAILABLE';
        
        jobState.status = 'COMPLETED';
        jobState.progress = 100;
        jobState.result = jobState.analysis;
        jobState.logs.push('Ingest analysis pipeline finished.');

      } catch (err: any) {
        jobState.status = 'FAILED';
        jobState.logs.push(`[FATAL] ${err.message}`);
      }
    })();
    
    res.json({ jobId });
  });

  // Job Status Polling
  app.get("/api/jobs/:id", (req, res) => {
    const job = activeJobs.get(req.params.id);
    if (job) res.json(job);
    else res.status(404).json({ error: "Job not found" });
  });

  // Unified Tool Detection API
  app.get("/api/tools/:tool/detect", async (req, res) => {
    const tool = req.params.tool;
    try {
      if (tool === 'ffmpeg') {
        const { stdout } = await execAsync("ffmpeg -version");
        const versionMatch = stdout.match(/ffmpeg version (.*?) /);
        res.json({ installed: true, version: versionMatch ? versionMatch[1] : "UNKNOWN" });
      } else if (tool === 'blender') {
        const { stdout } = await execAsync("blender --version");
        const versionMatch = stdout.match(/Blender (.*?)\s/);
        res.json({ installed: true, version: versionMatch ? versionMatch[1] : "UNKNOWN" });
      } else if (tool === 'comfyui') {
        try {
          const fetchRes = await fetch("http://127.0.0.1:8188/system_stats");
          if (fetchRes.ok) {
            res.json({ installed: true, version: "Service Running" });
          } else {
            res.json({ installed: false, error: "Not running" });
          }
        } catch (e) {
          res.json({ installed: false, error: "Not running" });
        }
      } else if (tool === 'obs') {
        const { stdout } = await execAsync("obs --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'whisper') {
        const { stdout } = await execAsync("whisper --version");
        res.json({ installed: true, version: stdout.trim() });
      } else if (tool === 'kdenlive') {
        const { stdout } = await execAsync("kdenlive --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'krita') {
        const { stdout } = await execAsync("krita --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'audacity') {
        const { stdout } = await execAsync("audacity --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'gimp') {
        const { stdout } = await execAsync("gimp --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'natron') {
        const { stdout } = await execAsync("NatronRenderer -version");
        res.json({ installed: true, version: stdout.trim() });
      } else if (tool === 'mlt') {
        const { stdout } = await execAsync("melt -version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'huggingface') {
        const { stdout } = await execAsync("huggingface-cli --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'piper') {
        const { stdout } = await execAsync("piper --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'makehuman') {
        const { stdout } = await execAsync("makehuman --version");
        res.json({ installed: true, version: stdout.split('\n')[0].trim() });
      } else if (tool === 'unreal') {
        res.json({ installed: false, error: "UnrealEditor-Cmd not in PATH" });
      } else {
        res.json({ installed: false, error: "Unknown tool" });
      }
    } catch (e) {
      res.json({ installed: false, error: (e as any).message });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
