# SteelGuard AI

SteelGuard AI is a simulated industrial safety command center for workforce digital twins, predictive risk analytics, hazard monitoring, alerts, and tabletop emergency escalation.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm --filter @workspace/steelguard-ai run dev` — run the web command center
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `artifacts/steelguard-ai/src/App.tsx` — routed command center UI and operator workflows
- `artifacts/steelguard-ai/src/index.css` — dark industrial theme tokens and utility styles
- `artifacts/api-server/src/routes/steelguard.ts` — synthetic workforce, alert, plant, analytics, authority, and emergency APIs
- `lib/api-spec/openapi.yaml` — source-of-truth API contract

## Architecture decisions

- The app uses deterministic synthetic data for 100 workforce digital twins; no physical sensors, cameras, or industrial controls are connected.
- The emergency shutdown is a two-step, audited simulation state change only; it never controls equipment or contacts emergency services.
- Authority escalation is represented by an in-prototype hierarchy and notification ledger; real outbound channels are not configured.

## Product

The command center provides a dark industrial dashboard, worker and plant twins, risk analytics, alert acknowledgement, authority readiness, a two-step simulated shutdown flow with audit IDs, and configurable prototype settings.

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

- Re-run API codegen after changing `lib/api-spec/openapi.yaml`.
- The API stores prototype state in memory; restarting the API resets worker mutations, alert acknowledgements, and emergency state.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
