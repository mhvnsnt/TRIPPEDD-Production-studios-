/**
 * What a supplied 3D model ACTUALLY IS, measured from the bytes.
 *
 * The creator supplies a model and the pipeline's first job is to know what it
 * received — not to assume it is a rigged character because it arrived in a
 * conversation about rigging. Everything here is read off the file: mesh and
 * primitive counts, triangles, vertices, whether it is skinned, how many
 * joints, morph targets, materials, textures and their real sizes, animations,
 * and the bounding box in the file's own units.
 *
 * Prints a verdict on what production lanes it can enter as-is, and what it
 * would need first. It changes nothing — the original is never modified.
 *
 *   node scripts/inspect_model.cjs <model.glb>
 */
const { NodeIO } = require('@gltf-transform/core');
const { ALL_EXTENSIONS } = require('@gltf-transform/extensions');
const fs = require('fs');
const path = require('path');

(async () => {
  const file = process.argv[2];
  if (!file || !fs.existsSync(file)) { console.error('usage: inspect_model.cjs <model.glb>'); process.exit(1); }

  const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
  let doc;
  try { doc = await io.read(file); }
  catch (e) { console.error(`CANNOT PARSE: ${e.message}`); process.exit(2); }

  const root = doc.getRoot();
  const bytes = fs.statSync(file).size;

  console.log('='.repeat(84));
  console.log(path.basename(file));
  console.log('='.repeat(84));
  console.log(`  file size        ${(bytes / 1048576).toFixed(1)} MB`);
  console.log(`  generator        ${root.getAsset().generator ?? '(not recorded)'}`);
  console.log(`  extensions       ${root.listExtensionsUsed().map((e) => e.extensionName).join(', ') || '(none)'}`);

  // ── geometry, counted off the accessors rather than the node names ────────
  let tris = 0, verts = 0, prims = 0, morphTargets = 0;
  const semantics = new Set();
  for (const mesh of root.listMeshes()) {
    for (const p of mesh.listPrimitives()) {
      prims++;
      const pos = p.getAttribute('POSITION');
      if (pos) verts += pos.getCount();
      const idx = p.getIndices();
      tris += idx ? idx.getCount() / 3 : (pos ? pos.getCount() / 3 : 0);
      morphTargets += p.listTargets().length;
      for (const s of p.listSemantics()) semantics.add(s);
    }
  }
  console.log(`\n  meshes           ${root.listMeshes().length} (${prims} primitive${prims === 1 ? '' : 's'})`);
  console.log(`  triangles        ${Math.round(tris).toLocaleString()}`);
  console.log(`  vertices         ${verts.toLocaleString()}`);
  console.log(`  vertex data      ${[...semantics].sort().join(', ')}`);
  console.log(`  morph targets    ${morphTargets}${morphTargets ? '' : '  (no blendshapes — facial expressions would have to be rigged)'}`);

  // ── rig ───────────────────────────────────────────────────────────────────
  const skins = root.listSkins();
  const joints = skins.flatMap((s) => s.listJoints());
  console.log(`\n  skins            ${skins.length}`);
  console.log(`  joints           ${joints.length}${joints.length ? '' : '  (UNRIGGED — a static mesh, not an animatable character)'}`);
  if (joints.length) {
    const names = joints.map((j) => j.getName()).filter(Boolean);
    console.log(`  joint names      ${names.slice(0, 12).join(', ')}${names.length > 12 ? ` … +${names.length - 12}` : ''}`);
    // Facial rigging needs head-region joints; say whether any exist.
    const facial = names.filter((n) => /head|jaw|eye|neck|tongue|teeth|brow|lip|cheek/i.test(n));
    console.log(`  head/face joints ${facial.length ? facial.slice(0, 10).join(', ') : '(none found by name)'}`);
  }
  console.log(`  animations       ${root.listAnimations().length}`);

  // ── surfacing ─────────────────────────────────────────────────────────────
  console.log(`\n  materials        ${root.listMaterials().length}`);
  const texes = root.listTextures();
  console.log(`  textures         ${texes.length}`);
  for (const t of texes.slice(0, 8)) {
    const img = t.getImage();
    const size = img ? (img.byteLength / 1048576).toFixed(2) + ' MB' : '?';
    const [w, h] = t.getSize() ?? [0, 0];
    console.log(`     ${(t.getName() || '(unnamed)').padEnd(26)} ${w}x${h}  ${t.getMimeType()}  ${size}`);
  }
  if (texes.length > 8) console.log(`     … +${texes.length - 8} more`);

  // ── real-world scale, from the vertex positions ───────────────────────────
  let min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
  for (const mesh of root.listMeshes()) {
    for (const p of mesh.listPrimitives()) {
      const pos = p.getAttribute('POSITION');
      if (!pos) continue;
      const el = [0, 0, 0];
      for (let i = 0; i < pos.getCount(); i++) {
        pos.getElement(i, el);
        for (let k = 0; k < 3; k++) { if (el[k] < min[k]) min[k] = el[k]; if (el[k] > max[k]) max[k] = el[k]; }
      }
    }
  }
  const dim = max.map((v, i) => v - min[i]);
  console.log(`\n  bounding box     X ${dim[0].toFixed(3)}  Y ${dim[1].toFixed(3)}  Z ${dim[2].toFixed(3)}  (file units)`);
  // glTF units are metres by spec, so the tallest axis reads as a height.
  const tallest = Math.max(...dim);
  console.log(`  tallest axis     ${tallest.toFixed(3)}  ${tallest > 1.2 && tallest < 2.5
    ? '— consistent with a full body in metres'
    : tallest < 0.6 ? '— too small for a body; a head/bust, or authored in other units'
    : '— neither a standard body height nor a head; check units before scaling'}`);
  // Which axis is up matters: a model lying on its back reconstructs perfectly
  // and is still wrong, and no vertex count will ever show it.
  const upAxis = dim.indexOf(tallest);
  console.log(`  longest axis is  ${'XYZ'[upAxis]}${upAxis === 1 ? ' (Y-up, as glTF expects)' : ' — NOT Y. The model may be rotated; render it before trusting it.'}`);

  // ── verdict ───────────────────────────────────────────────────────────────
  console.log('\n' + '-'.repeat(84));
  const ready = [], needs = [];
  (joints.length ? ready : needs).push(joints.length ? 'skeletal animation (it is rigged)' : 'RIGGING — no skeleton, so nothing can animate it yet');
  (morphTargets ? ready : needs).push(morphTargets ? 'blendshape expressions' : 'FACIAL BLENDSHAPES — none present, so visemes/expressions need authoring');
  (root.listAnimations().length ? ready : needs).push(root.listAnimations().length ? 'existing animation clips' : 'ANIMATION CLIPS — none in the file');
  (texes.length ? ready : needs).push(texes.length ? 'textured rendering' : 'TEXTURES — none embedded');
  console.log('CAN DO NOW:   ' + (ready.length ? ready.join(' · ') : 'nothing beyond static rendering'));
  console.log('NEEDS FIRST:  ' + (needs.length ? needs.join('\n              ') : 'nothing — this is production-ready'));
  console.log('\nThe original file was not modified.');
})();
