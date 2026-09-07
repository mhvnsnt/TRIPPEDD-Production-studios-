const fs = require('fs');

let appContent = fs.readFileSync('src/App.tsx', 'utf8');

appContent = appContent.replace(
  "import { DriveIngestWorkspace } from './components/DriveIngestWorkspace';",
  "import { DriveIngestWorkspace } from './components/DriveIngestWorkspace';\nimport { PeopleCastWorkspace } from './components/PeopleCastWorkspace';"
);

appContent = appContent.replace(
  "case 'studio_ops':\n        return <StudioOpsWorkspace />;",
  "case 'studio_ops':\n        return <StudioOpsWorkspace />;\n      case 'people_cast':\n        return <PeopleCastWorkspace />;"
);

fs.writeFileSync('src/App.tsx', appContent);

let sidebarContent = fs.readFileSync('src/components/Sidebar.tsx', 'utf8');

sidebarContent = sidebarContent.replace(
  "{ id: 'studio_ops', label: 'Studio Ops', icon: <Kanban size={18} /> },",
  "{ id: 'studio_ops', label: 'Studio Ops', icon: <Kanban size={18} /> },\n    { id: 'people_cast', label: 'People & Cast', icon: <Users size={18} /> },"
);

fs.writeFileSync('src/components/Sidebar.tsx', sidebarContent);

console.log("App and Sidebar updated");
