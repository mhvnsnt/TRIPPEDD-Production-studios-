const fs = require('fs');
let appCode = fs.readFileSync('src/App.tsx', 'utf8');

if (!appCode.includes('PhysicalEvidenceWorkspace')) {
  appCode = appCode.replace(
    "import { ProductionControlWorkspace } from './components/ProductionControlWorkspace';",
    "import { ProductionControlWorkspace } from './components/ProductionControlWorkspace';\nimport { PhysicalEvidenceWorkspace } from './components/PhysicalEvidenceWorkspace';"
  );

  appCode = appCode.replace(
    "case 'production':",
    "case 'physical_evidence':\n        return <PhysicalEvidenceWorkspace />;\n      case 'production':"
  );
  
  fs.writeFileSync('src/App.tsx', appCode);
  console.log("App.tsx updated");
}
