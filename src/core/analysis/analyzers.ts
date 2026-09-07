/**
 * Real media analyzers.
 *
 * Each analyzer runs an actual tool process against actual media through the
 * sanctioned executor and derives observations from the tool's real output.
 * When a tool is not AVAILABLE the analyzer returns UNAVAILABLE with an
 * ADAPTER_DEFINED provenance record and NO observations — an absent tool can
 * never contribute evidence.
 */
import path from 'path';
import { readFile, writeFile, readdir, mkdir } from 'fs/promises';
import { executeTool, adapterDefined } from '../tools/execution/executor';
import { runnerRoot } from '../tools/execution/runnerRoot';
import type { ToolRunProvenance } from '../types';
import type { ResourceClass } from '../scheduler/ResourceScheduler';

export type AnalyzerStatus = 'COMPLETED' | 'FAILED' | 'UNAVAILABLE' | 'SKIPPED';

/** A single machine-derived fact, always carrying the run that produced it. */
export interface MachineObservation {
  id: string;
  type: string;
  startTime?: number;
  endTime?: number;
  frame?: number;
  text?: string;
  data?: Record<string, unknown>;
  origin: 'MACHINE_GENERATED';
  reviewState: 'UNREVIEWED';
  tool: string;
  toolVersion: string;
}

export interface AnalyzerResult {
  tool: string;
  status: AnalyzerStatus;
  provenance: ToolRunProvenance;
  observations: MachineObservation[];
  derivedArtifacts: string[];
  data?: unknown;
  error?: string;
}

export interface ToolHandle {
  id: string;
  state: string;
  version?: string;
  executablePath?: string;
}

export interface AnalysisContext {
  fileId: string;
  /** Local path; undefined when only a stream is available. */
  localPath?: string;
  /** Streamable URL (with auth already applied by the caller). */
  streamUrl?: string;
  sourceHash?: string;
  /** Scratch directory for derived artifacts belonging to this job. */
  workDir: string;
  getTool(id: string): ToolHandle | undefined;
  pythonPath(): string;
}

export interface Analyzer {
  id: string;
  /** Registry id of the tool this analyzer needs. */
  requiresTool: string;
  resourceClass: ResourceClass;
  /** True when the tool cannot work from a URL and needs bytes on disk. */
  requiresLocalFile: boolean;
  /**
   * Analyzer ids that must COMPLETE first. WhisperX aligns the transcript
   * faster-whisper produces, so running them concurrently would hand alignment
   * a file that does not exist yet.
   */
  dependsOn?: string[];
  run(ctx: AnalysisContext): Promise<AnalyzerResult>;
}

let obsSeq = 0;
function obs(
  type: string,
  tool: string,
  toolVersion: string,
  fields: Partial<MachineObservation> = {}
): MachineObservation {
  return {
    id: `obs_${Date.now().toString(36)}_${(obsSeq++).toString(36)}`,
    type,
    origin: 'MACHINE_GENERATED',
    reviewState: 'UNREVIEWED',
    tool,
    toolVersion,
    ...fields,
  };
}

/** Uniform "tool is not usable" result. Produces no observations, ever. */
function unavailable(toolId: string, fileId: string, reason: string): AnalyzerResult {
  return {
    tool: toolId,
    status: 'UNAVAILABLE',
    provenance: adapterDefined(toolId, fileId, reason),
    observations: [],
    derivedArtifacts: [],
    error: reason,
  };
}

function scriptPath(name: string): string {
  return path.join(runnerRoot(), 'src', 'core', 'analysis', 'scripts', name);
}

// --------------------------------------------------------------- ffprobe

