/**
 * Deterministic working directory for spawned tools.
 *
 * Every tool process is launched with an EXPLICIT cwd rather than inheriting
 * whatever directory the caller happened to be in. The cwd is then recorded in
 * provenance, so a run can be reproduced exactly.
 *
 * Resolution order: an explicit TRIPPEDD_ROOT override, then the nearest
 * ancestor of the process cwd containing a package.json, then the process cwd
 * itself. `process.chdir` is never called — the global cwd stays untouched.
 */
import path from 'path';
import { existsSync } from 'fs';

let cached: string | undefined;

export function resolveRunnerRoot(startFrom: string = process.cwd()): string {
  const override = process.env.TRIPPEDD_ROOT;
  if (override && existsSync(override)) return override;

  let dir = path.resolve(startFrom);
  for (let i = 0; i < 20; i++) {
    if (existsSync(path.join(dir, 'package.json'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return path.resolve(startFrom);
}

export function runnerRoot(): string {
  if (cached === undefined) cached = resolveRunnerRoot();
  return cached;
}

/** Test seam: clears the memoised root. */
export function __resetRunnerRoot(): void {
  cached = undefined;
}
