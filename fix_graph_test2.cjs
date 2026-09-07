const fs = require('fs');

let content = fs.readFileSync('src/core/pipeline/__tests__/productionGraph.test.ts', 'utf8');
content = content.replace(
  "expect(chain[3].name).toBe('Writer Bob');",
  "expect(chain.chain.find((c: any) => c.type === 'RESPONSIBLE_PERSON').name).toBe('Writer Bob');"
);

fs.writeFileSync('src/core/pipeline/__tests__/productionGraph.test.ts', content);
