/**
 * THE FIRST GOD MOLECULE SHOT — rendered, not described.
 *
 * Deterministic seeded environment + the canonical MARS asset + a camera move,
 * rendered to real frames on disk. Everything here is checked against the
 * bytes: the master's sha256 must match the contract before a single frame is
 * drawn, every frame must exist and be non-empty afterwards, and the frame
 * count must be exact.
 *
 * THERE IS NO FALLBACK IMAGE. If the render fails, the state stays FAILED and
 * says why. A telemetry frame, a placeholder, or a diagram is NOT the shot —
 * substituting one is how a pipeline reports success while producing nothing,
 * which this project has already paid for four times.
 *
 *   node tools/environment/render_first_shot.cjs [--lod LOD1] [--out renders/GM-WORLD-0001-TEST]
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const http = require('http');
const crypto = require('crypto');

const arg = (f, d) => { const i = process.argv.indexOf(f); return i >= 0 ? process.argv[i + 1] : d; };
const CONFIG = JSON.parse(fs.readFileSync('config/god_molecule_first_shot.json', 'utf8'));
const LOD = arg('--lod', CONFIG.subject.renderLod);
const OUT = path.resolve(arg('--out', path.join('renders', CONFIG.shotId)));
const { width, height, fps, frames } = CONFIG.render;

const state = {
  shotId: CONFIG.shotId, worldSeed: CONFIG.worldSeed,
  startedAt: new Date().toISOString(),
  status: 'FAILED', statusReason: 'render did not run',
  telemetrySubstituteUsed: false,
  renderer: 'three.js r1xx via Chromium/SwiftShader (software raster, no GPU in this container)',
};
const die = (reason, code = 1) => {
  state.statusReason = reason;
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, 'shot_state.json'), JSON.stringify(state, null, 2));
  console.error(`\nFAILED: ${reason}`);
  console.error('No substitute frame was written. The shot state records the failure.');
  process.exit(code);
};

(async () => {
  // ── gate 1: the canonical master is who the contract says he is ───────────
  const master = CONFIG.subject.canonicalMaster;
  if (!fs.existsSync(master)) die(`canonical master missing: ${master}`);
  const sha = crypto.createHash('sha256').update(fs.readFileSync(master)).digest('hex');
  if (sha !== CONFIG.subject.canonicalSha256) {
    die(`canonical master hash MISMATCH — this is not the supplied model.\n  expected ${CONFIG.subject.canonicalSha256}\n  got      ${sha}`);
  }
  state.canonicalSha256 = sha;
  state.canonicalVerified = true;

  // The LOD is a decimation OF those bytes, tracked back to them.
  const lodFile = path.join('assets/source_models', `MARS_${LOD}.glb`);
  if (!fs.existsSync(lodFile)) die(`${LOD} missing — run: node scripts/make_lods.cjs ${master} assets/source_models`);
  const lods = JSON.parse(fs.readFileSync('assets/source_models/MARS_lods.json', 'utf8'));
  const lodMeta = lods.lods.find((l) => l.id === LOD);
  state.renderedWith = { lod: LOD, file: lodFile, triangles: lodMeta?.tris,
    derivedFromSha256: lods.master.sha256, derivedFrom: lods.master.file };
  if (lods.master.sha256 !== sha) die('the LOD manifest was built from a DIFFERENT master than the contract names');

  console.log(`${CONFIG.shotId} · seed ${CONFIG.worldSeed} · ${frames} frames @ ${width}x${height} @ ${fps}fps`);
  console.log(`MARS ${LOD} · ${lodMeta?.tris?.toLocaleString()} tris · derived from master ${sha.slice(0, 12)}…`);

  fs.mkdirSync(OUT, { recursive: true });
  const framesDir = path.join(OUT, 'frames');
  fs.rmSync(framesDir, { recursive: true, force: true });
  fs.mkdirSync(framesDir, { recursive: true });

  // ── serve the asset; file:// blocks the loader fetching its own bytes ─────
  const threeDir = path.join(process.cwd(), 'node_modules', 'three');
  const server = http.createServer((req, res) => {
    const u = decodeURIComponent(req.url.split('?')[0]);
    const p = u === '/mars.glb' ? path.resolve(lodFile)
      : u.startsWith('/three/') ? path.join(threeDir, u.slice(7)) : null;
    if (!p || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'application/octet-stream' });
    fs.createReadStream(p).pipe(res);
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;

  const pwRoot = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  const dir = fs.readdirSync(pwRoot).filter((d) => /^chromium-\d+$/.test(d)).sort().pop();
  const exe = dir && path.join(pwRoot, dir, 'chrome-linux', 'chrome');

  const browser = await chromium.launch({
    executablePath: exe && fs.existsSync(exe) ? exe : undefined,
    args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox',
           '--disable-dev-shm-usage', '--js-flags=--max-old-space-size=3072'],
  });
  const page = await browser.newPage({ viewport: { width, height } });
  // Software rasterising a 155k-triangle head takes far longer than the 30s
  // default, and a parse has no progress events to wait on.
  page.setDefaultTimeout(300000);
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(e.message));

  await page.setContent(scenePage(port, CONFIG.worldSeed, width, height, frames, CONFIG.environment.budget));
  // NOTE the null: the signature is waitForFunction(fn, ARG, options). Passing
  // the options object in the second slot makes it the ARGUMENT and leaves the
  // default 30s timeout in place — which reads exactly like a hung scene.
  await page.waitForFunction('window.__ready === true || window.__err', null, { timeout: 300000 });
  const err = await page.evaluate('window.__err');
  if (err) { await browser.close(); server.close(); die(`scene build failed: ${err}`); }

  state.environment = await page.evaluate('window.__envStats');
  console.log(`environment: ${state.environment.instances} instances · ${state.environment.lights} lights · seeded`);

  // ── render every frame, and verify each one as it lands ───────────────────
  const written = [];
  for (let f = 0; f < frames; f++) {
    await page.evaluate((i) => window.__renderFrame(i), f);
    const out = path.join(framesDir, `frame_${String(f).padStart(4, '0')}.png`);
    await page.locator('canvas').screenshot({ path: out });
    const size = fs.existsSync(out) ? fs.statSync(out).size : 0;
    if (size === 0) { await browser.close(); server.close(); die(`frame ${f} wrote 0 bytes`); }
    written.push({ frame: f, file: path.basename(out), bytes: size });
    process.stdout.write(`  frame ${f + 1}/${frames}  ${(size / 1024).toFixed(0)} KB\r`);
  }
  console.log('');
  await browser.close();
  server.close();

  // ── verification, from disk, not from what we think we did ────────────────
  const onDisk = fs.readdirSync(framesDir).filter((f) => f.endsWith('.png')).sort();
  const checks = {
    frameCountExact: onDisk.length === frames,
    allFramesNonEmpty: onDisk.every((f) => fs.statSync(path.join(framesDir, f)).size > 0),
    canonicalHashMatch: state.canonicalVerified === true,
    seedRecorded: Number.isInteger(state.worldSeed),
    noTelemetrySubstitute: state.telemetrySubstituteUsed === false,
    // Eight identical frames would be a still, not a shot. Compare the bytes.
    framesActuallyDiffer: new Set(onDisk.map((f) =>
      crypto.createHash('md5').update(fs.readFileSync(path.join(framesDir, f))).digest('hex'))).size > 1,
    noPageErrors: pageErrors.length === 0,
  };
  state.frames = written;
  state.checks = checks;
  state.pageErrors = pageErrors;
  const allPass = Object.values(checks).every(Boolean);
  state.status = allPass ? 'CREATIVE_FINAL' : 'FAILED';
  state.statusReason = allPass ? 'all verification gates passed against the files on disk'
    : 'failed: ' + Object.entries(checks).filter(([, v]) => !v).map(([k]) => k).join(', ');
  state.finishedAt = new Date().toISOString();
  state.framesDir = framesDir;

  fs.writeFileSync(path.join(OUT, 'shot_state.json'), JSON.stringify(state, null, 2));
  console.log('\nVERIFICATION');
  for (const [k, v] of Object.entries(checks)) console.log(`  ${v ? 'PASS' : 'FAIL'}  ${k}`);
  console.log(`\n${state.status}: ${state.statusReason}`);
  console.log(`frames → ${framesDir}`);
  if (!allPass) process.exit(1);
})().catch((e) => die(`unhandled: ${e.message}`));

/** The scene. Deterministic from the seed — same seed, same world, every run. */
function scenePage(port, seed, width, height, frames, budget) {
  return `<body style="margin:0;overflow:hidden">
<script type="importmap">{"imports":{"three":"http://127.0.0.1:${port}/three/build/three.module.js","three/addons/":"http://127.0.0.1:${port}/three/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// mulberry32 — small, fast, and DETERMINISTIC. The same seed must rebuild the
// same world on any machine, or the shot is not reproducible.
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const rand = rng(${seed});

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(${width}, ${height});
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x05030f);
scene.fog = new THREE.FogExp2(0x0a0520, 0.055);

// Starfield — the God Molecule void the character floats in.
const starGeo = new THREE.BufferGeometry();
const STARS = 1400, sp = new Float32Array(STARS * 3), sc = new Float32Array(STARS * 3);
const starPalette = [[1,1,1],[0.6,0.8,1],[1,0.7,0.9],[0.8,1,0.9],[1,0.9,0.6]];
for (let i = 0; i < STARS; i++) {
  const r = 26 + rand() * 40, th = rand() * Math.PI * 2, ph = Math.acos(2 * rand() - 1);
  sp[i*3] = r*Math.sin(ph)*Math.cos(th); sp[i*3+1] = r*Math.cos(ph); sp[i*3+2] = r*Math.sin(ph)*Math.sin(th);
  const c = starPalette[(rand() * starPalette.length) | 0];
  sc[i*3] = c[0]; sc[i*3+1] = c[1]; sc[i*3+2] = c[2];
}
starGeo.setAttribute('position', new THREE.BufferAttribute(sp, 3));
starGeo.setAttribute('color', new THREE.BufferAttribute(sc, 3));
scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ size: 0.17, vertexColors: true, sizeAttenuation: true })));

// Seeded floating geometry — instanced, so the whole environment is a handful
// of draw calls rather than one per shard.
const MAX = ${budget.maxInstances};
const shardGeo = new THREE.IcosahedronGeometry(1, 0);
const shardMat = new THREE.MeshStandardMaterial({ color: 0x2a1b6e, emissive: 0x140a3c, metalness: 0.35, roughness: 0.45, flatShading: true });
const shards = new THREE.InstancedMesh(shardGeo, shardMat, MAX);
const m = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), s = new THREE.Vector3();
const shardSeeds = [];
for (let i = 0; i < MAX; i++) {
  const ang = rand() * Math.PI * 2, rad = 3.2 + rand() * 13, hgt = (rand() - 0.5) * 9;
  v.set(Math.cos(ang) * rad, hgt, Math.sin(ang) * rad);
  e.set(rand() * Math.PI, rand() * Math.PI, rand() * Math.PI); q.setFromEuler(e);
  const sc2 = 0.18 + rand() * 0.85; s.set(sc2, sc2 * (0.6 + rand()), sc2);
  m.compose(v, q, s); shards.setMatrixAt(i, m);
  shardSeeds.push({ pos: v.clone(), quat: q.clone(), scl: s.clone(), drift: 0.2 + rand() * 0.8 });
}
shards.instanceMatrix.needsUpdate = true;
scene.add(shards);

// Light rig: cold key, magenta rim, deep fill — the show's palette.
const key = new THREE.DirectionalLight(0x9fd0ff, 3.0); key.position.set(3, 4, 5); scene.add(key);
const rim = new THREE.PointLight(0xff3fae, 26, 30); rim.position.set(-3.4, 1.3, -3.6); scene.add(rim);
const fill = new THREE.PointLight(0x3b6bff, 20, 26); fill.position.set(3.2, -1.6, 2.4); scene.add(fill);
scene.add(new THREE.AmbientLight(0x2a2550, 1.5));

const camera = new THREE.PerspectiveCamera(38, ${width} / ${height}, 0.05, 120);
window.__envStats = { instances: MAX, lights: 4, stars: STARS, seeded: true };
window.__ready = false;

new GLTFLoader().load('http://127.0.0.1:${port}/mars.glb', (g) => {
  const mars = g.scene;
  const box = new THREE.Box3().setFromObject(mars);
  const size = box.getSize(new THREE.Vector3());
  const centre = box.getCenter(new THREE.Vector3());
  // Normalise to a known head height so the camera framing is seed-independent.
  const k = 1.6 / Math.max(size.x, size.y, size.z);
  mars.scale.setScalar(k);
  mars.position.set(-centre.x * k, -centre.y * k, -centre.z * k);
  const pivot = new THREE.Group(); pivot.add(mars); scene.add(pivot);
  window.__mars = pivot;
  window.__ready = true;
}, undefined, (err) => { window.__err = 'GLB load failed: ' + err; window.__ready = true; });

window.__renderFrame = (i) => {
  const t = i / ${frames};           // 0..1 across the shot
  // Slow orbital push-in. Deterministic: frame index in, camera out.
  const ang = -0.55 + t * 0.85;
  const dist = 4.5 - t * 0.85;
  camera.position.set(Math.sin(ang) * dist, 0.35 + Math.sin(t * Math.PI) * 0.28, Math.cos(ang) * dist);
  camera.lookAt(0, 0.05, 0);
  if (window.__mars) window.__mars.rotation.y = -0.18 + t * 0.34;
  // The world drifts; a static environment behind a moving camera reads as a
  // photograph on a turntable.
  for (let j = 0; j < MAX; j++) {
    const sd = shardSeeds[j];
    v.copy(sd.pos); v.y += Math.sin(t * Math.PI * 2 + j) * 0.14 * sd.drift;
    e.set(sd.quat.x + t * 0.4 * sd.drift, sd.quat.y + t * 0.5 * sd.drift, sd.quat.z);
    q.setFromEuler(e);
    m.compose(v, q, sd.scl); shards.setMatrixAt(j, m);
  }
  shards.instanceMatrix.needsUpdate = true;
  rim.intensity = 22 + Math.sin(t * Math.PI * 2) * 8;
  renderer.render(scene, camera);
};
</script></body>`;
}
