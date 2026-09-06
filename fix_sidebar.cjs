const fs = require('fs');

let content = fs.readFileSync('src/components/Sidebar.tsx', 'utf8');

content = content.replace(
  "{ id: 'bible', label: 'Show Bible', icon: BookOpen },",
  "{ id: 'bible', label: 'Show Bible', icon: BookOpen },\n      { id: 'formats', label: 'Formats & Lore', icon: BookOpen },"
);

fs.writeFileSync('src/components/Sidebar.tsx', content);
