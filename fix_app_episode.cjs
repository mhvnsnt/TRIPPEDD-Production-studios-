const fs = require('fs');

let content = fs.readFileSync('src/App.tsx', 'utf8');

content = content.replace(
  "import { FormatsWorkspace } from './components/FormatsWorkspace';",
  "import { FormatsWorkspace } from './components/FormatsWorkspace';\nimport { EpisodeWorkspace } from './components/EpisodeWorkspace';"
);

content = content.replace(
  "case 'story':",
  "case 'episodes':\n        return <EpisodeWorkspace />;\n      case 'story':"
);

fs.writeFileSync('src/App.tsx', content);

let sidebar = fs.readFileSync('src/components/Sidebar.tsx', 'utf8');

sidebar = sidebar.replace(
  "{ id: 'story', label: 'Story / Fiction', icon: PenTool },",
  "{ id: 'story', label: 'Story / Fiction', icon: PenTool },\n    { id: 'episodes', label: 'Episode Pipeline', icon: Film },"
);

sidebar = sidebar.replace(
  "{ id: 'production', label: 'Production', icon: Film },",
  "{ id: 'production', label: 'Active Production', icon: Clapperboard },"
);

fs.writeFileSync('src/components/Sidebar.tsx', sidebar);
