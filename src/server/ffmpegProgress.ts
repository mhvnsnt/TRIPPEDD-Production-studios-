import { ChildProcess } from 'child_process';

export interface FfmpegProgressSample {
  outTimeSeconds?: number;
  speed?: number;
  fraction?: number;
  raw: Record<string, string>;
}

export function attachFfmpegProgress(child: ChildProcess, durationSeconds: number, onProgress: (sample: FfmpegProgressSample) => void) {
  if (!child.stdout) return;
  let buffer = '';
  let raw: Record<string, string> = {};
  child.stdout.setEncoding('utf8');
  child.stdout.on('data', (chunk: string) => {
    buffer += chunk;
    const lines = buffer.split(/\r?\n/);
    buffer = lines.pop() || '';
    for (const line of lines) {
      const separator = line.indexOf('=');
      if (separator <= 0) continue;
      const key = line.slice(0, separator);
      const value = line.slice(separator + 1);
      raw[key] = value;
      if (key === 'progress') {
        const outTimeUs = Number(raw.out_time_us ?? raw.out_time_ms);
        const outTimeSeconds = Number.isFinite(outTimeUs) ? outTimeUs / 1_000_000 : undefined;
        const fraction = Number.isFinite(outTimeSeconds) && durationSeconds > 0 ? Math.max(0, Math.min(1, outTimeSeconds / durationSeconds)) : undefined;
        const speedText = raw.speed?.replace(/x$/, '');
        const speed = Number(speedText);
        onProgress({ outTimeSeconds, speed: Number.isFinite(speed) ? speed : undefined, fraction, raw: { ...raw } });
        raw = {};
      }
    }
  });
}
