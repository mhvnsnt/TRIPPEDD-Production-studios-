import { buildEp01FirstAssembly } from '../src/server/pilotRenderer';

const maxClips = Number(process.env.EP01_MAX_CLIPS || 24);
const padding = Number(process.env.EP01_CLIP_PADDING || 1.25);

console.log('TRIPPEDD EP01 — THE WALK');
console.log('Building real first assembly from persisted source evidence...');

try {
  const manifest = await buildEp01FirstAssembly({ maxClips, clipPaddingSeconds: padding });
  console.log(JSON.stringify({
    status: manifest.status,
    sourceClipCount: manifest.sourceClipCount,
    selectedClipCount: manifest.selectedClipCount,
    outputPath: manifest.outputPath,
    missingBeats: manifest.missingBeats,
  }, null, 2));
  process.exit(manifest.status === 'ROUGH_CUT_READY' ? 0 : 2);
} catch (error) {
  console.error(error);
  process.exit(1);
}
