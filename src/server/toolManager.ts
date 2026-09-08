import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs/promises';
import { ToolStatus, ToolDefinition } from '../core/types';

const execAsync = promisify(exec);

export interface ProvisioningStatus {
  status: ToolStatus;
  version?: string;
  executablePath?: string;
  installError?: string;
}

export class ToolManager {
  private definitions: Map<string, ToolDefinition> = new Map();
  private baseVenvPath: string;

  constructor() {
    this.baseVenvPath = path.join(process.cwd(), '.trippedd_venv');
  }

  getTool(id: string): ToolDefinition | undefined {
    return this.definitions.get(id);
  }
  
  getTools(): ToolDefinition[] {
    return Array.from(this.definitions.values());
  }

  async initialize() {
    console.log('Initializing open-source media toolchain...');
    
    this.definitions.set('ffmpeg', this.createDef('ffmpeg', 'FFmpeg', 'Media processing', 'CLI'));
    this.definitions.set('ffprobe', this.createDef('ffprobe', 'FFprobe', 'Media metadata', 'CLI'));
    this.definitions.set('opencv', this.createDef('opencv', 'OpenCV', 'Computer Vision', 'PYTHON'));
    this.definitions.set('pyscenedetect', this.createDef('pyscenedetect', 'PySceneDetect', 'Scene detection', 'PYTHON'));
    this.definitions.set('whisper', this.createDef('whisper', 'Whisper', 'Speech recognition', 'PYTHON'));
    this.definitions.set('tesseract', this.createDef('tesseract', 'Tesseract OCR', 'Optical Character Recognition', 'CLI'));
    this.definitions.set('demucs', this.createDef('demucs', 'Demucs', 'Audio separation', 'PYTHON'));
    this.definitions.set('whisperx', this.createDef('whisperx', 'WhisperX', 'Aligned Speech recognition', 'PYTHON'));
    this.definitions.set('otio', this.createDef('otio', 'OpenTimelineIO', 'Editorial interchange', 'PYTHON'));

    await this.checkBinary('ffmpeg', 'ffmpeg -version', /ffmpeg version (.*?)\s/);
    await this.checkBinary('ffprobe', 'ffprobe -version', /ffprobe version (.*?)\s/);
    await this.checkAptPackage('tesseract', 'tesseract --version', /tesseract (.*?)\s/, 'tesseract-ocr');

    await this.provisionPythonTool('opencv', 'python3 -c "import cv2; print(cv2.__version__)"', null, 'opencv-python');
    await this.provisionPythonTool('pyscenedetect', 'scenedetect --version', /PySceneDetect v(.*)/, 'scenedetect');
    await this.provisionPythonTool('whisper', 'whisper --help', null, 'openai-whisper');
    
    await this.provisionPythonTool('demucs', 'demucs --version', /demucs (.*?)/, 'demucs', true);
    await this.provisionPythonTool('whisperx', 'whisperx --help', null, 'whisperx', true);
    await this.provisionPythonTool('otio', 'python3 -c "import opentimelineio as otio; print(otio.__version__)"', null, 'opentimelineio', true);
  }

  private createDef(id: string, name: string, desc: string, integrationType: any = 'CLI'): ToolDefinition {
    return {
      id, name, description: desc, category: 'Analysis', license: 'Open Source',
      installationStatus: 'NOT_INSTALLED', healthStatus: 'NOT_INSTALLED', integrationType,
      capabilities: { canLaunch: false, canOpenProject: false, canImportAsset: false, canExportAsset: false, canSubmitJob: true }
    };
  }

  private async checkBinary(id: string, cmd: string, versionRegex: RegExp | null) {
    const def = this.definitions.get(id)!;
    try {
      const { stdout } = await execAsync(cmd);
      let version = 'unknown';
      if (versionRegex) {
        const m = stdout.match(versionRegex);
        if (m) version = m[1];
      }
      def.installationStatus = 'AVAILABLE';
      def.healthStatus = 'AVAILABLE';
      def.version = version;
      def.executablePath = id;
    } catch (e: any) {
      def.installationStatus = 'UNAVAILABLE';
      def.healthStatus = 'UNAVAILABLE';
      def.installError = e.message;
    }
  }

  private async checkAptPackage(id: string, checkCmd: string, versionRegex: RegExp, aptPackage: string) {
    const def = this.definitions.get(id)!;
    try {
      const { stdout } = await execAsync(checkCmd);
      def.installationStatus = 'AVAILABLE';
      def.healthStatus = 'AVAILABLE';
      const m = stdout.match(versionRegex);
      if (m) def.version = m[1];
    } catch (e) {
      def.installationStatus = 'INSTALLING';
      try {
        await execAsync(`apt-get install -y ${aptPackage}`);
        const { stdout } = await execAsync(checkCmd);
        def.installationStatus = 'AVAILABLE';
        def.healthStatus = 'AVAILABLE';
        const m = stdout.match(versionRegex);
        if (m) def.version = m[1];
      } catch (err: any) {
        def.installationStatus = 'UNAVAILABLE';
        def.healthStatus = 'UNAVAILABLE';
        def.installError = 'PROVISIONING_UNAVAILABLE - environment does not permit dependency installation: ' + err.message;
      }
    }
  }

  private async markPythonAvailable(def: ToolDefinition, checkCmd: string, versionRegex: RegExp | null, executablePath: string) {
    const { stdout } = await execAsync(checkCmd);
    def.installationStatus = 'AVAILABLE';
    def.healthStatus = 'AVAILABLE';
    if (versionRegex) {
      const m = stdout.match(versionRegex);
      if (m) def.version = m[1];
    }
    def.executablePath = executablePath;
  }

  private async provisionPythonTool(id: string, checkCmd: string, versionRegex: RegExp | null, pipPackage: string, skipProvisioning: boolean = false) {
    const def = this.definitions.get(id)!;

    // CI and developer machines may already have the complete open-source stack.
    // Prefer it instead of creating a second venv and reinstalling the same tools.
    try {
      await this.markPythonAvailable(def, checkCmd, versionRegex, id);
      return;
    } catch {}

    const venvBin = path.join(this.baseVenvPath, 'bin');
    const activate = `source ${path.join(venvBin, 'activate')}`;

    try {
      await fs.stat(this.baseVenvPath);
    } catch {
      try {
        await execAsync(`python3 -m venv ${this.baseVenvPath}`);
      } catch (err: any) {
        def.installationStatus = 'UNAVAILABLE';
        def.installError = 'PROVISIONING_UNAVAILABLE - failed to create python venv: ' + err.message;
        return;
      }
    }

    try {
      await this.markPythonAvailable(def, `bash -c "${activate} && ${checkCmd}"`, versionRegex, path.join(venvBin, id));
    } catch (e) {
      if (skipProvisioning) {
        def.installationStatus = 'UNAVAILABLE';
        def.healthStatus = 'UNAVAILABLE';
        return;
      }

      def.installationStatus = 'INSTALLING';
      try {
        await execAsync(`bash -c "${activate} && pip install ${pipPackage}"`);
        await this.markPythonAvailable(def, `bash -c "${activate} && ${checkCmd}"`, versionRegex, path.join(venvBin, id));
      } catch (err: any) {
        def.installationStatus = 'UNAVAILABLE';
        def.healthStatus = 'UNAVAILABLE';
        def.installError = 'PROVISIONING_UNAVAILABLE - pip install failed: ' + err.message;
      }
    }
  }
}

export const toolManager = new ToolManager();