export const FFprobeAnalyzer: Analyzer = {
  id: 'ffprobe',
  requiresTool: 'ffprobe',
  resourceClass: 'LIGHT',
  requiresLocalFile: false, // reads a stream header without pulling the file
  async run(ctx) {
    const t = ctx.getTool('ffprobe');
    if (!t || t.state !== 'AVAILABLE' || !t.executablePath) {
      return unavailable('ffprobe', ctx.fileId, `ffprobe ${t?.state ?? 'NOT_INSTALLED'}`);
    }
    const target = ctx.localPath ?? ctx.streamUrl;
    if (!target) return unavailable('ffprobe', ctx.fileId, 'no readable source');

    const r = await executeTool({
      tool: 'ffprobe', version: t.version ?? 'unknown', executablePath: t.executablePath,
      args: ['-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', target],
      sourceFileId: ctx.fileId, sourcePath: ctx.localPath, sourceHash: ctx.sourceHash,
      timeoutMs: 120_000,
    });

    if (!r.provenance.success) {
      return { tool: 'ffprobe', status: 'FAILED', provenance: r.provenance, observations: [], derivedArtifacts: [], error: r.stderr.slice(0, 300) };
    }

    let parsed: any;
    try {
      parsed = JSON.parse(r.stdout);
    } catch (e: any) {
      return { tool: 'ffprobe', status: 'FAILED', provenance: { ...r.provenance, success: false }, observations: [], derivedArtifacts: [], error: `unparseable output: ${e.message}` };
    }

    const v = parsed.streams?.find((s: any) => s.codec_type === 'video');
    const a = parsed.streams?.find((s: any) => s.codec_type === 'audio');
    let fps: number | undefined;
    if (v?.r_frame_rate) {
      const [n, d] = String(v.r_frame_rate).split('/').map(Number);
      if (d) fps = n / d;
    }
    const duration = parsed.format?.duration ? Number(parsed.format.duration) : undefined;

    return {
      tool: 'ffprobe',
      status: 'COMPLETED',
      provenance: r.provenance,
      derivedArtifacts: [],
      data: { duration, width: v?.width, height: v?.height, codec: v?.codec_name, fps, hasAudio: !!a, format: parsed.format?.format_name },
      observations: [
        obs('TECHNICAL_METADATA', 'ffprobe', t.version ?? 'unknown', {
          startTime: 0, endTime: duration,
          data: {
            duration, width: v?.width, height: v?.height, codec: v?.codec_name, fps,
            hasAudio: !!a, container: parsed.format?.format_name,
            // Timestamp provenance is kept distinct: a container tag is not
            // shooting chronology, and the chronology engine must be able to
            // tell which kind of time it is looking at.
            containerCreationTime: parsed.format?.tags?.creation_time ?? null,
          },
        }),
      ],
    };
  },
};

// ---------------------------------------------------------- PySceneDetect

export const SceneDetectAnalyzer: Analyzer = {
  id: 'pyscenedetect',
  requiresTool: 'pyscenedetect',
  resourceClass: 'CPU_HEAVY',
  requiresLocalFile: true,
  async run(ctx) {
    const t = ctx.getTool('pyscenedetect');
    if (!t || t.state !== 'AVAILABLE' || !t.executablePath) {
      return unavailable('pyscenedetect', ctx.fileId, `pyscenedetect ${t?.state ?? 'NOT_INSTALLED'}`);
    }
    if (!ctx.localPath) return unavailable('pyscenedetect', ctx.fileId, 'requires a local file');

    const outDir = path.join(ctx.workDir, 'scenes');
    await mkdir(outDir, { recursive: true });

    const r = await executeTool({
      tool: 'pyscenedetect', version: t.version ?? 'unknown', executablePath: t.executablePath,
      args: ['-i', ctx.localPath, '-o', outDir, 'detect-content', 'list-scenes'],
      sourceFileId: ctx.fileId, sourcePath: ctx.localPath, sourceHash: ctx.sourceHash,
      timeoutMs: 1_800_000,
    });

    if (!r.provenance.success) {
      return { tool: 'pyscenedetect', status: 'FAILED', provenance: r.provenance, observations: [], derivedArtifacts: [], error: r.stderr.slice(0, 300) };
    }

    // Parse the CSV it wrote; fall back to the printed table.
    const scenes: { start: number; end: number; startFrame: number; endFrame: number }[] = [];
    let csvFile: string | undefined;
    try {
      const files = await readdir(outDir);
      csvFile = files.find((f) => f.endsWith('.csv'));
    } catch { /* directory may be absent when no scenes were written */ }

    if (csvFile) {
      const csv = await readFile(path.join(outDir, csvFile), 'utf8');
      for (const line of csv.split('\n')) {
        const c = line.split(',');
        // Data rows begin with a scene number; the file has a preamble.
        if (c.length > 7 && /^\d+$/.test(c[0].trim())) {
          const start = Number(c[3]), end = Number(c[6]);
          if (Number.isFinite(start) && Number.isFinite(end)) {
            scenes.push({ start, end, startFrame: Number(c[1]), endFrame: Number(c[4]) });
          }
        }
      }
    }

    const version = t.version ?? 'unknown';
    return {
      tool: 'pyscenedetect',
      status: 'COMPLETED',
      provenance: { ...r.provenance, derivedArtifactIds: csvFile ? [csvFile] : [] },
      derivedArtifacts: csvFile ? [path.join(outDir, csvFile)] : [],
      data: { sceneCount: scenes.length, scenes },
      observations: scenes.map((s, i) =>
        obs('SHOT_BOUNDARY', 'pyscenedetect', version, {
          startTime: s.start, endTime: s.end,
          data: { shotIndex: i + 1, startFrame: s.startFrame, endFrame: s.endFrame },
        })
      ),
    };
  },
};

