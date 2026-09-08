import { execFile } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs/promises';
import { ToolStatus, ToolDefinition, IntegrationType } from '../core/types';

const execFileAsync = promisify(execFile);

type ToolSpec = {
  id: string;
  name: string;
  description: string;
  category: string;
  license: string;
  sourceRepository: string;
  integrationType: IntegrationType;
  command: string;
  args: string[];
  versionRegex?: RegExp;
  pipPackage?: string;
  optional?: boolean;
  capabilities: ToolDefinition['capabilities'];
  runtimeRequirements?: ToolDefinition['runtimeRequirements'];
};

export interface ProvisioningStatus {
  status: ToolStatus;
  version?: string;
  executablePath?: string;
  installError?: string;
}

const OPEN_SOURCE_SPECS: ToolSpec[] = [
  {
    id: 'ffmpeg', name: 'FFmpeg', description: 'Deterministic media decode, encode, mux, filter and audio processing.', category: 'MEDIA', license: 'LGPL/GPL', sourceRepository: 'https://github.com/FFmpeg/FFmpeg', integrationType: 'CLI', command: 'ffmpeg', args: ['-version'], versionRegex: /ffmpeg version ([^\\s]+)/,
    capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: true, canSubmitJob: true }
  },
  {
    id: 'ffprobe', name: 'FFprobe', description: 'Authoritative technical media inspection and verification.', category: 'QC', license: 'LGPL/GPL', sourceRepository: 'https://github.com/FFmpeg/FFmpeg', integrationType: 'CLI', command: 'ffprobe', args: ['-version'], versionRegex: /ffprobe version ([^\\s]+)/,
    capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: false, canSubmitJob: true }
  },
  {
    id: 'opencv', name: 'OpenCV', description: 'Frame sampling and computer-vision primitives.', category: 'ANALYSIS', license: 'Apache-2.0', sourceRepository: 'https://github.com/opencv/opencv', integrationType: 'PYTHON_BRIDGE', command: 'python3', args: ['-c', 'import cv2; print(cv2.__version__)'], pipPackage: 'opencv-python-headless', capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: false, canSubmitJob: true }
  },
  {
    id: 'pyscenedetect', name: 'PySceneDetect', description: 'Automated shot-boundary and scene detection.', category: 'ANALYSIS', license: 'BSD-3-Clause', sourceRepository: 'https://github.com/Breakthrough/PySceneDetect', integrationType: 'CLI', command: 'scenedetect', args: ['--version'], versionRegex: /PySceneDetect v(.+)/, pipPackage: 'scenedetect-headless>=0.7.1', capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: true, canSubmitJob: true }
  },
  {
    id: 'whisper', name: 'faster-whisper', description: 'Production transcription wrapper backed by CTranslate2.', category: 'TRANSCRIPTION', license: 'MIT', sourceRepository: 'https://github.com/SYSTRAN/faster-whisper', integrationType: 'PYTHON_BRIDGE', command: 'python3', args: ['-c', 'import faster_whisper; print("faster-whisper")'], pipPackage: 'faster-whisper>=1.2.0', capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: true, canSubmitJob: true }, runtimeRequirements: { cpu: true, ramMB: 2048 }
  },
  {
    id: 'tesseract', name: 'Tesseract OCR', description: 'OCR for titles, signage, UI, credits and visual evidence.', category: 'ANALYSIS', license: 'Apache-2.0', sourceRepository: 'https://github.com/tesseract-ocr/tesseract', integrationType: 'CLI', command: 'tesseract', args: ['--version'], versionRegex: /tesseract ([^\\s]+)/, capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: false, canSubmitJob: true }
  },
  {
    id: 'otio', name: 'OpenTimelineIO', description: 'Editorial timeline interchange and machine-readable cut representation.', category: 'EDITORIAL', license: 'Apache-2.0', sourceRepository: 'https://github.com/AcademySoftwareFoundation/OpenTimelineIO', integrationType: 'PYTHON_BRIDGE', command: 'python3', args: ['-c', 'import opentimelineio as otio; print(otio.__version__)'], pipPackage: 'opentimelineio>=0.18.1', capabilities: { canLaunch: false, canOpenProject: true, canImportAsset: true, canExportAsset: true, canSubmitJob: true }
  },
  {
    id: 'blender', name: 'Blender', description: 'Procedural 3D, animation, compositing and headless generation.', category: '3D_ANIMATION', license: 'GPL-3.0', sourceRepository: 'https://github.com/blender/blender', integrationType: 'CLI', command: 'blender', args: ['--version'], versionRegex: /Blender ([^\\s]+)/, optional: true, capabilities: { canLaunch: true, canOpenProject: true, canImportAsset: true, canExportAsset: true, canSubmitJob: true }, runtimeRequirements: { cpu: true, gpu: false, ramMB: 4096 }
  },
  {
    id: 'kdenlive', name: 'Kdenlive', description: 'Open-source nonlinear editor and project/timeline authoring backend.', category: 'EDITORIAL', license: 'GPL-3.0', sourceRepository: 'https://invent.kde.org/multimedia/kdenlive', integrationType: 'PROJECT_FILE', command: 'kdenlive', args: ['--version'], versionRegex: /kdenlive ([^\\s]+)/i, optional: true, capabilities: { canLaunch: true, canOpenProject: true, canImportAsset: true, canExportAsset: true, canSubmitJob: true }
  },
  {
    id: 'mlt', name: 'MLT', description: 'Kdenlive-compatible media framework and deterministic render backend.', category: 'EDITORIAL', license: 'LGPL-2.1+', sourceRepository: 'https://github.com/mltframework/mlt', integrationType: 'CLI', command: 'melt', args: ['-version'], optional: true, capabilities: { canLaunch: false, canOpenProject: true, canImportAsset: true, canExportAsset: true, canSubmitJob: true }
  },
  {
    id: 'natron', name: 'Natron', description: 'Node-based compositing and VFX backend.', category: 'VFX', license: 'GPL-2.0', sourceRepository: 'https://github.com/NatronGitHub/Natron', integrationType: 'PROJECT_FILE', command: 'Natron', args: ['--version'], optional: true, capabilities: { canLaunch: true, canOpenProject: true, canImportAsset: true, canExportAsset: true, canSubmitJob: true }, runtimeRequirements: { cpu: true, ramMB: 4096 }
  },
  {
    id: 'opencolorio', name: 'OpenColorIO', description: 'Studio color-management and interchange foundation.', category: 'COLOR', license: 'BSD-3-Clause', sourceRepository: 'https://github.com/AcademySoftwareFoundation/OpenColorIO', integrationType: 'CLI', command: 'ociocheck', args: ['--version'], optional: true, capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: true, canSubmitJob: true }
  },
  {
    id: 'openassetio', name: 'OpenAssetIO', description: 'Asset-centric interoperability boundary between production tools and asset management.', category: 'ASSET_MANAGEMENT', license: 'Apache-2.0', sourceRepository: 'https://github.com/OpenAssetIO/OpenAssetIO', integrationType: 'PYTHON_BRIDGE', command: 'python3', args: ['-c', 'import openassetio; print("openassetio import OK")'], pipPackage: 'openassetio', optional: true, capabilities: { canLaunch: false, canOpenProject: true, canImportAsset: true, canExportAsset: true, canSubmitJob: true }
  },
  {
    id: 'opencue', name: 'OpenCue', description: 'Distributed render management for scalable animation/VFX jobs.', category: 'RENDER_FARM', license: 'Apache-2.0', sourceRepository: 'https://github.com/AcademySoftwareFoundation/OpenCue', integrationType: 'LOCAL_SERVICE', command: 'cueadmin', args: ['-version'], optional: true, capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: false, canExportAsset: false, canSubmitJob: true }, runtimeRequirements: { cpu: true, ramMB: 2048 }
  },
  {
    id: 'demucs', name: 'Demucs', description: 'Optional source-separation capability for music/dialogue/effects isolation.', category: 'AUDIO', license: 'MIT', sourceRepository: 'https://github.com/facebookresearch/demucs', integrationType: 'CLI', command: 'demucs', args: ['--help'], optional: true, capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: true, canExportAsset: true, canSubmitJob: true }, runtimeRequirements: { cpu: true, ramMB: 4096 }
  }
];

