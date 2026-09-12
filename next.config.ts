import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // The existing Vite studio remains the production/runtime path. This Next
  // entry is an additive integration surface for Rocket and other Next-aware
  // workers; it imports the same React UI instead of forking the application.
};

export default nextConfig;
