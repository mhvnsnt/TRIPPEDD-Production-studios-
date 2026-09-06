const fs = require('fs');

let content = fs.readFileSync('src/App.tsx', 'utf8');

content = content.replace(
  "import { AssetWorkspace } from './components/AssetWorkspace';",
  "import { AssetWorkspace } from './components/AssetWorkspace';\nimport { FormatsWorkspace } from './components/FormatsWorkspace';"
);

content = content.replace(
  "case 'bible':",
  "case 'formats':\n        return <FormatsWorkspace />;\n      case 'bible':"
);

fs.writeFileSync('src/App.tsx', content);
