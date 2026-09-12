import type { NextConfig } from 'next';

// The existing Vite studio remains the production/runtime path. This Next entry
// is an additive integration surface for Rocket and other Next-aware workers; it
// imports the same React UI instead of forking the application.
//
// `output: 'export'` is what makes the cockpit deployable to GitHub Pages with
// no paid hosted runtime, and basePath keeps asset URLs correct under a project
// page. Both halves of the merge are kept: the comment states the intent, the
// config is what actually ships it.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  basePath,
  assetPrefix: basePath ? `${basePath}/` : undefined,
};

export default nextConfig;
