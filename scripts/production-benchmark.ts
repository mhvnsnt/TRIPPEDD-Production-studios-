import { performance } from 'node:perf_hooks';
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const reportDir = path.join(root, 'public', 'production');
const reportPath = path.join(reportDir, 'production-benchmark.json');

type Stage = { name: string; command: string; args: string[]; startedAt: string; durationMs: number; ok: boolean; error?: string };

function run(command: string, args: string[]) {
  return new Promise<void>((resolve, reject) => {
    const child = spawn(command, args, { cwd: root, stdio: ['ignore', 'pipe', 'pipe'] });
    let stderr = '';
    child.stderr.on('data', chunk => { stderr += chunk.toString(); });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}: ${stderr.slice(-2000)}`)));
  });
}

const stages: Stage[] = [];
async function timed(name: string, command: string, args: string[]) {
  const startedAt = new Date().toISOString();
  const start = performance.now();
  try {
    await run(command, args);
    stages.push({ name, command, args, startedAt, durationMs: Math.round(performance.now() - start), ok: true });
  } catch (error) {
    stages.push({ name, command, args, startedAt, durationMs: Math.round(performance.now() - start), ok: false, error: error instanceof Error ? error.message : String(error) });
    throw error;
  }
}

await timed('typecheck', 'bun', ['run', 'lint']);

const report = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  gitSha: process.env.GITHUB_SHA || 'local',
  stages,
  totalDurationMs: stages.reduce((sum, stage) => sum + stage.durationMs, 0),
  purpose: 'Measure repeatable pipeline overhead so speed improvements are evidence-based rather than estimated.'
};

await fs.mkdir(reportDir, { recursive: true });
await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
