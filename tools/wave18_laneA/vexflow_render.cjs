// Wave 18 Lane A proof: VexFlow (MIT) headless SVG render via jsdom.
// Run: npm install vexflow jsdom   (in this dir or set NODE_PATH)
// Produces: proofs/wave18_vexflow/output.svg
const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!DOCTYPE html><html><body><div id="out"></div></body></html>');
global.window = dom.window;
global.document = dom.window.document;
global.navigator = dom.window.navigator;

const VF = require('vexflow');
const document = dom.window.document;
const div = document.getElementById('out');

const renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);
renderer.resize(640, 220);
const ctx = renderer.getContext();
ctx.setFont('Bravura', 10);

const stave = new VF.Stave(10, 40, 600);
stave.addClef('treble').addTimeSignature('4/4');
stave.setContext(ctx).draw();

// C-major scale fragment, quarter notes
const keys = ['c/4', 'd/4', 'e/4', 'f/4', 'g/4', 'a/4', 'b/4', 'c/5'];
const notes = keys.map((k) => new VF.StaveNote({ keys: [k], duration: 'q', clef: 'treble' }));
const voice = new VF.Voice({ numBeats: 4, beatValue: 4 }).setStrict(false);
voice.addTickables(notes);
new VF.Formatter().joinVoices([voice]).format([voice], 520);
voice.draw(ctx, stave);

const svg = div.innerHTML;
const path = require('path');
const fs = require('fs');
let vfVersion = 'unknown';
try {
  const mainFile = require.resolve('vexflow'); // .../node_modules/vexflow/build/cjs/vexflow.js
  const pkgFile = path.join(path.dirname(mainFile), '..', '..', 'package.json');
  vfVersion = JSON.parse(fs.readFileSync(pkgFile, 'utf8')).version;
} catch (e) { /* version lookup best-effort */ }
const outDir = path.join(__dirname, 'proofs', 'wave18_vexflow');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'output.svg'), svg);
const noteCount = (svg.match(/vf-stavenote/g) || []).length;
console.log(JSON.stringify({
  library: 'vexflow',
  version: vfVersion,
  svg_bytes: svg.length,
  stavenote_groups: noteCount,
  notes_rendered: notes.length,
  artifact: 'tools/wave18_laneA/proofs/wave18_vexflow/output.svg',
}));
