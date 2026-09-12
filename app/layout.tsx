import type { Metadata } from 'next';
import '../src/index.css';

export const metadata: Metadata = {
  title: 'TRIPPEDD Production Studios',
  description: 'TRIPPEDD production studio control plane',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