// -------------------------------------------------------------- OpenCV

export const OpenCVAnalyzer: Analyzer = {
  id: 'opencv',
  requiresTool: 'opencv',
  resourceClass: 'CPU_HEAVY',
  requiresLocalFile: true,
  async run(ctx) {
    const t = ctx.getTool('opencv');
    if (!t || t.state !== 'AVAILABLE') {
      return unavailable('opencv', ctx.fileId, `opencv ${t?.state ?? 'NOT_INSTALLED'}`);
    }
    if (!ctx.localPath) return unavailable('opencv', ctx.fileId, 'requires a local file');

    const r = await executeTool({
      tool: 'opencv', version: t.version ?? 'unknown', executablePath: ctx.pythonPath(),
      args: [scriptPath('opencv_analyze.py'), ctx.localPath, '240'],
      sourceFileId: ctx.fileId, sourcePath: ctx.localPath, sourceHash: ctx.sourceHash,
      timeoutMs: 900_000,
    });

    if (!r.provenance.success) {
      return { tool: 'opencv', status: 'FAILED', provenance: r.provenance, observations: [], derivedArtifacts: [], error: r.stderr.slice(0, 300) };
    }

    let d: any;
    try { d = JSON.parse(r.stdout); } catch (e: any) {
      return { tool: 'opencv', status: 'FAILED', provenance: { ...r.provenance, success: false }, observations: [], derivedArtifacts: [], error: `unparseable output: ${e.message}` };
    }
    if (d.error) {
      return { tool: 'opencv', status: 'FAILED', provenance: { ...r.provenance, success: false }, observations: [], derivedArtifacts: [], error: d.error };
    }

    const version = t.version ?? 'unknown';
    const out: MachineObservation[] = [
      obs('VISUAL_SUMMARY', 'opencv', version, {
        data: { sampled: d.sampled, stride: d.stride, motionMean: d.motionMean, motionMax: d.motionMax, blankFrameCount: d.blankFrames?.length ?? 0 },
      }),
    ];

    // Only flag high-motion moments relative to THIS clip's own distribution;
    // an absolute threshold is meaningless across different footage.
    if (d.motionMean != null && d.motionMax != null && d.motionMax > d.motionMean * 3) {
      for (const s of d.samples ?? []) {
        if (s.motion > d.motionMean * 3 && s.t != null) {
          out.push(obs('VISUAL_CHANGE', 'opencv', version, {
            startTime: s.t, frame: s.frame,
            data: { motion: s.motion, motionMean: d.motionMean, luma: s.luma },
          }));
        }
      }
    }
    for (const f of d.blankFrames ?? []) {
      const s = (d.samples ?? []).find((x: any) => x.frame === f);
      out.push(obs('BLANK_FRAME', 'opencv', version, { frame: f, startTime: s?.t, data: { luma: s?.luma } }));
    }

    return { tool: 'opencv', status: 'COMPLETED', provenance: r.provenance, observations: out, derivedArtifacts: [], data: { sampled: d.sampled, motionMean: d.motionMean } };
  },
};

