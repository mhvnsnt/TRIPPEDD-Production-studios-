# Rocket + TRIPPEDD integration

Rocket expects a Next.js + TypeScript application. TRIPPEDD is intentionally still a React application and its existing production runtime remains Vite/React.

This repository therefore exposes **two integration surfaces over the same React UI**:

- **Vite/React:** the existing `dev`, `build`, and `start` production path. Do not remove it.
- **Next.js/TypeScript:** `app/` plus `next.config.ts`, with `next:dev`, `next:build`, and `next:start` scripts for Rocket and other Next-aware workers.

The Next App Router entry imports the existing `src/App.tsx` rather than copying the studio into a second implementation. The browser-first app is loaded with `ssr: false` because it reads `window` for its view selection. The same `ProductionProvider` and tool registry initialization are retained in the Next entry.

## Non-negotiable architecture

1. Do not migrate the studio away from React merely to satisfy a hosting/tooling detector.
2. Do not create a second production UI implementation.
3. Rocket's Next surface is an adapter around the existing React studio.
4. The production orchestration/toolchain remains the TRIPPEDD application and CLI/tooling already in this repository.
5. The character authority and production asset gates remain independent of the web UI framework.

## Commands

```text
bun run dev          # existing Vite/React studio
bun run build        # existing Vite/React production build
bun run next:dev     # Rocket-compatible Next development surface
bun run next:build   # Rocket-compatible Next production build
bun run next:start   # serve the Next surface on port 3001
```

The two web surfaces must continue to consume the same `src/App.tsx`; they are not competing applications.
