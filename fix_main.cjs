const fs = require('fs');
let content = fs.readFileSync('src/main.tsx', 'utf8');

content = content.replace(
  "import App from './App.tsx'",
  "import App from './App.tsx'\nimport { GoogleOAuthProvider } from '@react-oauth/google';"
);

content = content.replace(
  "<App />",
  "<GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID || ''}>\n      <App />\n    </GoogleOAuthProvider>"
);

fs.writeFileSync('src/main.tsx', content);
