/**
 * Declarative specs for the open-source media-analysis toolchain.
 *
 * TIERING IS DELIBERATE (owner instruction): the first tier is what actually
 * earns its keep on ingest, so it auto-provisions. WhisperX and Demucs are
 * expensive dependencies and OpenTimelineIO only matters once we are genuinely
 * crossing into editorial interchange, so those are opt-in and are never
 * installed blindly at boot.
 */
import type { ToolCapability } from '../../types';

export type ToolTier = 'CORE' | 'PRIMARY' | 'ENHANCED' | 'INTERCHANGE';

/** How a tool is obtained when it is missing. */
export type InstallPlan =
  | { kind: 'apt'; package: string }
  | { kind: 'pip'; package: string }
  | { kind: 'manual'; reason: string };

/** How a tool is found and version-stamped once present. */
export interface DetectPlan {
  /** Executable basename to resolve, for CLI tools. */
  bin?: string;
  /** Python module to import, for library tools with no CLI. */
  pythonModule?: string;
  /** Args that make the tool print its version. */
  versionArgs?: string[];
  /** Extracts the version from combined stdout+stderr. */
  versionPattern: RegExp;
}

/**
 * A health check is a MINIMAL REAL RUN, not a version string. `media` checks
 * run the tool against a real generated fixture; `import` checks only prove the
 * library loads. The kind is recorded on the result so a weaker check is never
 * silently read as a strong one.
 */
export interface HealthPlan {
  kind: 'media' | 'image' | 'import' | 'selftest';
  /** Builds the argv for the check, given fixture paths. */
  args: (fixtures: { video: string; image: string; audio: string }) => string[];
  /** Optional stricter assertion on the output of a successful run. */
  expect?: (out: string) => boolean;
}

export interface ToolSpec {
  id: string;
  name: string;
  tier: ToolTier;
  category: string;
  license: string;
  sourceRepository: string;
  description: string;
  capabilities: string[];
  toolCapability: ToolCapability;
  runtimeRequirements: {
    cpu: boolean;
    gpu: boolean;
    ramMB: number;
    diskMB: number;
    /** Scheduling class the queue uses to bound concurrency. */
    resourceClass: 'LIGHT' | 'CPU_HEAVY' | 'GPU';
  };
  install: InstallPlan;
  detect: DetectPlan;
  health: HealthPlan;
  minVersion?: string;
}

const JOB: ToolCapability = {
  canLaunch: false, canOpenProject: false, canImportAsset: true,
  canExportAsset: false, canSubmitJob: true,
};