export class ToolManager {
  private definitions: Map<string, ToolDefinition> = new Map();
  private baseVenvPath: string;

  constructor() {
    this.baseVenvPath = path.join(process.cwd(), '.trippedd_venv');
  }

  getTool(id: string): ToolDefinition | undefined { return this.definitions.get(id); }
  getTools(): ToolDefinition[] { return Array.from(this.definitions.values()); }

  async initialize() {
    this.definitions.clear();
    for (const spec of OPEN_SOURCE_SPECS) {
      this.definitions.set(spec.id, this.createDef(spec));
    }

    // Probe independent tools concurrently. Optional tools are reported honestly
    // when absent; they are never represented as fake AVAILABLE integrations.
    await Promise.all(OPEN_SOURCE_SPECS.map(spec => this.provisionOrDetect(spec)));
  }

  private createDef(spec: ToolSpec): ToolDefinition {
    return {
      id: spec.id,
      name: spec.name,
      description: spec.description,
      category: spec.category,
      license: spec.license,
      sourceRepository: spec.sourceRepository,
      installationStatus: 'NOT_INSTALLED',
      healthStatus: 'NOT_INSTALLED',
      integrationType: spec.integrationType,
      capabilities: spec.capabilities,
      runtimeRequirements: spec.runtimeRequirements,
      installSource: spec.pipPackage ? `python:${spec.pipPackage}` : `system:${spec.command}`
    };
  }

