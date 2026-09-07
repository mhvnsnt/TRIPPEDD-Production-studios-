import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import App from './App.tsx'
import { GoogleOAuthProvider } from '@react-oauth/google';

// @ts-ignore;
import './index.css';
import { ProductionProvider } from './context.tsx';
import { initTools } from './core/tools/init.ts';

initTools();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ProductionProvider>
      <GoogleOAuthProvider clientId={(import.meta as any).env.VITE_GOOGLE_CLIENT_ID || ''}>
      <App />
    </GoogleOAuthProvider>
    </ProductionProvider>
  </StrictMode>,
);
