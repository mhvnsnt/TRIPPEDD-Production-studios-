import fs from 'fs/promises';
import path from 'path';

const root = process.cwd();
const scanRoots = ['src', 'scripts', 'server.ts', 'production/EP01/generated'];
const sourceExtensions = new Set(['.ts', '.tsx', '.js', '.cjs', '.mjs', '.py']);
const suspiciousPatterns: Array<[string, RegExp]> = [
  ['not-implemented', /not\s+implemented/i],
  ['todo-implementation', /TODO\s*:\s*(implement|finish|complete|replace)/i],
  ['placeholder-implementation', /placeholder\s+(implementation|logic|function)/i],
  ['stub-implementation', /stub\s+(implementation|function|logic)/i],
  ['implement-me', /IMPLEMENT[_ -]?ME/i],
  ['fake-available', /(?:status|healthStatus|installationStatus)\s*[:=]\s*['"]AVAILABLE['"]/i],
];

async function collectFiles(entry: string): Promise<string[]> {
  const absolute = path.join(root, entry);
  let stat;
  try { stat = await fs.stat(absolute); } catch { return []; }
  if (stat.isFile()) return sourceExtensions.has(path.extname(absolute)) ? [absolute] : [];
  const files: string[] = [];
  for (const child of await fs.readdir(absolute)) files.push(...await collectFiles(path.join(entry, child)));
  return files;
}

const files = (await Promise.all(scanRoots.map(collectFiles))).flat();
const findings: Array<{ file: string; line: number; kind: string; text: string }> = [];

for (const file of files) {
  const text = await fs.readFile(file, 'utf8');
  if (!text.trim()) {
    findings.push({ file: path.relative(root, file), line: 1, kind: 'empty-source-file', text: 'Source file is empty.' });
    continue;
  }
  const lines = text.split(/\r?\n/);
  lines.forEach((line, index) => {
    for (const [kind, pattern] of suspiciousPatterns) {
      if (pattern.test(line)) findings.push({ file: path.relative(root, file), line: index + 1, kind, text: line.trim().slice(0, 240) });
    }
  });
}

const report = {
  schemaVersion: 2,
  generatedAt: new Date().toISOString(),
  scannedRoots: scanRoots,
  scannedFiles: files.length,
  status: findings.length ? 'BLOCKED' : 'READY',
  findings,
  policy: {
    emptyProductionSourceIsForbidden: true,
    explicitImplementationStubsAreForbidden: true,
    hardcodedAvailableHealthStateIsForbidden: true,
    documentationMayDescribeUnimplementedWorkOutsideThisScan: true,
  },
};

console.log(JSON.stringify(report, null, 2));
if (findings.length) {
  console.error(`Production integrity audit found ${findings.length} blocking finding(s).`);
  process.exitCode = 2;
} else {
  console.log(`Production integrity audit passed: ${files.length} source files scanned.`);
}
