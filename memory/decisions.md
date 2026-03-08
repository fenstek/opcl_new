# Architecture Decisions

This file records important project decisions.

## 2026-03-08

- Project memory should store both repository structure and live agent/runtime structure, not only high-level goals.
- `memory/project_state.md` and `memory/system_map.md` are the primary places for repository and runtime context.
- For `ops-manager`, admin access depends on the `ops-agent` extension loading successfully, not only on `openclaw.json` allowlists.
- `oracle-e2` should be treated as a separate infrastructure node for Matrix/Element connectivity, distinct from the main OpenClaw host `opcl`.
- The current observed Matrix stack on `oracle-e2` is `nginx` + `matrix-conduit`; no standalone Element server deployment was found in the audited Docker stack.
