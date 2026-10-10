// Wave 18 Lane A proof: abcjs (MIT) headless ABC->SVG render via jsdom.
// Run: npm install abcjs jsdom   (in this dir or set NODE_PATH)
// Produces: proofs/wave18_abcjs/output.svg
const { JSDOM } = require('jsdom');

const dom = new JSDOM('<!DOCTYPE html><html><body><div id="paper"></div></body></html>');
global.window = dom.window;
global.document = dom.window.document;
global.navigator = dom.window.navigator;

const abcjs = require('abcjs');

const abc = `X:1
T:Wave18 smoke test — Cooley's Reel fragment
M:4/4
L:1/8
K:Emin
EE FG|AFdF|eB~B2|eB~B2|EE FG|AFdF|eB BA|1 FE D2:|2 FE E2|]`;

const visualObjs = abcjs.renderAbc(document.getElementById('paper'), abc, {
  responsive: 'resize',
});
const svg = document.getElementById('paper').innerHTML;
const fs = require('fs');
const path = require('path');
const outDir = path.join(__dirname, 'proofs', 'wave18_abcjs');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'output.svg'), svg);
console.log(JSON.stringify({
  library: 'abcjs',
  tunes_parsed: visualObjs.length,
  svg_bytes: svg.length,
  has_title: svg.includes('Cooley'),
  artifact: 'tools/wave18_laneA/proofs/wave18_abcjs/output.svg',
}));
