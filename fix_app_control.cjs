const fs = require('fs');

let appContent = fs.readFileSync('src/App.tsx', 'utf8');
appContent = appContent.replace(
  "import { PeopleCastWorkspace } from './components/PeopleCastWorkspace';",
  "import { PeopleCastWorkspace } from './components/PeopleCastWorkspace';\nimport { ProductionControlWorkspace } from './components/ProductionControlWorkspace';"
);
appContent = appContent.replace(
  "case 'people_cast':\n        return <PeopleCastWorkspace />;",
  "case 'people_cast':\n        return <PeopleCastWorkspace />;\n      case 'control':\n        return <ProductionControlWorkspace />;"
);
fs.writeFileSync('src/App.tsx', appContent);

let sidebarContent = fs.readFileSync('src/components/Sidebar.tsx', 'utf8');
sidebarContent = sidebarContent.replace(
  "{ id: 'people_cast', label: 'People & Cast', icon: <Users size={18} /> },",
  "{ id: 'people_cast', label: 'People & Cast', icon: <Users size={18} /> },\n    { id: 'control', label: 'Production Control', icon: <Kanban size={18} /> },"
);
fs.writeFileSync('src/components/Sidebar.tsx', sidebarContent);
