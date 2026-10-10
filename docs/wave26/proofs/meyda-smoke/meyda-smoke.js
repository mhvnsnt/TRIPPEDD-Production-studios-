// Meyda smoke test — extracts audio features from a synthesized WAV.
// Reads test-440.wav (2s mono 16-bit PCM: 440Hz sine + 880Hz harmonic),
// parses the PCM16 payload manually, and runs Meyda.extract on one
// 512-sample frame plus a full-buffer MFCC/chroma pass.
const fs = require('fs');
const Meyda = require('meyda');

const buf = fs.readFileSync('test-440.wav');
// Minimal WAV parse: find 'data' chunk, assume 16-bit PCM mono.
const dataIdx = buf.indexOf(Buffer.from('data'));
const dataStart = dataIdx + 8;
const dataLen = buf.readUInt32LE(dataIdx + 4);
const n = dataLen / 2;
const signal = new Float32Array(n);
for (let i = 0; i < n; i++) signal[i] = buf.readInt16LE(dataStart + i * 2) / 32768;

Meyda.bufferSize = 512;
Meyda.sampleRate = 44100;

const frame = signal.slice(0, 512);
const features = Meyda.extract(
  ['rms', 'energy', 'spectralCentroid', 'spectralRolloff', 'zcr', 'mfcc', 'chroma', 'spectralFlatness'],
  frame
);

// Full-buffer MFCC mean (frames of 512, hop 512).
const mfccFrames = [];
for (let o = 0; o + 512 <= n; o += 512) {
  mfccFrames.push(Meyda.extract('mfcc', signal.slice(o, o + 512)));
}
const mfccMean = mfccFrames[0].map((_, k) =>
  mfccFrames.reduce((s, f) => s + f[k], 0) / mfccFrames.length
);

const out = {
  tool: 'meyda',
  version: require('meyda/package.json').version,
  license: 'MIT (github.com/hughrawlinson/meyda)',
  input: 'test-440.wav — 2s mono 16-bit PCM @44100Hz, 440Hz sine + 0.4*880Hz harmonic (synthesized, no copyrighted audio)',
  frame0: {
    rms: features.rms,
    energy: features.energy,
    spectralCentroid: features.spectralCentroid,
    spectralRolloff: features.spectralRolloff,
    zeroCrossingRate: features.zcr,
    spectralFlatness: features.spectralFlatness,
    mfcc_first5: features.mfcc.slice(0, 5),
    chroma_peak_bin: features.chroma.indexOf(Math.max(...features.chroma)),
  },
  mfcc_mean_first5_over_full_buffer: mfccMean.slice(0, 5),
  frames_analyzed: mfccFrames.length,
};
fs.writeFileSync('meyda-smoke-output.json', JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
console.log('SMOKE-TEST PASS: meyda extracted features from real synthesized audio');
