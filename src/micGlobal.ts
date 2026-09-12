import { Activity } from 'lucide-react';

// Temporary compatibility bridge for the evidence workspace's legacy Mic icon.
// Keep this isolated so the workspace can be migrated to an explicit import later.
(globalThis as typeof globalThis & { Mic: typeof Activity }).Mic = Activity;
