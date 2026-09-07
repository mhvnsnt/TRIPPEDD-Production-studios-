const fs = require('fs');

let content = fs.readFileSync('src/App.tsx', 'utf8');

content = content.replace(
  "import { EpisodeWorkspace } from './components/EpisodeWorkspace';",
  "import { EpisodeWorkspace } from './components/EpisodeWorkspace';\nimport { DriveIngestWorkspace } from './components/DriveIngestWorkspace';"
);

content = content.replace(
  "case 'story':",
  "case 'ingest':\n        return <DriveIngestWorkspace />;\n      case 'story':"
);

fs.writeFileSync('src/App.tsx', content);

let sidebar = fs.readFileSync('src/components/Sidebar.tsx', 'utf8');

sidebar = sidebar.replace(
  "{ id: 'production', label: 'Active Production', icon: Clapperboard },",
  "{ id: 'production', label: 'Active Production', icon: Clapperboard },\n    { id: 'ingest', label: 'Media Ingest', icon: Video },"
);

fs.writeFileSync('src/components/Sidebar.tsx', sidebar);
