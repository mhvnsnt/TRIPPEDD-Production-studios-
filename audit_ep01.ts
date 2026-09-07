import { EpisodeRegistry } from './src/core/pipeline/episodes';

const ep = EpisodeRegistry.getEpisode('EP01');

if (!ep) {
  console.error("Episode EP01 not found.");
  process.exit(1);
}

console.log(`\n=== PRODUCTION READINESS AUDIT: ${ep.id} - ${ep.name} ===\n`);

let missingAssets = 0;
let blockedJobsCount = 0;

ep.segments.forEach((seg, i) => {
  console.log(`--- SEGMENT ${i + 1}: ${seg.name} (${seg.id}) ---`);
  
  // Required source media
  const requiredMedia = seg.sourceClips.map(c => c.assetId).concat(seg.gags.flatMap(g => g.sourceMaterial?.map(sm => sm.assetId) || []));
  console.log(`Required Source Media: ${requiredMedia.length > 0 ? requiredMedia.join(', ') : 'None'}`);
  
  // Physical check (simulated - we know no files have been uploaded/rendered yet)
  const sourcesExist = false;
  console.log(`Physical Media Exists & Verified: ${requiredMedia.length === 0 ? 'N/A' : 'NO (Missing files from disk/registry)'}`);
  
  if (requiredMedia.length > 0) {
    let prov = seg.provenance.realityStatus;
    if (seg.sourceClips.length > 0 && seg.sourceClips[0].originalProvenance) {
        prov = seg.sourceClips[0].originalProvenance.realityStatus;
    } else if (seg.gags.length > 0 && seg.gags[0].sourceMaterial && seg.gags[0].sourceMaterial.length > 0) {
        prov = seg.gags[0].sourceMaterial[0].originalProvenance?.realityStatus || prov;
    }
    console.log(`Source Clip Provenance: ${prov}`);
  } else {
    console.log(`Source Clip Provenance: N/A`);
  }

  console.log(`Required Performances: ${seg.performances.length > 0 ? seg.performances.map(p => `${p.personId} as ${p.characterId}`).join(', ') : 'None'}`);
  console.log(`Required Generated Assets: ${seg.assetIds.length > 0 ? seg.assetIds.join(', ') : 'None'}`);
  
  // Tool deduction based on jobs and assembly mode
  const tools = new Set<string>();
  if (seg.jobIds.some(j => j.includes('COMFYUI'))) tools.add('ComfyUI');
  if (seg.jobIds.some(j => j.includes('FFMPEG'))) tools.add('FFmpeg');
  if (seg.provenance.assemblyMode.includes('ANIMATION')) tools.add('2D/3D Animation Tools');
  if (tools.size === 0) tools.add('NLE / Kdenlive (Editorial Assembly)');
  console.log(`Required Tools: ${Array.from(tools).join(', ')}`);

  console.log(`Executable Jobs: None (Dependencies missing)`);
  
  const blocked = seg.jobIds.length > 0 ? seg.jobIds : (requiredMedia.length > 0 ? ['AWAITING_SOURCE_INGEST'] : ['AWAITING_GENERATION']);
  console.log(`Blocked Jobs: ${blocked.join(', ')}`);
  
  console.log(`Expected Physical Outputs: ${seg.id}_FINAL_RENDER.mkv`);
  console.log(`Current Output Paths: None`);
  
  console.log(`Complete Provenance/Lineage: \n  Reality: ${seg.provenance.realityStatus} \n  Capture: ${seg.provenance.captureStatus} \n  Authorship: ${seg.provenance.authorship} \n  Assembly: ${seg.provenance.assemblyMode} \n  AI Contribution: ${seg.provenance.aiContributions.join(', ')}`);
  
  console.log(`Segment Watchable: NO`);
  console.log('');
  
  missingAssets += requiredMedia.length + seg.assetIds.length;
  blockedJobsCount += seg.jobIds.length;
});

console.log(`=== OVERALL EPISODE 01 STATUS ===`);
console.log(`Total Segments: ${ep.segments.length}`);
console.log(`Watchable: NO (0 physical renders exist)`);
console.log(`Missing Physical Assets/Sources: ${missingAssets}`);
console.log(`Blocked Jobs: ${blockedJobsCount}`);

console.log(`\nCURRENT STATE: CONCEPT / STORYBOARD`);
