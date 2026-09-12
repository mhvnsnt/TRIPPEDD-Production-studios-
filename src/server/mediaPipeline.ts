import { execFile } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';
import os from 'os';
import { Readable } from 'stream';
import { pipeline } from 'stream/promises';
import { evidenceCache, EvidenceCache } from './evidenceCache';

const execFileAsync = promisify(execFile);

const ANALYZER_VERSIONS = {
  ffprobe: 'ffprobe-json-v1',
  pyscenedetect: 'pyscenedetect-content-v1',
  opencv: 'opencv-10s-sampling-v1',
  tesseract: 'tesseract-12-frame-v1',
  whisper: 'whisper-json-v1',
} as const;

export interface MediaPipelineProgress {
  stage: string;
  progress: number;
  message: string;
}

/**
 * What a process ACTUALLY did, recorded as it happens.
 *
 * Provenance was previously minted after the fact by a helper that hardcoded
 * success:true, durationMs:0, identical start and end timestamps, and a command
 * string containing the literal placeholder '<local-source>'. A record like
 * that is a DESCRIPTION of what was supposed to happen, and it reads exactly
 * the same whether the tool ran or never ran — which is the failure this
 * project has been bitten by four separate times.
 *
 * These are measured around the real execFile call. A tool with no entry here
 * did not run, and provenance refuses to claim otherwise.
 */
export interface ToolRun {
  tool: string;
  command: string;        // the argv that was actually executed
  startedAt: string;
  endedAt: string;
  durationMs: number;
  success: boolean;
  exitCode: number | null;
  error?: string;
}

export interface MediaPipelineResult {
  /** Every process this analysis spawned, in order. */
  runs: ToolRun[];
  ffprobe?: any;
  scenes?: any[];
  transcript?: any;
  ocr?: string;
  visual?: { sampledFrames: number; width?: number; height?: number; fps?: number; duration?: number; frameCount?: number };
}

async function run(
  command: string,
  args: string[],
  onOutput?: (text: string) => void,
  ledger?: ToolRun[],
) {
  const startedAt = new Date();
  const t0 = Date.now();
  const record = (success: boolean, exitCode: number | null, error?: string) => {
    ledger?.push({
      tool: command,
      command: [command, ...args].join(' '),
      startedAt: startedAt.toISOString(),
      endedAt: new Date().toISOString(),
      durationMs: Date.now() - t0,
      success,
      exitCode,
      ...(error ? { error } : {}),
    });
  };
  try {
    const result = await execFileAsync(command, args, { maxBuffer: 20 * 1024 * 1024 });
    record(true, 0);
    if (onOutput && result.stdout) onOutput(result.stdout);
    return result;
  } catch (e: any) {
    // A failed run is still a run, and the ledger has to say so — a tool that
    // was attempted and failed is a different fact from one never attempted.
    record(false, typeof e?.code === 'number' ? e.code : null, e?.message || String(e));
    throw e;
  }
}

export async function downloadToFile(url: string, credential: string, destination: string) {
  const isPublicKey = credential.startsWith('public:');
  const requestUrl = isPublicKey
    ? `${url}&key=${encodeURIComponent(credential.slice('public:'.length))}`
    : url;
  const response = await fetch(requestUrl, isPublicKey ? undefined : { headers: { Authorization: `Bearer ${credential}` } });
  if (!response.ok || !response.body) throw new Error(`Media download failed: ${response.status} ${response.statusText}`);
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await pipeline(Readable.fromWeb(response.body as any), await fs.open(destination, 'w').then(handle => handle.createWriteStream()));
}

