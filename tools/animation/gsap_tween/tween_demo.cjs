// gsap_tween/tween_demo.js — drive a GSAP timeline headlessly and sample it.
// Tweens obj.x 0 -> 100 over 1s with power3.inOut, sampling at 60Hz (61 samples).
// Writes proofs/tween_samples.json and proofs/tween_samples.csv.
const fs = require("fs");
const path = require("path");
if (typeof self === "undefined") globalThis.self = globalThis;
const { gsap } = require("./vendor/gsap.min.cjs");

const HERE = __dirname;
const PROOFS = path.join(HERE, "proofs");
fs.mkdirSync(PROOFS, { recursive: true });

const obj = { x: 0, y: 0 };
const tl = gsap.timeline({ paused: true });
tl.to(obj, { x: 100, duration: 0.5, ease: "power3.inOut" }, 0)
  .to(obj, { y: 50, duration: 0.5, ease: "power2.out" }, 0.5); // 1s total

const N = 61;
const samples = [];
for (let i = 0; i < N; i++) {
  const t = i / (N - 1);
  tl.progress(t);
  samples.push({ t: t, x: obj.x, y: obj.y });
}
const jsonPath = path.join(PROOFS, "tween_samples.json");
const csvPath = path.join(PROOFS, "tween_samples.csv");
fs.writeFileSync(jsonPath, JSON.stringify({ ease: ["power3.inOut", "power2.out"], samples }, null, 2));
fs.writeFileSync(csvPath, "t,x,y\n" + samples.map(s => `${s.t},${s.x},${s.y}`).join("\n") + "\n");
console.log(`wrote ${N} samples -> ${jsonPath}`);