// ------------------------------------------------------------ Tesseract

export const TesseractAnalyzer: Analyzer = {
  id: 'tesseract',
  requiresTool: 'tesseract',
  resourceClass: 'CPU_HEAVY',
  requiresLocalFile: true,
  async run(ctx) {
    const t = ctx.getTool('tesseract');
    const ff = ctx.getTool('ffmpeg');
    if (!t || t.state !== 'AVAILABLE' || !t.executablePath) {
      return unavailable('tesseract', ctx.fileId, `tesseract ${t?.state ?? 'NOT_INSTALLED'}`);
    }
    // OCR needs frames, and frames need ffmpeg. Say so rather than guessing.
    if (!ff || ff.state !== 'AVAILABLE' || !ff.executablePath) {
      return unavailable('tesseract', ctx.fileId, 'frame extraction requires ffmpeg, which is unavailable');
    }
    if (!ctx.localPath) return unavailable('tesseract', ctx.fileId, 'requires a local file');

    const frameDir = path.join(ctx.workDir, 'ocr_frames');
    await mkdir(frameDir, { recursive: true });
    const fps = 0.2; // one frame every 5s: enough for slates and signage

    const ex = await executeTool({
      tool: 'ffmpeg', version: ff.version ?? 'unknown', executablePath: ff.executablePath,
      args: ['-v', 'error', '-i', ctx.localPath, '-vf', `fps=${fps}`, '-q:v', '3', path.join(frameDir, 'f_%05d.jpg')],
      sourceFileId: ctx.fileId, sourcePath: ctx.localPath, timeoutMs: 900_000,
    });
    if (!ex.provenance.success) {
      return { tool: 'tesseract', status: 'FAILED', provenance: ex.provenance, observations: [], derivedArtifacts: [], error: `frame extraction failed: ${ex.stderr.slice(0, 200)}` };
    }

    const frames = (await readdir(frameDir)).filter((f) => f.endsWith('.jpg')).sort();
    const version = t.version ?? 'unknown';
    const observations: MachineObservation[] = [];
    let last: ToolRunProvenance | undefined;

    for (let i = 0; i < frames.length; i++) {
      const fp = path.join(frameDir, frames[i]);
      const r = await executeTool({
        tool: 'tesseract', version, executablePath: t.executablePath,
        args: [fp, 'stdout'], sourceFileId: ctx.fileId, timeoutMs: 120_000,
      });
      last = r.provenance;
      if (!r.provenance.success) continue;
      const text = r.stdout.trim();
      // Short noise is not text. Anything kept is what the OCR engine actually
      // returned, never a cleaned-up guess.
      if (text.length >= 3) {
        observations.push(obs('ON_SCREEN_TEXT', 'tesseract', version, {
          startTime: i / fps, endTime: (i + 1) / fps, text,
          data: { frameFile: frames[i] },
        }));
      }
    }

    const provenance: ToolRunProvenance =
      last ?? { ...ex.provenance, tool: 'tesseract', version };

    return {
      tool: 'tesseract',
      status: 'COMPLETED',
      provenance: { ...provenance, derivedArtifactIds: frames },
      observations,
      derivedArtifacts: frames.map((f) => path.join(frameDir, f)),
      data: { framesScanned: frames.length, textFrames: observations.length },
    };
  },
};

// -------------------------------------------------------- faster-whisper

