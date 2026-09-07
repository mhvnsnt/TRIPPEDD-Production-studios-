const fs = require('fs');

let comp = fs.readFileSync('src/components/ToolManager.tsx', 'utf8');
comp = comp.replace(/INSTALLED/g, 'AVAILABLE');
comp = comp.replace(/NOT_CHECKED/g, 'UNAVAILABLE');
comp = comp.replace(/CONFIGURED/g, 'AVAILABLE');
comp = comp.replace(/CONNECTED/g, 'AVAILABLE');
comp = comp.replace(/RUNNING/g, 'INSTALLING');
comp = comp.replace(/ERROR/g, 'INSTALL_FAILED');
comp = comp.replace(/NOT_IMPLEMENTED/g, 'UNAVAILABLE');
comp = comp.replace(/UNSUPPORTED/g, 'VERSION_UNSUPPORTED');
fs.writeFileSync('src/components/ToolManager.tsx', comp);

console.log('Fixed ToolManager component');
