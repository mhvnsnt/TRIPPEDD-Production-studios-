import { describe, it, expect } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'fs';
import path from 'path';

/**
 * Structural enforcement of the ADAPTER_DEFINED / EXECUTED distinction.
 *
 * Rather than trusting every future edit to be careful, this scans the source
 * tree: the evidence marker may only be constructed inside the sanctioned
 * executor, which cannot produce it without spawning a real process. If someone
 * hand-writes `executionState: 'EXECUTED'` anywhere else, the build fails here.
 */
const SRC = path.join(process.cwd(), 'src');
const SANCTIONED = path.join('src', 'core', 'tools', 'execution', 'executor.ts');

function walk(dir: string, out: string[] = []): string[] {
  for (const e of readdirSync(dir)) {
    const p = path.join(dir, e);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (/\.tsx?$/.test(e)) out.push(p);
  }
  return out;
}

describe('Execution integrity — EXECUTED cannot be fabricated', () => {
  const files = walk(SRC);

  it('only the sanctioned executor constructs the EXECUTED marker', () => {
    const offenders: string[] = [];

    for (const f of files) {
      const rel = path.relative(process.cwd(), f);
      if (rel === SANCTIONED) continue;
      if (rel.includes('__tests__')) continue;

      const src = readFileSync(f, 'utf8');
      // Assignment form: executionState: 'EXECUTED'
      const assigns = src.match(/executionState\s*:\s*['"`]EXECUTED['"`]/g);
      if (assigns) offenders.push(`${rel} (${assigns.length}x)`);
    }

    expect(offenders, `EXECUTED constructed outside ${SANCTIONED}: ${offenders.join(', ')}`).toEqual([]);
  });

  it('the sanctioned executor actually spawns a process', () => {
    const src = readFileSync(path.join(process.cwd(), SANCTIONED), 'utf8');
    expect(src).toMatch(/from ['"]child_process['"]/);
    expect(src).toMatch(/spawn\(/);
    // The marker and the spawn live in the same module by design.
    expect(src).toMatch(/executionState:\s*'EXECUTED'/);
  });

  it('no analyzer or queue module fabricates a COMPLETED tool status without a run', () => {
    // The specific historical bug: queueManager marked tools COMPLETED with a
    // literal command string and no process. Assert that shape is gone.
    const q = readFileSync(path.join(process.cwd(), 'src', 'server', 'queueManager.ts'), 'utf8');
    expect(q).not.toMatch(/command:\s*['"`]cv2\.VideoCapture['"`]/);
    expect(q).not.toMatch(/executionState:\s*['"`]EXECUTED['"`]/);
  });
});
