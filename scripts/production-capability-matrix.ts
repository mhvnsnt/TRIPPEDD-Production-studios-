import fs from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const config = JSON.parse(await fs.readFile(path.join(root, 'config', 'studio-toolchain.json'), 'utf8')) as any;
const performance = JSON.parse(await fs.readFile(path.join(root, 'config', 'production-performance.json'), 'utf8')) as any;

const capabilities = [
  { id: 'media-ingest', tools: ['gdown', 'ffprobe'], output: 'checksum-addressed source media and technical metadata' },
  { id: 'shot-analysis', tools: ['pyscenedetect', 'opencv'], output: 'shot boundaries and visual coverage evidence' },
  { id: 'dialogue-analysis', tools: ['whisper', 'tesseract'], output: 'transcript and on-screen text evidence' },
  { id: 'image-inspection', tools: ['openimageio'], output: 'image metadata and sequence validation' },
  { id: 'procedural-generation', tools: ['blender'], output: 'generated 3D/VFX assets with provenance' },
  { id: 'compositing', tools: ['natron'], output: 'node-based compositing when installed' },
  { id: 'color-management', tools: ['opencolorio'], output: 'repeatable color transforms' },
  { id: 'editorial-interchange', tools: ['otio', 'openassetio'], output: 'portable timelines and asset references' },
  { id: 'audio-separation', tools: ['demucs'], output: 'dialogue/music/effects stems when needed' },
  { id: 'distributed-rendering', tools: ['opencue', 'blender'], output: 'parallel render dispatch when workers exist' },
  { id: 'deterministic-delivery', tools: ['ffmpeg', 'ffprobe', 'mediainfo'], output: 'reproducible MP4 encode and technical QC' },
];

const required = new Set(config.required || []);
const optional = new Set(config.optional || []);
const report = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  targets: { episodeMinutes: performance.targetEpisodeMinutes, generationWallClockMinutes: performance.targetGenerationWallClockMinutes, stretchSpeedupFactor: performance.stretchSpeedupFactor },
  capabilities: capabilities.map(capability => ({ ...capability, requiredTools: capability.tools.filter((tool: string) => required.has(tool)), optionalTools: capability.tools.filter((tool: string) => optional.has(tool) || !required.has(tool)) })),
  architecture: { requiredToolchain: [...required], optionalToolchain: [...optional], featureGatedOptionalAcceleration: performance.policy?.optionalAccelerationMustBeFeatureGated === true },
};

const out = path.join(root, 'public', 'production', 'production-capability-matrix.json');
await fs.mkdir(path.dirname(out), { recursive: true });
await fs.writeFile(out, JSON.stringify(report, null, 2), 'utf8');
console.log(JSON.stringify(report, null, 2));
