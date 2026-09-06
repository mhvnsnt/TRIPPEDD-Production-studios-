import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { ProductionProvider } from './context.tsx';
import { initTools } from './core/tools/init.ts';

initTools();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ProductionProvider>
      <App />
    </ProductionProvider>
  </StrictMode>,
);
