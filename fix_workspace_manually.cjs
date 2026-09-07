const fs = require('fs');

let content = fs.readFileSync('src/components/DriveIngestWorkspace.tsx', 'utf8');

// The render functions are currently inside the useEffect. Let's extract them.
const startIdx = content.indexOf('const renderStatusIcon');
const endIdx = content.indexOf('return () => {');

const renderFunctions = content.substring(startIdx, endIdx);

content = content.replace(renderFunctions, '');

const mainReturnIdx = content.indexOf('return (\n    <div className="h-full');

content = content.slice(0, mainReturnIdx) + renderFunctions + '\n  ' + content.slice(mainReturnIdx);

fs.writeFileSync('src/components/DriveIngestWorkspace.tsx', content);
