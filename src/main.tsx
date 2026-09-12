import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import App from './App.tsx';
import { GoogleOAuthProvider } from '@react-oauth/google';

import './index.css';
import { ProductionProvider } from './context.tsx';
import { initTools } from './core/tools/init.ts';
import './micGlobal.ts';

initTools();

const googleClientId = (import.meta as any).env.VITE_GOOGLE_CLIENT_ID as string | undefined;

function AppWithOptionalAuth() {
  const app = <App />;

  // Google OAuth is an optional integration. The studio itself must remain
  // bootable in local/dev environments where OAuth credentials are not set.
  if (!googleClientId?.trim()) {
    return app;
  }

  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      {app}
    </GoogleOAuthProvider>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ProductionProvider>
      <AppWithOptionalAuth />
    </ProductionProvider>
  </StrictMode>,
);
