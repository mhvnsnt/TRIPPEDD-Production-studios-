/**
 * LOD ladder for a canonical character asset.
 *
 * The supplied Mars head is 1.94M triangles. That is a raw generation output,
 * not a shot-weight asset, and carrying it through every 8-frame test is how a
 * renderer runs out of memory on work that did not need the detail.
 *
 * The ORIGINAL IS NEVER TOUCHED. Each LOD is written to its own path, and every
 * one is re-read from the bytes that were written and checked: triangle count
 * actually fell, vertices only shrank, and the bounding box did not move — a
 * simplifier that silently drops a texture or collapses the silhouette produces
 * a smaller file and a different character.
 *
 *   node scripts/make_lods.cjs <source.glb> [outDir]
 */
const { NodeIO } = require('@gltf-transform/core');
const { ALL_EXTENSIONS } = require('@gltf-transform/extensions');
const { simplify, weld, textureCompress } = require('@gltf-transform/functions');
const { MeshoptSimplifier } = require('meshoptimizer');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// LOD 0 is the master. Ratios are of the ORIGINAL triangle count.
const LADDER = [
  { id: 'LOD1', ratio: 0.08, error: 0.002, texture: 2048, role: 'production mesh — hero shots' },
  { id: 'LOD2', ratio: 0.02, error: 0.008, texture: 1024, role: 'animation / test mesh' },
  { id: 'LOD3', ratio: 0.005, error: 0.02, texture: 512, role: 'preview proxy — cheap iteration' },
];

function measure(doc) {
  const root = doc.getRoot();
  let tris = 0, verts = 0;
  let min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
  for (const mesh of root.listMeshes()) {
    for (const p of mesh.listPrimitives()) {
      const pos = p.getAttribute('POSITION');
      if (!pos) continue;
      verts += pos.getCount();
      const idx = p.getIndices();
      tris += idx ? idx.getCount() / 3 : pos.getCount() / 3;
      const el = [0, 0, 0];
      for (let i = 0; i < pos.getCount(); i++) {
        pos.getElement(i, el);
        for (let k = 0; k < 3; k++) { if (el[k] < min[k]) min[k] = el[k]; if (el[k] > max[k]) max[k] = el[k]; }
      }
    }
  }
  return { tris: Math.round(tris), verts, textures: root.listTextures().length,
           bbox: max.map((v, i) => +(v - min[i]).toFixed(4)) };
}

(async () => {
  const src = path.resolve(process.argv[2]);
  const outDir = path.resolve(process.argv[3] ?? path.dirname(src));
  fs.mkdirSync(outDir, { recursive: true });
  await MeshoptSimplifier.ready;

  const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
  const master = measure(await io.read(src));
  const base = path.basename(src, '.glb').replace(/_source$/, '');

  console.log(`MASTER (never modified)  ${path.basename(src)}`);
  console.log(`  ${master.tris.toLocaleString()} tris · ${master.verts.toLocaleString()} verts · ` +
              `${master.textures} textures · bbox ${master.bbox.join(' x ')}\n`);

  const manifest = { master: { file: path.basename(src), ...master,
    sha256: crypto.createHash('sha256').update(fs.readFileSync(src)).digest('hex') }, lods: [] };

  for (const step of LADDER) {
    const doc = await io.read(src);
    // Weld first: an unwelded mesh has no shared edges, so the simplifier has
    // nothing to collapse and quietly does almost nothing.
    await doc.transform(weld());

    // ITERATE. meshoptimizer enforces an error bound per pass and simply stops
    // when reaching the ratio would exceed it — measured here, a single pass
    // parked all three LODs at ~173k triangles no matter what ratio was asked
    // for, so LOD2 and LOD3 differed from LOD1 only in texture size. Feeding
    // each pass its own output, with the error allowance widening as detail is
    // already gone, actually walks the count down.
    const target = Math.round(master.tris * step.ratio);
    let error = step.error;
    for (let pass = 1; pass <= 8; pass++) {
      const before = measure(doc).tris;
      if (before <= target) break;
      // Never ask for less than a third in one go; a huge jump is what trips
      // the error bound into refusing outright.
      const ratio = Math.max(0.34, target / before);
      await doc.transform(simplify({ simplifier: MeshoptSimplifier, ratio, error }));
      const after = measure(doc).tris;
      if (after >= before * 0.98) {
        // No progress at this error allowance. Widen it once, then give up and
        // report the floor honestly rather than looping forever.
        if (error >= step.error * 8) {
          console.log(`  (simplifier floor reached at ${after.toLocaleString()} tris after ${pass} pass(es))`);
          break;
        }
        error *= 2;
      }
    }
    await doc.transform(textureCompress({ targetFormat: 'jpeg', resize: [step.texture, step.texture] }));
    const out = path.join(outDir, `${base}_${step.id}.glb`);
    await io.write(out, doc);

    // Re-read the SHIPPED BYTES. Measuring the in-memory document would report
    // what we intended rather than what landed on disk.
    const got = measure(await io.read(out));
    const bytes = fs.statSync(out).size;
    const moved = got.bbox.some((v, i) => Math.abs(v - master.bbox[i]) > master.bbox[i] * 0.02);

    const problems = [];
    if (got.tris >= master.tris) problems.push('triangles did not fall');
    if (got.verts > master.verts) problems.push('vertices GREW');
    if (got.textures !== master.textures) problems.push(`textures ${master.textures} -> ${got.textures}`);
    if (moved) problems.push(`silhouette moved: bbox ${got.bbox.join(' x ')}`);

    console.log(`${step.id}  ${step.role}`);
    console.log(`  ${got.tris.toLocaleString()} tris (${(100 * got.tris / master.tris).toFixed(1)}% of master) · ` +
                `${(bytes / 1048576).toFixed(1)} MB · ${step.texture}px textures`);
    if (problems.length) { console.log(`  REJECTED: ${problems.join('; ')}`); fs.unlinkSync(out); continue; }
    console.log(`  verified from the written bytes · ${out}`);
    manifest.lods.push({ id: step.id, role: step.role, file: path.basename(out), bytes, ...got });
  }

  const mf = path.join(outDir, `${base}_lods.json`);
  fs.writeFileSync(mf, JSON.stringify(manifest, null, 2));
  console.log(`\nmanifest → ${mf}`);
})();