export const WhisperAnalyzer: Analyzer = {
  id: 'faster-whisper',
  requiresTool: 'faster-whisper',
  resourceClass: 'CPU_HEAVY',
  requiresLocalFile: true,
  async run(ctx) {
    const t = ctx.getTool('faster-whisper');
    if (!t || t.state !== 'AVAILABLE') {
      return unavailable('faster-whisper', ctx.fileId, `faster-whisper ${t?.state ?? 'NOT_INSTALLED'}`);
    }
    if (!ctx.localPath) return unavailable('faster-whisper', ctx.fileId, 'requires a local file');

    const modelDir = path.join(runnerRoot(), '.trippedd_tools', 'models');
    const modelSize = process.env.TRIPPEDD_WHISPER_MODEL || 'tiny';

    const r = await executeTool({
      tool: 'faster-whisper', version: t.version ?? 'unknown', executablePath: ctx.pythonPath(),
      args: [scriptPath('whisper_transcribe.py'), ctx.localPath, modelSize, modelDir],
      sourceFileId: ctx.fileId, sourcePath: ctx.localPath, sourceHash: ctx.sourceHash,
      timeoutMs: 3_600_000,
    });

    if (!r.provenance.success) {
      return { tool: 'faster-whisper', status: 'FAILED', provenance: r.provenance, observations: [], derivedArtifacts: [], error: r.stderr.slice(0, 300) };
    }

    let d: any;
    try { d = JSON.parse(r.stdout); } catch (e: any) {
      return { tool: 'faster-whisper', status: 'FAILED', provenance: { ...r.provenance, success: false }, observations: [], derivedArtifacts: [], error: `unparseable output: ${e.message}` };
    }

    const version = `${t.version ?? 'unknown'}/${d.model}`;
    const segs = (d.segments ?? []).filter((s: any) => s.text);

    const transcriptPath = path.join(ctx.workDir, 'transcript.json');
    await writeFile(transcriptPath, JSON.stringify(d, null, 2));

    return {
      tool: 'faster-whisper',
      status: 'COMPLETED',
      provenance: { ...r.provenance, version, derivedArtifactIds: ['transcript.json'] },
      derivedArtifacts: [transcriptPath],
      data: { language: d.language, languageProbability: d.languageProbability, segmentCount: segs.length },
      observations: segs.map((s: any) =>
        obs('TRANSCRIPT_SEGMENT', 'faster-whisper', version, {
          startTime: s.start, endTime: s.end, text: s.text,
          data: { language: d.language, languageProbability: d.languageProbability },
        })
      ),
    };
  },
};

// ---------------------------------------------------------- WhisperX

/**
 * Word-level forced alignment on top of the faster-whisper transcript.
 *
 * Utterance timestamps are good enough to find a moment; word timestamps are
 * what let a cut land between words instead of chopping one. Runs only when the
 * transcript already exists — it refines, it does not re-transcribe.
 */
export const WhisperXAnalyzer: Analyzer = {
  id: 'whisperx',
  requiresTool: 'whisperx',
  resourceClass: 'GPU',
  requiresLocalFile: true,
  dependsOn: ['faster-whisper'],
  async run(ctx) {
    const t = ctx.getTool('whisperx');
    if (!t || t.state !== 'AVAILABLE') {
      return unavailable('whisperx', ctx.fileId, `whisperx ${t?.state ?? 'NOT_INSTALLED'}`);
    }
    if (!ctx.localPath) return unavailable('whisperx', ctx.fileId, 'requires a local file');

    // Alignment needs the transcript the whisper pass wrote.
    const transcriptPath = path.join(ctx.workDir, 'transcript.json');
    try {
      await readFile(transcriptPath, 'utf8');
    } catch {
      return unavailable('whisperx', ctx.fileId, 'no transcript to align — faster-whisper did not produce one');
    }

    const modelDir = path.join(runnerRoot(), '.trippedd_tools', 'models');
    const r = await executeTool({
      tool: 'whisperx', version: t.version ?? 'unknown', executablePath: ctx.pythonPath(),
      args: [scriptPath('whisperx_align.py'), ctx.localPath, transcriptPath, modelDir],
      sourceFileId: ctx.fileId, sourcePath: ctx.localPath, sourceHash: ctx.sourceHash,
      timeoutMs: 3_600_000,
      env: {
        // NLTK refuses proxied downloads by default as an SSRF guard and names
        // this flag as the opt-in. This container's egress IS a documented
        // policy-enforcing proxy, so opting in is the intended path. No TLS
        // verification is disabled anywhere.
        NLTK_ALLOW_PROXIED_URLOPEN: '1',
      },
    });

    if (!r.provenance.success) {
      return { tool: 'whisperx', status: 'FAILED', provenance: r.provenance, observations: [], derivedArtifacts: [], error: r.stderr.slice(0, 300) };
    }

    let d: any;
    try { d = JSON.parse(r.stdout.trim().split('\n').pop() || '{}'); } catch (e: any) {
      return { tool: 'whisperx', status: 'FAILED', provenance: { ...r.provenance, success: false }, observations: [], derivedArtifacts: [], error: `unparseable output: ${e.message}` };
    }
    if (!d.aligned) {
      return { tool: 'whisperx', status: 'COMPLETED', provenance: r.provenance, observations: [], derivedArtifacts: [], data: { aligned: false, reason: d.reason } };
    }

    const version = t.version ?? 'unknown';
    const wordsPath = path.join(ctx.workDir, 'words.json');
    await writeFile(wordsPath, JSON.stringify(d, null, 2));

    return {
      tool: 'whisperx',
      status: 'COMPLETED',
      provenance: { ...r.provenance, derivedArtifactIds: ['words.json'] },
      derivedArtifacts: [wordsPath],
      data: { wordCount: d.wordCount, language: d.language },
      observations: (d.words ?? []).map((w: any) =>
        obs('WORD_TIMING', 'whisperx', version, {
          startTime: w.start, endTime: w.end, text: w.word,
          data: { score: w.score },
        })
      ),
    };
  },
};

