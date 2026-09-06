import { ToolRegistry } from './registry';
import { FFmpegAdapter } from './adapters/ffmpeg';
import { ComfyUIAdapter } from './adapters/comfyui';
import { BlenderAdapter } from './adapters/blender';
import { GenericAdapter } from './adapters/generic';

export function initTools() {
  // Foundational Adapters (Specialized implementations)
  ToolRegistry.register(new FFmpegAdapter());
  ToolRegistry.register(new ComfyUIAdapter());
  ToolRegistry.register(new BlenderAdapter());

  const stdCaps = {
    canLaunch: true, canOpenProject: true, canImportAsset: true, canExportAsset: true, canSubmitJob: false
  };

  // Expanded Open Source Stack
  ToolRegistry.register(new GenericAdapter('obs', 'OBS Studio', 'Capture', 'Capture / recording / compositing', 'GPLv2', 'WEBSOCKET', stdCaps));
  ToolRegistry.register(new GenericAdapter('audacity', 'Audacity', 'Audio', 'Audio editing/recording', 'GPLv2', 'PROJECT_FILE', stdCaps));
  ToolRegistry.register(new GenericAdapter('krita', 'Krita', '2D', '2D art / painting / graphics', 'GPLv3', 'PYTHON_BRIDGE', stdCaps));
  ToolRegistry.register(new GenericAdapter('unreal', 'Unreal Engine', '3D', 'Virtual production / realtime environments', 'Proprietary', 'PROJECT_FILE', stdCaps));
  
  ToolRegistry.register(new GenericAdapter('kdenlive', 'Kdenlive', 'Video', 'Non-linear video editing', 'GPLv2', 'PROJECT_FILE', stdCaps));
  ToolRegistry.register(new GenericAdapter('natron', 'Video', 'Compositing', 'Node-based compositing', 'GPLv2', 'SUBPROCESS', stdCaps));
  ToolRegistry.register(new GenericAdapter('gimp', 'GIMP', '2D', 'Image manipulation', 'GPLv3', 'PLUGIN', stdCaps));
  ToolRegistry.register(new GenericAdapter('mlt', 'MLT Framework', 'Video', 'Multimedia framework / backend', 'LGPL', 'CLI', { ...stdCaps, canSubmitJob: true }));
  ToolRegistry.register(new GenericAdapter('huggingface', 'Hugging Face CLI', 'AI', 'Model discovery and management', 'Apache 2.0', 'CLI', { ...stdCaps, canSubmitJob: true }));
  ToolRegistry.register(new GenericAdapter('whisper', 'Whisper', 'Audio', 'Speech recognition and transcription', 'MIT', 'CLI', { ...stdCaps, canSubmitJob: true }));
  ToolRegistry.register(new GenericAdapter('piper', 'Piper TTS', 'Audio', 'Fast local neural text to speech', 'MIT', 'CLI', { ...stdCaps, canSubmitJob: true }));
  ToolRegistry.register(new GenericAdapter('makehuman', 'MakeHuman', '3D', '3D character creation', 'AGPL', 'CLI', stdCaps));
}
