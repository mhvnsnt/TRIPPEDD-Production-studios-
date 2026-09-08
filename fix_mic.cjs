const fs = require('fs');

const path = 'src/components/PhysicalEvidenceWorkspace.tsx';
let source = fs.readFileSync(path, 'utf8');

if (source.includes('<Mic ')) {
  const importPattern = /import \{([^}]+)\} from 'lucide-react';/;
  const match = source.match(importPattern);
  if (match && !match[1].split(',').map(s => s.trim()).includes('Mic')) {
    const icons = match[1].trim();
    source = source.replace(importPattern, `import { ${icons}, Mic } from 'lucide-react';`);
  }
}

fs.writeFileSync(path, source);