export async function analyzeMedia(
  inputPath: string,
  tools: Record<string, boolean>,
  onProgress: (progress: MediaPipelineProgress) => void,
): Promise<MediaPipelineResult> {
  const result: MediaPipelineResult = { runs: [] };
  const ledger = result.runs;
  const sourceSha256 = await EvidenceCache.sha256(inputPath);

  onProgress({ stage: 'ffprobe', progress: 10, message: 'Reading technical media metadata.' });
  if (tools.ffprobe) {
    const key = { sourceSha256, analyzer: 'ffprobe', analyzerVersion: ANALYZER_VERSIONS.ffprobe };
    result.ffprobe = await evidenceCache.get<any>(key);
    if (result.ffprobe) {
      onProgress({ stage: 'ffprobe', progress: 12, message: 'Reused checksum-keyed FFprobe evidence.' });
    } else {
      const { stdout } = await run('ffprobe', ['-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', inputPath], undefined, ledger);
      result.ffprobe = JSON.parse(stdout);
      await evidenceCache.put(key, result.ffprobe);
    }
  }

  const videoStream = result.ffprobe?.streams?.find((stream: any) => stream.codec_type === 'video');
  const duration = Number(result.ffprobe?.format?.duration || 0);
  const width = videoStream?.width;
  const height = videoStream?.height;
  const fpsText = videoStream?.r_frame_rate;
  const fps = fpsText && fpsText.includes('/')
    ? Number(fpsText.split('/')[0]) / Number(fpsText.split('/')[1])
    : Number(fpsText || 0);

  // These analyses are independent after ffprobe. Run them concurrently so the
  // open-source stack spends the wall-clock time of its slowest analyzer rather
  // than the sum of scene detection + sampling + OCR + transcription.
  const tasks: Promise<void>[] = [];

  if (tools.pyscenedetect) {
    tasks.push((async () => {
      onProgress({ stage: 'pyscenedetect', progress: 30, message: 'Detecting shot boundaries.' });
      const key = { sourceSha256, analyzer: 'pyscenedetect', analyzerVersion: ANALYZER_VERSIONS.pyscenedetect };
      const cached = await evidenceCache.get<any[]>(key);
      if (cached) {
        result.scenes = cached;
        onProgress({ stage: 'pyscenedetect', progress: 32, message: 'Reused checksum-keyed scene evidence.' });
        return;
      }
      const workDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-scenes-'));
      try {
        await run('scenedetect', ['-i', inputPath, 'detect-content', 'list-scenes', '-o', workDir], undefined, ledger);
        const csvPath = path.join(workDir, `${path.basename(inputPath).replace(/\.[^.]+$/, '')}-Scenes.csv`);
        try {
          const csv = await fs.readFile(csvPath, 'utf8');
          const lines = csv.split(/\r?\n/).filter(Boolean);
          const headers = lines.shift()?.split(',') || [];
          result.scenes = lines.map(line => {
            const values = line.split(',');
            return Object.fromEntries(headers.map((header, index) => [header.trim(), values[index]?.trim() ?? '']));
          });
        } catch { result.scenes = []; }
        await evidenceCache.put(key, result.scenes || []);
      } finally { await fs.rm(workDir, { recursive: true, force: true }); }
    })());
  }

  if (tools.opencv) {
    tasks.push((async () => {
      onProgress({ stage: 'opencv', progress: 45, message: 'Sampling frames for visual coverage.' });
      const key = { sourceSha256, analyzer: 'opencv', analyzerVersion: ANALYZER_VERSIONS.opencv };
      const cached = await evidenceCache.get<MediaPipelineResult['visual']>(key);
      if (cached) {
        result.visual = cached;
        onProgress({ stage: 'opencv', progress: 47, message: 'Reused checksum-keyed visual sampling evidence.' });
        return;
      }
      const python = [
        'import cv2, json, sys',
        'p=cv2.VideoCapture(sys.argv[1])',
        'fps=p.get(cv2.CAP_PROP_FPS) or 0',
        'frames=int(p.get(cv2.CAP_PROP_FRAME_COUNT) or 0)',
        'w=int(p.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)',
        'h=int(p.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)',
        'step=max(1,int(fps*10))',
        'pos=0',
        'sampled=0',
        'while pos < frames:',
        '    p.set(cv2.CAP_PROP_POS_FRAMES, pos)',
        '    ok,_=p.read()',
        '    if ok: sampled+=1',
        '    pos+=step',
        'p.release()',
        'print(json.dumps({"sampledFrames":sampled,"frameCount":frames,"width":w,"height":h,"fps":fps}))',
      ].join('\n');
      const { stdout } = await run('python3', ['-c', python, inputPath], undefined, ledger);
      result.visual = { ...JSON.parse(stdout.trim()), duration, width, height, fps };
      await evidenceCache.put(key, result.visual);
    })());
  }

  if (tools.tesseract && width && height) {
    tasks.push((async () => {
      onProgress({ stage: 'tesseract', progress: 60, message: 'Running OCR on representative video frames.' });
      const key = { sourceSha256, analyzer: 'tesseract', analyzerVersion: ANALYZER_VERSIONS.tesseract };
      const cached = await evidenceCache.get<string>(key);
      if (cached !== null) {
        result.ocr = cached;
        onProgress({ stage: 'tesseract', progress: 62, message: 'Reused checksum-keyed OCR evidence.' });
        return;
      }
      const frameDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-ocr-'));
      try {
        const fpsForSampling = duration > 0 ? Math.min(1 / Math.max(duration / 12, 1), 1) : 0.1;
        await run('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-i', inputPath, '-vf', `fps=${fpsForSampling},scale=iw:ih`, '-frames:v', '12', path.join(frameDir, 'frame-%02d.png')], undefined, ledger);
        const frames = (await fs.readdir(frameDir)).filter(name => name.endsWith('.png')).sort();
        const chunks: string[] = [];
        for (const frame of frames) {
          try { const { stdout } = await run('tesseract', [path.join(frameDir, frame), 'stdout', '--psm', '6'], undefined, ledger); if (stdout.trim()) chunks.push(`[${frame}] ${stdout.trim()}`); } catch {}
        }
        result.ocr = chunks.join('\n');
        await evidenceCache.put(key, result.ocr);
      } finally { await fs.rm(frameDir, { recursive: true, force: true }); }
    })());
  }

  if (tools.whisper && process.env.TRIPPEDD_ENABLE_WHISPER !== 'false') {
    tasks.push((async () => {
      onProgress({ stage: 'whisper', progress: 80, message: 'Transcribing dialogue and speech.' });
      const key = { sourceSha256, analyzer: 'whisper', analyzerVersion: ANALYZER_VERSIONS.whisper };
      const cached = await evidenceCache.get<any>(key);
      if (cached !== null) {
        result.transcript = cached;
        onProgress({ stage: 'whisper', progress: 82, message: 'Reused checksum-keyed transcript evidence.' });
        return;
      }
      const outputDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-whisper-'));
      try {
        const model = process.env.WHISPER_MODEL || 'tiny';
        try {
          await run('whisper', [inputPath, '--model', model, '--output_dir', outputDir, '--output_format', 'json'], undefined, ledger);
          const jsonPath = path.join(outputDir, `${path.basename(inputPath).replace(/\.[^.]+$/, '')}.json`);
          try { result.transcript = JSON.parse(await fs.readFile(jsonPath, 'utf8')); } catch { result.transcript = null; }
        } catch (error: any) {
          result.transcript = null;
          onProgress({ stage: 'whisper', progress: 85, message: `Whisper failed; continuing with visual/audio evidence. ${error?.message || String(error)}` });
        }
        if (result.transcript !== null && result.transcript !== undefined) await evidenceCache.put(key, result.transcript);
      } finally { await fs.rm(outputDir, { recursive: true, force: true }); }
    })());
  } else if (tools.whisper) {
    onProgress({ stage: 'whisper', progress: 85, message: 'Whisper deferred for the fast first assembly; visual and scene evidence are sufficient to build the initial cut.' });
  }

  await Promise.all(tasks);
  onProgress({ stage: 'complete', progress: 100, message: 'Media analysis completed.' });
  return result;
}