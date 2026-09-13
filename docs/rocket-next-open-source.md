# Rocket / Next.js integration

This repository now exposes an additive Next.js + TypeScript application surface so Next-aware development tools such as Rocket can open the production studio without replacing the existing React/Vite application.

## Architecture

- **Canonical UI:** `src/App.tsx`
- **Existing runtime:** Vite + React (`dev`, `build`, `start`)
- **Rocket integration surface:** `app/page.tsx` -> `app/studio-client.tsx` -> the same `src/App.tsx`
- **Framework:** Next.js App Router
- **Language:** TypeScript
- **React:** existing React 19 dependency is retained

The Next surface is deliberately a wrapper, not a fork. Do not delete or migrate the Vite React runtime just to satisfy a Next-only editor.

## Open-source stack

The integration uses the open-source Next.js framework and the repository's existing open-source React/TypeScript/Vite stack. Existing production dependencies remain intact.

## Commands

```text
bun run dev         # existing React/Vite studio
bun run build       # existing production build
bun run next:dev    # Next/Rocket development surface
bun run next:build  # validates the Next application
bun run next:start  # serves the built Next application
```

CI runs both the existing Vite production build and `next:build`. This prevents the Rocket compatibility surface from becoming an unvalidated second implementation.

## Non-regression rules

1. Keep the existing React application and Vite scripts.
2. Keep `src/App.tsx` as the single canonical studio UI.
3. Do not create a second character/oral implementation in the Next app.
4. Next integration must wrap existing production code rather than fork it.
5. The Next surface must not weaken the MARS_CANONICAL or production evidence gates.
