const fs = require('fs');
let content = fs.readFileSync('src/components/Sidebar.tsx', 'utf8');

// Add Users icon import
content = content.replace("import {\n  Film,", "import {\n  Users,\n  Film,");

// Add Studio Ops to studioItems
content = content.replace(
  "{ id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },",
  "{ id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },\n    { id: 'studio_ops', label: 'Studio Operations', icon: Users },"
);

fs.writeFileSync('src/components/Sidebar.tsx', content);
