/**
 * Test-only real child process for proving the RSS sampler.
 *
 * Deliberately NOT a mock: it is spawned through the same executeTool() path
 * production tools use, so the sampler reads a real /proc entry for a real pid.
 *
 *   node memory_probe.cjs <allocMB> <durationMs>
 *
 * Buffer.alloc zero-fills, which forces the pages to be genuinely resident —
 * a lazy allocation would never show up in RSS and the probe would prove
 * nothing.
 */
const allocMB = Number(process.argv[2] || 200);
const durationMs = Number(process.argv[3] || 2000);

const block = Buffer.alloc(allocMB * 1024 * 1024, 1);

// Keep a reference so the optimiser cannot discard the allocation.
let checksum = 0;
for (let i = 0; i < block.length; i += 1024 * 1024) checksum += block[i];

process.stdout.write(`allocated ${allocMB}MB checksum=${checksum}\n`);

const started = Date.now();
const tick = setInterval(() => {
  if (Date.now() - started >= durationMs) {
    clearInterval(tick);
    process.stdout.write(`held ${Date.now() - started}ms\n`);
    process.exit(0);
  }
}, 25);
