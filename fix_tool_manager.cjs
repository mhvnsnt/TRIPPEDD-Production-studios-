const fs = require('fs');

let content = fs.readFileSync('src/server/toolManager.ts', 'utf8');
content = content.replace(
  /private createDef\(id: string, name: string, desc: string\): ToolDefinition \{/,
  "private createDef(id: string, name: string, desc: string, integrationType: any = 'CLI'): ToolDefinition {"
);
content = content.replace(
  /integrationType: 'CLI',/,
  "integrationType,"
);
fs.writeFileSync('src/server/toolManager.ts', content);
