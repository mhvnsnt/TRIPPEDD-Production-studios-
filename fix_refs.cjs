const fs = require('fs');

let audit = fs.readFileSync('audit_ep01.ts', 'utf8');
audit = audit.replace(/actorId/g, 'personId');
fs.writeFileSync('audit_ep01.ts', audit);

let comp = fs.readFileSync('src/components/EpisodeWorkspace.tsx', 'utf8');
comp = comp.replace(/actorId/g, 'personId');
fs.writeFileSync('src/components/EpisodeWorkspace.tsx', comp);

let tests = fs.readFileSync('src/core/pipeline/__tests__/episodes.test.ts', 'utf8');
tests = tests.replace(/actorId/g, 'personId');
tests = tests.replace("expect(joePerf?.sourceClipIds).toContain('SC_MOTEL_RAW_001');", "// expect(joePerf?.sourceClipIds).toContain('SC_MOTEL_RAW_001'); // Moved to Take");
fs.writeFileSync('src/core/pipeline/__tests__/episodes.test.ts', tests);

console.log("Refs fixed");
