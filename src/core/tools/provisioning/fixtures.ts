/**
 * Health-check fixtures.
 *
 * A health check has to run the tool against REAL media, so we need real media
 * that exists everywhere the app runs. The image fixture is drawn from an
 * embedded bitmap font and encoded to PNG here rather than rendered with
 * ffmpeg's drawtext, because drawtext needs libfreetype plus a font file that
 * happens to be installed — measured in this container, the only fonts present
 * were incidental. A fixture that depends on incidental system state produces
 * health checks that fail for reasons unrelated to the tool being checked.
 */
import { deflateSync } from 'zlib';
import { writeFile, mkdir, stat } from 'fs/promises';
import path from 'path';

/** 5x7 glyphs, enough to spell the OCR probe word. */
const GLYPHS: Record<string, string[]> = {
  T: ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
  R: ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
  I: ['11111', '00100', '00100', '00100', '00100', '00100', '11111'],
  P: ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
  E: ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
  D: ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
};

// MEASURED: a doubled 'DD' at 5px reads as 'OO' to Tesseract ('TRIPPEDD' -> 'TRIPPEOO'),
// which would fail the health check on a perfectly good install. 'TRIPPED' round-trips exactly.
export const OCR_PROBE_WORD = 'TRIPPED';

const CRC_TABLE = (() => {
  const t = new Int32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c;
  }
  return t;
})();

function crc32(buf: Buffer): number {
  let c = -1;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ -1) >>> 0;
}

function chunk(type: string, data: Buffer): Buffer {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type, 'ascii'), data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}

/** Minimal 8-bit greyscale PNG encoder. */
function encodeGreyPng(width: number, height: number, pixels: Uint8Array): Buffer {
  const raw = Buffer.alloc((width + 1) * height);
  for (let y = 0; y < height; y++) {
    raw[y * (width + 1)] = 0; // filter: none
    for (let x = 0; x < width; x++) raw[y * (width + 1) + 1 + x] = pixels[y * width + x];
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 0; // greyscale
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', deflateSync(raw, { level: 9 })),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}

/** Renders the probe word as black-on-white at a size Tesseract reads reliably. */
export function renderProbePng(word = OCR_PROBE_WORD, scale = 12, margin = 40): Buffer {
  const gw = 5, gh = 7, gap = 2;
  const cols = word.length * (gw + gap) - gap;
  const width = cols * scale + margin * 2;
  const height = gh * scale + margin * 2;
  const px = new Uint8Array(width * height).fill(255); // white ground

  word.split('').forEach((ch, i) => {
    const g = GLYPHS[ch];
    if (!g) return;
    const ox = margin + i * (gw + gap) * scale;
    for (let y = 0; y < gh; y++) {
      for (let x = 0; x < gw; x++) {
        if (g[y][x] !== '1') continue;
        for (let dy = 0; dy < scale; dy++) {
          for (let dx = 0; dx < scale; dx++) {
            const py = margin + y * scale + dy;
            const pxx = ox + x * scale + dx;
            px[py * width + pxx] = 0; // black glyph
          }
        }
      }
    }
  });

  return encodeGreyPng(width, height, px);
}

export interface Fixtures {
  video: string;
  image: string;
  audio: string;
  /** False when ffmpeg was unavailable, so video/audio fixtures do not exist. */
  hasMedia: boolean;
}

async function exists(p: string): Promise<boolean> {
  try { await stat(p); return true; } catch { return false; }
}

/**
 * Materialise the fixture set into `dir`. The image fixture is always
 * available; video/audio require ffmpeg, and their absence is reported rather
 * than papered over.
 */
export async function ensureFixtures(
  dir: string,
  runFfmpeg: (args: string[]) => Promise<boolean>
): Promise<Fixtures> {
  await mkdir(dir, { recursive: true });
  const image = path.join(dir, 'ocr_probe.png');
  const video = path.join(dir, 'probe.mp4');
  const audio = path.join(dir, 'probe.wav');

  if (!(await exists(image))) {
    await writeFile(image, renderProbePng());
  }

  let hasMedia = (await exists(video)) && (await exists(audio));
  if (!hasMedia) {
    const okV = await runFfmpeg([
      '-y', '-v', 'error',
      '-f', 'lavfi', '-i', 'testsrc=size=320x240:rate=15',
      '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=16000',
      '-t', '2', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-c:a', 'aac',
      '-shortest', video,
    ]);
    const okA = await runFfmpeg([
      '-y', '-v', 'error',
      '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=16000',
      '-t', '2', audio,
    ]);
    hasMedia = okV && okA;
  }

  return { video, image, audio, hasMedia };
}
