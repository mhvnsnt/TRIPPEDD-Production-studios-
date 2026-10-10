'use client';

import dynamic from 'next/dynamic';
import { useEffect } from 'react';
import { ProductionProvider } from '../src/context';
import { initTools } from '../src/core/tools/init';

// The canonical studio UI remains src/App.tsx. Next is an integration surface,
// not a second implementation. Disable SSR for the legacy browser-first shell
// because it intentionally reads window during initial view selection.
const StudioApp = dynamic(() => import('../src/App'), { ssr: false });

export function StudioClient() {
  useEffect(() => {
    initTools();
  }, []);

  return (
    <ProductionProvider>
      <StudioApp />
    </ProductionProvider>
  );
}
