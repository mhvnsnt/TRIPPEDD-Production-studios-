import type { Metadata } from 'next';
import type { ReactNode } from 'react';
<<<<<<< HEAD
import './globals.css';
export const metadata: Metadata = { title: 'TRIPPEDD Production Studios', description: 'God Molecule production control plane' };
export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
=======
import '../src/index.css';

export const metadata: Metadata = {
  title: 'TRIPPEDD Production Studios',
  description: 'TRIPPEDD production studio control plane',
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
>>>>>>> origin/claude/trippedd-toolchain-provisioning-8pccfc
