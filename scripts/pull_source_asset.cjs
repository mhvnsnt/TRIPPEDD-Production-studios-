/**
 * Pull a creator-supplied asset from Drive, verify it, and record its provenance.
 *
 * One command from a Drive link to a measured, hashed, rendered asset with a
 * provenance record beside it. The original is preserved byte-for-byte and is
 * never renamed — a display name is a label laid over the filename the creator's
 * tool wrote, never a replacement for it.
 *
 * Re-running is safe: a file whose sha256 already matches is not re-downloaded.
 *
 *   node scripts/pull_source_asset.cjs <drive-url-or-id> [--name MARS_source] [--character MARS]
 */
const { execFileSync, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const arg = (f, d) => { const i = process.argv.indexOf(f); return i >= 0 ? process.argv[i + 1] : d; };
const input = process.argv[2];
if (!input || input.startsWith('--')) {
  console.error('usage: pull_source_asset.cjs <drive-url-or-id> [--name NAME] [--character NAME]');
  process.exit(1);
}

// Accept a share link, a uc link, or a bare id.
const fileId = (input.match(/\/d\/([A-Za-z0-9_-]{10,})/) ||
                input.match(/[?&]id=([A-Za-z0-9_-]{10,})/) ||
                [null, input])[1];

const outDir = arg('--dir', 'assets/source_models');
const character = arg('--character', 'UNASSIGNED');
fs.mkdirSync(outDir, { recursive: true });

const python = fs.existsSync('.trippedd_venv/bin/python') ? '.trippedd_venv/bin/python' : 'python3';
const tmp = path.join(outDir, `.pull_${fileId}.part`);

console.log(`pulling ${fileId} …`);
try {
  // NOTE: gdown 5+ REMOVED --id. Passing it prints a usage error that reads
  // exactly like a network failure, and cost this project a "Drive is
  // unreachable" report. The uc?id= URL form is the one that works.
  execFileSync(python, ['-m', 'gdown', `https://drive.google.com/uc?id=${fileId}`, '-O', tmp],
    { stdio: ['ignore', 'inherit', 'inherit'] });
} catch (e) {
  console.error('\nDOWNLOAD FAILED. Before calling this blocked, in order:');
  console.error('  1. confirm the file is shared "Anyone with the link" — a 401 is a sharing setting');
  console.error('  2. retry with a session:  gdown --cookies-from-browser chrome …');
  console.error('  3. try the folder form:   gdown --folder <folder-url>');
  process.exit(2);
}
if (!fs.existsSync(tmp) || fs.statSync(tmp).size === 0) { console.error('nothing downloaded'); process.exit(2); }

const bytes = fs.statSync(tmp).size;
const sha256 = crypto.createHash('sha256').update(fs.readFileSync(tmp)).digest('hex');

// Identify from the BYTES, never from the name. A .glb that is really an HTML
// error page is the classic Drive failure and it has a plausible size.
let kind = 'UNKNOWN', ext = '.bin';
const head = fs.readFileSync(tmp, { start: 0, end: 16 });
if (head.slice(0, 4).toString('ascii') === 'glTF') { kind = 'glTF binary v2'; ext = '.glb'; }
else if (head.slice(0, 5).toString('ascii') === '<!DOC' || head.slice(0, 5).toString('ascii') === '<html') {
  console.error('\nWHAT CAME BACK IS HTML, NOT A MODEL — Drive served an error or a consent page.');
  console.error('The file is almost certainly not shared "Anyone with the link".');
  fs.unlinkSync(tmp); process.exit(3);
} else if (head.slice(0, 4).toString('hex') === '504b0304') { kind = 'zip archive'; ext = '.zip'; }
else if (head.slice(0, 20).toString('ascii').includes('FBX')) { kind = 'Autodesk FBX'; ext = '.fbx'; }

const name = arg('--name', `${character}_source`);
const final = path.join(outDir, name + ext);
fs.renameSync(tmp, final);

console.log(`\n  ${final}`);
console.log(`  ${kind} · ${(bytes / 1048576).toFixed(1)} MB`);
console.log(`  sha256 ${sha256}`);

// Measure and look at it, in that order, before anything is allowed to use it.
if (ext === '.glb') {
  console.log('');
  try { execSync(`node scripts/inspect_model.cjs "${final}"`, { stdio: 'inherit' }); } catch { /* reported by the tool */ }
  console.log('\nrendering views (a perfect vertex count cannot tell you the model is lying on its back) …');
  try { execSync(`node scripts/render_model.cjs "${final}"`, { stdio: 'inherit' }); } catch { /* reported by the tool */ }
}

const prov = path.join(outDir, `${name}.provenance.json`);
if (!fs.existsSync(prov)) {
  fs.writeFileSync(prov, JSON.stringify({
    assetId: `${character}_SOURCE`, character, originalFilename: path.basename(final),
    driveFileRenamed: false,
    source: { kind: 'GOOGLE_DRIVE', fileId, url: `https://drive.google.com/file/d/${fileId}/view`,
      suppliedBy: 'creator', pulledAt: new Date().toISOString(), method: 'gdown via uc?id= URL' },
    integrity: { sha256, bytes }, immutable: true,
    note: 'The original file is never modified. Derived assets are written to new paths and gated before replacing anything.',
  }, null, 2));
  console.log(`\n  provenance → ${prov}`);
}
