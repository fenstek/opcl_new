# Messaging Topology

This document records the current messaging topology for OpenClaw, including Telegram routing, Matrix routing, rooms, and known inter-agent limitations.

Use this document as the operational map for chat delivery and agent reachability.

Related docs:

- `docs/infrastructure-map.md`
- `docs/opcl-audit.md`
- `docs/oracle-e2-audit.md`
- `docs/architecture.md`

## Messaging Overview

OpenClaw messaging currently spans two layers:

- Telegram, handled directly by the OpenClaw gateway on `opcl`
- Matrix, where the public homeserver path is provided by `oracle-e2` and agent-side Matrix handling runs inside OpenClaw on `opcl`

## Telegram Topology

Observed runtime settings:

- Telegram is enabled
- policy: DM allowlist
- group policy: allowlist
- streaming mode: `partial`

Observed routing:

- Telegram traffic routes to `ops-manager`

Practical meaning:

- Telegram is currently the direct user-to-ops-manager path
- Telegram is not the observed main routing path for the other named agents

## Matrix Topology

Observed homeserver:

- `https://matrix.utildesk.de`

Infrastructure path:

1. Element client connects to `matrix.utildesk.de`
2. `oracle-e2` nginx terminates HTTPS
3. nginx proxies Matrix API traffic to Conduit on port `6167`
4. OpenClaw on `opcl` connects to this homeserver using configured Matrix accounts

## Matrix Account Map

Observed accounts in OpenClaw runtime:

- `codex_bot` -> `@codex_bot:matrix.utildesk.de`
- `claude_bot` -> `@claude_bot:matrix.utildesk.de`
- `sonnet` -> `@sonnet:matrix.utildesk.de`
- `petya` -> `@petya:matrix.utildesk.de`

Observed agent mapping:

- `ops-manager` -> Matrix account `codex_bot`
- `agent-kolia` -> Matrix account `claude_bot`
- `agent-sonnet` -> Matrix account `sonnet`
- `agent-petya` -> Matrix account `petya`

## Binding Rules

Observed route bindings:

- `ops-manager` -> `telegram`
- `ops-manager` -> `matrix/codex_bot`
- `agent-kolia` -> `matrix/claude_bot`
- `agent-sonnet` -> `matrix/sonnet`
- `agent-petya` -> `matrix/petya`

Practical meaning:

- routing is account-based on Matrix
- each agent is tied to its own Matrix account identity

## Matrix Rooms

Observed rooms from `ops-manager` workspace notes and runtime config:

- `trialog (main)` -> `!V-PNS_zYPuJIi17YdvBu3-Uc2XCQ8AfVUjbD8sBfHZ8`
- `DM with Sergey` -> `!8PRlNVN344GCCgU6zCJAXrk04QoA4ikM5BeC3dMDGuQ`
- `Boltalka` -> `!AxqiHetgEEbgtS8H0zxarctn0ZlK9Mx7V6y9ogv-4_U`

Observed room behavior:

- `trialog` is not encrypted
- `DM with Sergey` is encrypted
- `Boltalka` exists but was described in workspace notes as not in routing

## Per-Account Messaging Notes

### codex_bot / ops-manager

- group policy: `open`
- DM allowlist includes `@sergey:matrix.utildesk.de`
- `trialog` has `autoReply: true`
- `trialog` room config includes explicit user list for active participants
- `Boltalka` is also present with `autoReply: true`

### claude_bot / agent-kolia

- group policy: `open`
- DM allowlist includes `@sergey:matrix.utildesk.de`
- `trialog` has `autoReply: true`
- `Boltalka` is also present with `autoReply: true`

### sonnet / agent-sonnet

- group policy: `allowlist`
- `groupAllowFrom` includes `@sergey`, `@claude_bot`, `@codex_bot`, `@sonnet`, `@petya`
- `trialog` has `autoReply: true`
- DM allowlist includes only `@sergey:matrix.utildesk.de`

### petya / agent-petya

- group policy: `open`
- `groupAllowFrom` includes `@sergey`, `@codex_bot`, `@claude_bot`, `@sonnet`
- `autoJoinAllowlist` includes `@sergey`, `@claude_bot`, `@codex_bot`, `@sonnet`
- `trialog` has `autoReply: true`
- `Boltalka` also has `autoReply: true`
- DM allowlist includes `@sergey` and `@claude_bot`

## Known Issue: Agent-to-Agent Messaging

This is an important operational caveat.

Observed workspace note in `ops-manager/TOOLS.md`:

- agent-to-agent messaging has historically been unreliable
- messages from other bots may be dropped before routing if `groupAllowFrom` or related account policy is too restrictive

Current practical interpretation:

- routing must be checked per account, not assumed globally
- room membership alone is not enough
- `groupPolicy`, `groupAllowFrom`, room-level settings, and DM allowlists all matter
- changes should be verified end-to-end with real message flow after config updates

## Current Operational Guidance

- use Telegram when you need the most direct path to `ops-manager`
- use Matrix when collaborating with named agent accounts and room-based workflows
- for Matrix troubleshooting, check both `oracle-e2` and `opcl`
- after Matrix policy changes, verify:
  - account binding
  - room membership
  - `groupAllowFrom`
  - room `autoReply`
  - DM allowlist behavior

## Recommended Verification Checklist

1. Confirm the target agent-to-account binding.
2. Confirm the Matrix account is started inside OpenClaw.
3. Confirm the room is present in account config.
4. Confirm `groupPolicy` and `groupAllowFrom` permit the sender.
5. Confirm room `autoReply` or mention behavior matches expectations.
6. Send a real test message and verify routing in logs.

## Notes

- This document intentionally avoids storing tokens or secrets.
- Messaging behavior should be treated as runtime-sensitive and verified after changes.
