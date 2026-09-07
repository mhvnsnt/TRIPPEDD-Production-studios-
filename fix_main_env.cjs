const fs = require('fs');
let content = fs.readFileSync('src/main.tsx', 'utf8');
content = content.replace(
  "import.meta.env.VITE_GOOGLE_CLIENT_ID",
  "(import.meta as any).env.VITE_GOOGLE_CLIENT_ID"
);
fs.writeFileSync('src/main.tsx', content);
