// Wave 41 Lane A — threefive.js (keithah/threefive.js, MIT) smoke test.
// Decodes a known SCTE-35 base64 segmentation cue (from threefive's own docs)
// and writes a deterministic JSON proof artifact. No network, no fixtures beyond
// the embedded cue string.
import { Cue } from 'threefive-scte35';
import { writeFileSync } from 'node:fs';

const CUE_B64 = '/DBUAAAAAAAA///wBQb+AAAAAAA+AjxDVUVJAAAACn+/Dy11cm46dXVpZDphYTg1YmJiNi01YzQzLTRiNmEtYmViYi1lZTNiMTNlYjc5OTkRAAB2c6LA';

const cue = new Cue(CUE_B64);

const proof = {
  tool: 'threefive.js (threefive-scte35 npm)',
  upstream: 'https://github.com/keithah/threefive.js',
  license: 'MIT (README license section; verified 2026-10-08)',
  input_format: 'base64',
  splice_command: cue.command?.constructor?.name ?? null,
  table_id: cue.infoSection?.tableId ?? null,
  pts_adjustment: cue.infoSection?.ptsAdjustment ?? null,
  descriptors: (cue.descriptors ?? []).map((d) => ({
    tag: d.tag,
    name: d.name,
    identifier: d.identifier,
    segmentation_type_id: d.segmentationTypeId ?? null,
    segmentation_message: d.segmentationMessage ?? null,
    segmentation_upid_type: d.segmentationUpidType ?? null,
  })),
};

writeFileSync(new URL('./proof_decode.json', import.meta.url), JSON.stringify(proof, null, 2) + '\n');

// Assertions — fail loudly instead of writing a fake artifact.
if (proof.splice_command !== 'TimeSignal') throw new Error('expected TimeSignal command, got ' + proof.splice_command);
if (proof.descriptors.length !== 1) throw new Error('expected 1 descriptor, got ' + proof.descriptors.length);
if (proof.descriptors[0].segmentation_type_id !== 17) {
  throw new Error('unexpected segmentation_type_id: ' + proof.descriptors[0].segmentation_type_id);
}
if (proof.descriptors[0].segmentation_message !== 'Program End') {
  throw new Error('unexpected segmentation message: ' + proof.descriptors[0].segmentation_message);
}
console.log('OK: decoded', proof.splice_command, '+', proof.descriptors[0].segmentation_message);
