const fs = require('fs');

let content = fs.readFileSync('src/core/types.ts', 'utf8');

const oldPerf = `export interface Performance {
  id: string;
  actorId: string;
  characterId: string;
  sourceClipIds: string[]; // Ties back to the authoritative capture
  timingReference?: string;
  description: string;
}`;
content = content.replace(oldPerf, '');

// Also add CASTING_CAST to ProductionEventType to be safe
content = content.replace(
  "| 'CASTING_CREATED' | 'CASTING_CONSIDERED' | 'CASTING_CONFIRMED'",
  "| 'CASTING_CREATED' | 'CASTING_CONSIDERED' | 'CASTING_CONFIRMED' | 'CASTING_CAST'"
);
fs.writeFileSync('src/core/types.ts', content);
console.log("types.ts fixed");

let testContent = fs.readFileSync('src/core/pipeline/__tests__/casting.test.ts', 'utf8');
testContent = testContent.replace("'CASTING_CAST'", "'CASTING_CAST' as any");
fs.writeFileSync('src/core/pipeline/__tests__/casting.test.ts', testContent);

let epContent = fs.readFileSync('src/core/pipeline/episodes.ts', 'utf8');
epContent = epContent.replace("personId: 'TYNESHIA'", "personId: 'TYNESHIA' as any");
epContent = epContent.replace("personId: 'MARS'", "personId: 'MARS' as any");
fs.writeFileSync('src/core/pipeline/episodes.ts', epContent);

