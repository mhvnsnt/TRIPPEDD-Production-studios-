const fs = require('fs');

let content = fs.readFileSync('src/core/types.ts', 'utf8');

// Ensure executablePath is inside ToolDefinition
if (!content.includes('executablePath?: string;')) {
   content = content.replace('capabilities: ToolCapability;', 'capabilities: ToolCapability;\n  executablePath?: string;\n  installSource?: string;\n  installError?: string;\n  runtimeRequirements?: { cpu?: boolean; gpu?: boolean; ramMB?: number; };');
}
fs.writeFileSync('src/core/types.ts', content);

// Fix ToolManager signature
let tm = fs.readFileSync('src/server/toolManager.ts', 'utf8');
tm = tm.replace(/private createDef\(id: string, name: string, desc: string\)/, 'private createDef(id: string, name: string, desc: string, integrationType: any = "CLI")');
fs.writeFileSync('src/server/toolManager.ts', tm);

console.log('Fixed types');