  private async provisionOrDetect(spec: ToolSpec) {
    const def = this.definitions.get(spec.id)!;
    try {
      const detected = await this.detect(spec);
      if (detected) return;
    } catch {}

    if (!spec.pipPackage || spec.optional) {
      def.installationStatus = 'UNAVAILABLE';
      def.healthStatus = 'UNAVAILABLE';
      def.installError = spec.optional ? 'OPTIONAL_TOOL_NOT_INSTALLED' : 'TOOL_NOT_FOUND';
      return;
    }

    def.installationStatus = 'INSTALLING';
    try {
      await this.ensureVenv();
      const pip = path.join(this.baseVenvPath, 'bin', 'pip');
      await execFileAsync(pip, ['install', spec.pipPackage], { maxBuffer: 20 * 1024 * 1024 });
      const executable = path.join(this.baseVenvPath, 'bin', spec.command);
      await this.markAvailable(spec, executable, true);
    } catch (error: any) {
      def.installationStatus = 'UNAVAILABLE';
      def.healthStatus = 'UNAVAILABLE';
      def.installError = `PROVISIONING_UNAVAILABLE: ${error?.message || String(error)}`;
    }
  }

  private async detect(spec: ToolSpec): Promise<boolean> {
    const def = this.definitions.get(spec.id)!;
    try {
      const { stdout, stderr } = await execFileAsync(spec.command, spec.args, { maxBuffer: 20 * 1024 * 1024 });
      await this.markAvailable(spec, spec.command, false, `${stdout || stderr}`);
      return true;
    } catch {
      return false;
    }
  }

  private async markAvailable(spec: ToolSpec, executablePath: string, pythonVenv: boolean, output?: string) {
    const def = this.definitions.get(spec.id)!;
    const text = output ?? (await execFileAsync(spec.command, spec.args, { maxBuffer: 20 * 1024 * 1024 })).stdout;
    def.installationStatus = 'AVAILABLE';
    def.healthStatus = 'AVAILABLE';
    def.executablePath = executablePath;
    if (spec.versionRegex) {
      const match = text.match(spec.versionRegex);
      if (match) def.version = match[1];
    } else {
      def.version = text.trim().split(/\r?\n/)[0].slice(0, 160) || (pythonVenv ? 'available' : 'unknown');
    }
  }

  private async ensureVenv() {
    try {
      await fs.access(path.join(this.baseVenvPath, 'bin', 'python'));
    } catch {
      await execFileAsync('python3', ['-m', 'venv', this.baseVenvPath], { maxBuffer: 20 * 1024 * 1024 });
    }
  }
}

export const toolManager = new ToolManager();
