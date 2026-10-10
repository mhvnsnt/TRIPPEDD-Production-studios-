/**
 * LOOK AT THE MODEL. Six views, rendered from the real file.
 *
 * Every number in an inspection report can be perfect while the model is lying
 * on its back, mirrored, or is not the character at all. A vertex count cannot
 * express any of those. This renders the actual geometry so a human decides.
 *
 *   node scripts/render_model.cjs <model.glb> [outDir]
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const http = require('http');

(async () => {
  const file = path.resolve(process.argv[2]);
  const outDir = path.resolve(process.argv[3] ?? 'public/model_views');
  if (!fs.existsSync(file)) { console.error('no such file'); process.exit(1); }
  fs.mkdirSync(outDir, { recursive: true });

  // A local server, because file:// blocks the loader's fetch of its own asset.
  const threeDir = path.join(process.cwd(), 'node_modules', 'three');
  const server = http.createServer((req, res) => {
    const url = decodeURIComponent(req.url.split('?')[0]);
    let p = url === '/model.glb' ? file
      : url.startsWith('/three/') ? path.join(threeDir, url.slice(7))
      : null;
    if (!p || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, {
      'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'application/octet-stream',
      'Access-Control-Allow-Origin': '*',
    });
    fs.createReadStream(p).pipe(res);
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;

  // Resolve the real binary rather than hardcoding a version-stamped path —
  // the directory is chromium-<build>, and a stale literal reads as "no browser".
  const pwRoot = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  const chromeDir = fs.readdirSync(pwRoot).filter((d) => /^chromium-\d+$/.test(d)).sort().pop();
  const exe = chromeDir && path.join(pwRoot, chromeDir, 'chrome-linux', 'chrome');
  const browser = await chromium.launch({
    executablePath: exe && fs.existsSync(exe) ? exe : undefined,
    args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'],
  });
  const page = await browser.newPage({ viewport: { width: 640, height: 640 } });
  page.on('pageerror', (e) => console.error('  page error:', e.message));

  await page.setContent(`<body style="margin:0"><div id="c"></div>
<script type="importmap">{"imports":{"three":"http://127.0.0.1:${port}/three/build/three.module.js","three/addons/":"http://127.0.0.1:${port}/three/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(640, 640);
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.getElementById('c').appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a1e);
scene.add(new THREE.AmbientLight(0xffffff, 1.6));
const key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(2, 3, 4); scene.add(key);
const fill = new THREE.DirectionalLight(0x99bbff, 1.0); fill.position.set(-3, 1, -2); scene.add(fill);
const camera = new THREE.PerspectiveCamera(35, 1, 0.01, 100);
window.__ready = false;
new GLTFLoader().load('http://127.0.0.1:${port}/model.glb', (g) => {
  scene.add(g.scene);
  const box = new THREE.Box3().setFromObject(g.scene);
  window.__center = box.getCenter(new THREE.Vector3()).toArray();
  window.__radius = box.getBoundingSphere(new THREE.Sphere()).radius;
  window.__ready = true;
}, undefined, (e) => { window.__err = String(e); window.__ready = true; });
window.__shoot = (yaw, pitch) => {
  const c = new THREE.Vector3(...window.__center), r = window.__radius;
  const d = r * 3.1;
  camera.position.set(
    c.x + d * Math.cos(pitch) * Math.sin(yaw),
    c.y + d * Math.sin(pitch),
    c.z + d * Math.cos(pitch) * Math.cos(yaw));
  camera.lookAt(c);
  camera.near = r * 0.05; camera.far = r * 20; camera.updateProjectionMatrix();
  renderer.render(scene, camera);
};
</script></body>`);

  await page.waitForFunction('window.__ready === true', { timeout: 180000 });
  const err = await page.evaluate('window.__err');
  if (err) { console.error('LOAD FAILED:', err); await browser.close(); server.close(); process.exit(2); }

  const r = await page.evaluate('window.__radius');
  const c = await page.evaluate('window.__center');
  console.log(`loaded · bounding radius ${r.toFixed(3)} · centre [${c.map((v) => v.toFixed(2)).join(', ')}]`);

  const D = Math.PI / 180;
  const views = [
    ['front', 0, 0], ['right', 90 * D, 0], ['back', 180 * D, 0],
    ['left', 270 * D, 0], ['above', 0, 75 * D], ['three_quarter', 35 * D, 12 * D],
  ];
  const base = path.basename(file, path.extname(file));
  for (const [name, yaw, pitch] of views) {
    await page.evaluate(([y, p]) => window.__shoot(y, p), [yaw, pitch]);
    const out = path.join(outDir, `${base}__${name}.png`);
    await page.locator('canvas').screenshot({ path: out });
    console.log(`  ${name.padEnd(14)} ${out}`);
  }
  await browser.close();
  server.close();
})();
