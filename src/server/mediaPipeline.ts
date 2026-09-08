import { execFile } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';
import os from 'os';
import { Readable } from 'stream';
import { pipeline } from 'stream/promises';

const execFileAsync = promisify(execFile);

export interface MediaPipelineProgress {
  stage: string;
  progress: number;
  message: string;
}

export interface MediaPipelineResult {
  ffprobe?: any;
  scenes?: any[];
  transcript?: any;
  ocr?: string;
  visual?: { sampledFrames: number; width?: number; height?: number; fps?: number; duration?: number };
}

async function run(command: string, args: string[], onOutput?: (text: string) => void) {
  const result = await execFileAsync(command, args, { maxBuffer: 20 * 1024 * 1024 });
  if (onOutput && result.stdout) onOutput(result.stdout);
  return result;
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
  const result: MediaPipelineResult = {};

  onProgress({ stage: 'ffprobe', progress: 10, message: 'Reading technical media metadata.' });
  if (tools.ffprobe) {
    const { stdout } = await run('ffprobe', ['-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', inputPath]);
    result.ffprobe = JSON.parse(stdout);
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
      const workDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-scenes-'));
      try {
        await run('scenedetect', ['-i', inputPath, 'detect-content', 'list-scenes', '-o', workDir]);
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
      } finally { await fs.rm(workDir, { recursive: true, force: true }); }
    })());
  }

  if (tools.opencv) {
    tasks.push((async () => {
      onProgress({ stage: 'opencv', progress: 45, message: 'Sampling frames for visual coverage.' });
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
      const { stdout } = await run('python3', ['-c', python, inputPath]);
      result.visual = { ...JSON.parse(stdout.trim()), duration, width, height, fps };
    })());
  }

  if (tools.tesseract && width && height) {
    tasks.push((async () => {
      onProgress({ stage: 'tesseract', progress: 60, message: 'Running OCR on representative video frames.' });
      const frameDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-ocr-'));
      try {
        const fpsForSampling = duration > 0 ? Math.min(1 / Math.max(duration / 12, 1), 1) : 0.1;
        await run('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-i', inputPath, '-vf', `fps=${fpsForSampling},scale=iw:ih`, '-frames:v', '12', path.join(frameDir, 'frame-%02d.png')]);
        const frames = (await fs.readdir(frameDir)).filter(name => name.endsWith('.png')).sort();
        const chunks: string[] = [];
        for (const frame of frames) {
          try { const { stdout } = await run('tesseract', [path.join(frameDir, frame), 'stdout', '--psm', '6']); if (stdout.trim()) chunks.push(`[${frame}] ${stdout.trim()}`); } catch {}
        }
        result.ocr = chunks.join('\n');
      } finally { await fs.rm(frameDir, { recursive: true, force: true }); }
    })());
  }

  if (tools.whisper && process.env.TRIPPEDD_ENABLE_WHISPER !== 'false') {
    tasks.push((async () => {
      onProgress({ stage: 'whisper', progress: 80, message: 'Transcribing dialogue and speech.' });
      const outputDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-whisper-'));
      try {
        const model = process.env.WHISPER_MODEL || 'tiny';
        try {
          await run('whisper', [inputPath, '--model', model, '--output_dir', outputDir, '--output_format', 'json']);
          const jsonPath = path.join(outputDir, `${path.basename(inputPath).replace(/\.[^.]+$/, '')}.json`);
          try { result.transcript = JSON.parse(await fs.readFile(jsonPath, 'utf8')); } catch { result.transcript = null; }
        } catch (error: any) {
          result.transcript = null;
          onProgress({ stage: 'whisper', progress: 85, message: `Whisper failed; continuing with visual/audio evidence. ${error?.message || String(error)}` });
        }
      } finally { await fs.rm(outputDir, { recursive: true, force: true }); }
    })());
  } else if (tools.whisper) {
    onProgress({ stage: 'whisper', progress: 85, message: 'Whisper deferred for the fast first assembly; visual and scene evidence are sufficient to build the initial cut.' });
  }

  await Promise.all(tasks);
  onProgress({ stage: 'complete', progress: 100, message: 'Media analysis completed.' });
  return result;
}