export const TOOL_SPECS: ToolSpec[] = [
  {
    id: 'ffmpeg',
    name: 'FFmpeg',
    tier: 'CORE',
    category: 'Media',
    license: 'LGPL-2.1-or-later / GPL-2.0-or-later',
    sourceRepository: 'https://github.com/FFmpeg/FFmpeg',
    description: 'Decode, transcode and extract frames/audio from source media.',
    capabilities: ['transcode', 'frame-extraction', 'audio-extraction', 'thumbnailing'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 512, diskMB: 200, resourceClass: 'CPU_HEAVY' },
    install: { kind: 'apt', package: 'ffmpeg' },
    detect: { bin: 'ffmpeg', versionArgs: ['-version'], versionPattern: /ffmpeg version (\S+)/i },
    health: {
      kind: 'media',
      // Decodes the fixture and writes nothing: proves the decoder path works.
      args: (f) => ['-v', 'error', '-i', f.video, '-f', 'null', '-'],
    },
  },
  {
    id: 'ffprobe',
    name: 'FFprobe',
    tier: 'CORE',
    category: 'Media',
    license: 'LGPL-2.1-or-later / GPL-2.0-or-later',
    sourceRepository: 'https://github.com/FFmpeg/FFmpeg',
    description: 'Container/stream metadata inspection.',
    capabilities: ['metadata', 'stream-inspection', 'duration', 'codec-detection'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 128, diskMB: 0, resourceClass: 'LIGHT' },
    install: { kind: 'apt', package: 'ffmpeg' },
    detect: { bin: 'ffprobe', versionArgs: ['-version'], versionPattern: /ffprobe version (\S+)/i },
    health: {
      kind: 'media',
      args: (f) => ['-v', 'quiet', '-print_format', 'json', '-show_format', f.video],
      // A health check that only checks exit code would pass on empty output.
      expect: (out) => {
        try { return !!JSON.parse(out)?.format; } catch { return false; }
      },
    },
  },
  {
    id: 'pyscenedetect',
    name: 'PySceneDetect',
    tier: 'PRIMARY',
    category: 'Analysis',
    license: 'BSD-3-Clause',
    sourceRepository: 'https://github.com/Breakthrough/PySceneDetect',
    description: 'Shot-boundary detection — the spine of the physical source timeline.',
    capabilities: ['scene-detection', 'shot-boundaries', 'cut-list'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 1024, diskMB: 100, resourceClass: 'CPU_HEAVY' },
    install: { kind: 'pip', package: 'scenedetect[opencv]' },
    detect: { bin: 'scenedetect', versionArgs: ['version'], versionPattern: /PySceneDetect[ v]+([\d.]+)/i },
    health: {
      kind: 'media',
      args: (f) => ['-i', f.video, 'detect-content', 'list-scenes', '-n'],
    },
  },
  {
    id: 'opencv',
    name: 'OpenCV',
    tier: 'PRIMARY',
    category: 'Analysis',
    license: 'Apache-2.0',
    sourceRepository: 'https://github.com/opencv/opencv',
    description: 'Frame-level computer vision: histograms, motion, black/blank frames.',
    capabilities: ['frame-analysis', 'histogram', 'motion-estimation', 'blank-detection'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 1024, diskMB: 300, resourceClass: 'CPU_HEAVY' },
    install: { kind: 'pip', package: 'opencv-python-headless' },
    detect: {
      pythonModule: 'cv2',
      versionArgs: ['-c', 'import cv2;print(cv2.__version__)'],
      versionPattern: /([\d]+\.[\d]+\.[\d]+\S*)/,
    },
    health: {
      kind: 'media',
      // Opens the real fixture and reads a real frame. An import alone would
      // pass even with no video backend compiled in.
      args: (f) => [
        '-c',
        `import cv2,sys
c=cv2.VideoCapture(${JSON.stringify(f.video)})
ok,fr=c.read()
c.release()
sys.exit(0 if ok and fr is not None else 3)`,
      ],
    },
  },
  {
    id: 'tesseract',
    name: 'Tesseract OCR',
    tier: 'PRIMARY',
    category: 'Analysis',
    license: 'Apache-2.0',
    sourceRepository: 'https://github.com/tesseract-ocr/tesseract',
    description: 'On-screen text recovery from frames (slates, timecode burn-in, signage).',
    capabilities: ['ocr', 'slate-reading', 'burn-in-timecode'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 512, diskMB: 150, resourceClass: 'CPU_HEAVY' },
    install: { kind: 'apt', package: 'tesseract-ocr' },
    detect: { bin: 'tesseract', versionArgs: ['--version'], versionPattern: /tesseract\s+v?([\d.]+)/i },
    health: {
      kind: 'image',
      args: (f) => [f.image, 'stdout'],
      // Proves the OCR engine and its language data actually resolve glyphs.
      expect: (out) => /TRIPPED/i.test(out),
    },
  },
  {
    id: 'faster-whisper',
    name: 'faster-whisper',
    tier: 'PRIMARY',
    category: 'Audio',
    license: 'MIT',
    sourceRepository: 'https://github.com/SYSTRAN/faster-whisper',
    description: 'CTranslate2 Whisper transcription — dialogue and spoken slate capture.',
    capabilities: ['transcription', 'timestamps', 'language-detection'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 2048, diskMB: 900, resourceClass: 'CPU_HEAVY' },
    install: { kind: 'pip', package: 'faster-whisper' },
    detect: {
      pythonModule: 'faster_whisper',
      versionArgs: ['-c', 'import faster_whisper as w;print(getattr(w,"__version__","0"))'],
      versionPattern: /([\d]+\.[\d]+\.[\d]+\S*)/,
    },
    health: {
      kind: 'import',
      // Deliberately an import-only check: a media check would download model
      // weights at boot. The model is fetched lazily on first real transcription.
      args: () => ['-c', 'from faster_whisper import WhisperModel;print("ok")'],
      expect: (out) => out.includes('ok'),
    },
  },
  {
    id: 'whisperx',
    name: 'WhisperX',
    tier: 'ENHANCED',
    category: 'Audio',
    license: 'BSD-4-Clause',
    sourceRepository: 'https://github.com/m-bain/whisperX',
    description: 'Word-level alignment and diarisation on top of Whisper.',
    capabilities: ['transcription', 'word-alignment', 'diarisation'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: true, ramMB: 6144, diskMB: 4000, resourceClass: 'GPU' },
    install: { kind: 'pip', package: 'whisperx' },
    detect: {
      pythonModule: 'whisperx',
      versionArgs: ['-c', 'import whisperx;print(getattr(whisperx,"__version__","0"))'],
      versionPattern: /([\d]+\.[\d]+\S*)/,
    },
    health: { kind: 'import', args: () => ['-c', 'import whisperx;print("ok")'], expect: (o) => o.includes('ok') },
  },
  {
    id: 'demucs',
    name: 'Demucs',
    tier: 'ENHANCED',
    category: 'Audio',
    license: 'MIT',
    sourceRepository: 'https://github.com/adefossez/demucs',
    description: 'Music/dialogue stem separation for isolating usable production audio.',
    capabilities: ['source-separation', 'stem-extraction', 'dialogue-isolation'],
    toolCapability: JOB,
    runtimeRequirements: { cpu: true, gpu: true, ramMB: 8192, diskMB: 5000, resourceClass: 'GPU' },
    install: { kind: 'pip', package: 'demucs' },
    detect: {
      pythonModule: 'demucs',
      versionArgs: ['-c', 'import demucs;print(getattr(demucs,"__version__","0"))'],
      versionPattern: /([\d]+\.[\d]+\S*)/,
    },
    health: { kind: 'import', args: () => ['-c', 'import demucs;print("ok")'], expect: (o) => o.includes('ok') },
  },
  {
    id: 'otio',
    name: 'OpenTimelineIO',
    tier: 'INTERCHANGE',
    category: 'Interchange',
    license: 'Apache-2.0',
    sourceRepository: 'https://github.com/AcademySoftwareFoundation/OpenTimelineIO',
    description: 'Editorial interchange — export the physical timeline to an NLE.',
    capabilities: ['timeline-export', 'edl', 'aaf-adjacent', 'otio-json'],
    toolCapability: { ...JOB, canExportAsset: true },
    runtimeRequirements: { cpu: true, gpu: false, ramMB: 256, diskMB: 80, resourceClass: 'LIGHT' },
    install: { kind: 'pip', package: 'opentimelineio' },
    detect: {
      pythonModule: 'opentimelineio',
      versionArgs: ['-c', 'import opentimelineio as o;print(o.__version__)'],
      versionPattern: /([\d]+\.[\d]+\.[\d]+\S*)/,
    },
    health: {
      kind: 'selftest',
      // Builds a real timeline in memory and serialises it.
      args: () => [
        '-c',
        `import opentimelineio as otio
t=otio.schema.Timeline(name="hc")
t.tracks.append(otio.schema.Track(name="V1"))
print("ok" if otio.adapters.write_to_string(t,"otio_json") else "")`,
      ],
      expect: (o) => o.includes('ok'),
    },
  },
];

/** Tiers provisioned automatically at boot. Everything else is opt-in. */
export const AUTO_PROVISION_TIERS: ToolTier[] = ['CORE', 'PRIMARY'];

export function specById(id: string): ToolSpec | undefined {
  return TOOL_SPECS.find((s) => s.id === id);
}
