const fs = require('fs');
let code = fs.readFileSync('src/components/Sidebar.tsx', 'utf8');

if (!code.includes("id: 'physical_evidence'")) {
  code = code.replace(
    "{ id: 'ingest', label: 'Media Ingest', icon: Video },",
    "{ id: 'ingest', label: 'Media Ingest', icon: Video },\n    { id: 'physical_evidence', label: 'Evidence Review', icon: Search },"
  );
  
  // also add Search to lucide-react import
  if (!code.includes('Search,')) {
    code = code.replace("Settings,", "Settings,\n  Search,");
  }

  fs.writeFileSync('src/components/Sidebar.tsx', code);
  console.log("Sidebar.tsx updated");
}