// ----------------------------------------------------------- Demucs

/**
 * Stem separation. Isolating dialogue from music/noise makes a cut cleaner and
 * gives the editor usable production audio. Derived stems are new artifacts —
 * the original media is never modified.
 */
export const DemucsAnalyzer: Analyzer = {
  id: 'demucs',
  requiresTool: 'demucs',
  resourceClass: 'GPU',
  requiresLocalFile: true,
  async run(ctx) {
    const t = ctx.getTool('demucs');
    if (!t || t.state !== 'AVAILABLE') {
      return unavailable('demucs', ctx.fileId, `demucs ${t?.state ?? 'NOT_INSTALLED'}`);
    }
    if (!ctx.localPath) return unavailable('demucs', ctx.fileId, 'requires a local file');

    const outDir = path.join(ctx.workDir, 'stems');
    await mkdir(outDir, { recursive: true });

    const r = await executeTool({
      tool: 'demucs', version: t.version ?? 'unknown', executablePath: ctx.pythonPath(),
      args: ['-m', 'demucs', '--two-stems', 'vocals', '-d', 'cpu', '-o', outDir, ctx.localPath],
      sourceFileId: ctx.fileId, sourcePath: ctx.localPath, sourceHash: ctx.sourceHash,
      timeoutMs: 3_600_000,
    });

    if (!r.provenance.success) {
      return { tool: 'demucs', status: 'FAILED', provenance: r.provenance, observations: [], derivedArtifacts: [], error: r.stderr.slice(0, 300) };
    }

    const produced: string[] = [];
    async function walk(dir: string) {
      for (const e of await readdir(dir, { withFileTypes: true })) {
        const p = path.join(dir, e.name);
        if (e.isDirectory()) await walk(p);
        else if (/\.(wav|mp3|flac)$/i.test(e.name)) produced.push(p);
      }
    }
    try { await walk(outDir); } catch { /* no stems written */ }

    const version = t.version ?? 'unknown';
    return {
      tool: 'demucs',
      status: 'COMPLETED',
      provenance: { ...r.provenance, derivedArtifactIds: produced.map((p) => path.basename(p)) },
      derivedArtifacts: produced,
      data: { stemCount: produced.length },
      observations: produced.length
        ? [obs('AUDIO_STEMS', 'demucs', version, { data: { stems: produced.map((p) => path.basename(p)), count: produced.length } })]
        : [],
    };
  },
};

/** Ordered so cheap structural facts land before expensive analysis. */
export const ALL_ANALYZERS: Analyzer[] = [
  FFprobeAnalyzer,
  SceneDetectAnalyzer,
  OpenCVAnalyzer,
  TesseractAnalyzer,
  WhisperAnalyzer,
  // Enhancements last: they refine what the earlier passes produced.
  WhisperXAnalyzer,
  DemucsAnalyzer,
];
