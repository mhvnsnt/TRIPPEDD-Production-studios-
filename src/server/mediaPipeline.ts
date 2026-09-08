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
  if (!response.ok || !response.body) {
    throw new Error(`Media download failed: ${response.status} ${response.statusText}`);
  }
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
    const { stdout } = await run('ffprobe', [
      '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', inputPath,
    ]);
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

  if (tools.pyscenedetect) {
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
  }

  if (tools.opencv) {
    onProgress({ stage: 'opencv', progress: 45, message: 'Sampling frames for visual coverage.' });
    const python = [
      'import cv2, json, sys', 'p=cv2.VideoCapture(sys.argv[1])', 'fps=p.get(cv2.CAP_PROP_FPS) or 0',
      'frames=int(p.get(cv2.CAP_PROP_FRAME_COUNT) or 0)', 'w=int(p.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)',
      'h=int(p.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)', 'step=max(1,int(fps*10))', 'count=0; sampled=0',
      'while True:', ' ok,_=p.read()', ' if not ok: break', ' count+=1', ' if count % step == 0: sampled+=1',
      'p.release()', 'print(json.dumps({"sampledFrames":sampled,"frameCount":frames,"width":w,"height":h,"fps":fps}))',
    ].join(';');
    const { stdout } = await run('python3', ['-c', python, inputPath]);
    const visual = JSON.parse(stdout.trim());
    result.visual = { ...visual, duration, width, height, fps };
  }

  if (tools.tesseract && width && height) {
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
  }

  if (tools.whisper) {
    onProgress({ stage: 'whisper', progress: 80, message: 'Transcribing dialogue and speech.' });
    const outputDir = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-whisper-'));
    try {
      const model = process.env.WHISPER_MODEL || 'tiny';
      await run('whisper', [inputPath, '--model', model, '--output_dir', outputDir, '--output_format', 'json']);
      const jsonPath = path.join(outputDir, `${path.basename(inputPath).replace(/\.[^.]+$/, '')}.json`);
      try { result.transcript = JSON.parse(await fs.readFile(jsonPath, 'utf8')); } catch { result.transcript = null; }
    } finally { await fs.rm(outputDir, { recursive: true, force: true }); }
  }

  onProgress({ stage: 'complete', progress: 100, message: 'Media analysis completed.' });
  return result;
}
