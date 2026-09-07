const fs = require('fs');
let code = fs.readFileSync('src/components/PhysicalEvidenceWorkspace.tsx', 'utf8');

code = code.replace("style={{ left: \\`\\${(parseFloat(obs.startTime || '0') / 150) * 100}%\\` }}", "style={{ left: `${(parseFloat(obs.startTime || '0') / 150) * 100}%` }}");
code = code.replace("style={{ left: \\`\\${(parseFloat(obs.startTime || '0') / 150) * 100}%\\` }}", "style={{ left: `${(parseFloat(obs.startTime || '0') / 150) * 100}%` }}");

fs.writeFileSync('src/components/PhysicalEvidenceWorkspace.tsx', code);
