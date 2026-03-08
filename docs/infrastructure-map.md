# Infrastructure Map

This document provides a single high-level view of the current OpenClaw-related infrastructure.

It summarizes the roles of the two audited hosts:

- `opcl`
- `oracle-e2`

Use the host-specific audit docs for detail:

- `docs/opcl-audit.md`
- `docs/oracle-e2-audit.md`

## High-Level Topology

```text
User
  -> Telegram client
  -> OpenClaw on opcl
  -> Agents on opcl
  -> VPS tools / safe ops execution

User
  -> Element client
  -> matrix.utildesk.de on oracle-e2
  -> Matrix-Conduit on oracle-e2
  -> Matrix bridge inside OpenClaw on opcl
  -> Agents on opcl
```

## Host Roles

### opcl

Primary OpenClaw operations host.

Main responsibilities:

- runs the OpenClaw gateway
- stores runtime state
- stores managed agent workspaces
- runs the safe ops executor service
- handles Telegram and Matrix agent-side messaging
- runs local `searxng` service inside Docker network

Key technologies:

- Docker
- systemd
- SSH
- Tailscale

Key paths:

- `/opt/openclaw/app/openclaw/`
- `/opt/openclaw/state/`
- `/opt/openclaw/state/openclaw.json`
- `/opt/openclaw/workspace/`
- `/opt/openclaw/backups/`

Main containers:

- `openclaw-openclaw-gateway-1`
- `searxng`

### oracle-e2

Secondary Matrix infrastructure host.

Main responsibilities:

- serves `matrix.utildesk.de`
- terminates HTTPS for Matrix traffic
- runs `matrix-conduit`
- acts as Matrix backend for Element clients and Matrix-connected agents

Key technologies:

- Docker
- nginx
- matrix-conduit
- SSH

Key paths:

- `/home/ubuntu/conduit/docker-compose.yml`
- `/home/ubuntu/conduit/nginx.conf`
- `/home/ubuntu/conduit/conduit.toml`
- `/home/ubuntu/conduit/data`

Main containers:

- `conduit_nginx_1`
- `conduit_conduit_1`

## Messaging Flow

### Telegram path

1. User sends a message in Telegram.
2. OpenClaw gateway on `opcl` receives it.
3. Request is routed to the matching agent.
4. Agent uses allowed tools and runtime state on `opcl`.

### Matrix / Element path

1. User uses Element as a Matrix client.
2. Element connects to `https://matrix.utildesk.de`.
3. `oracle-e2` nginx terminates TLS.
4. nginx proxies Matrix API traffic to Conduit on port `6167`.
5. OpenClaw gateway on `opcl` connects to that Matrix homeserver as configured in `openclaw.json`.
6. Matrix accounts such as `codex_bot`, `claude_bot`, `sonnet`, and `petya` are handled inside the OpenClaw gateway.
7. Requests are routed from Matrix into the relevant agent workspace on `opcl`.

## Agent Map

Observed OpenClaw agents:

- `ops-manager`
  - channels: Telegram, Matrix `codex_bot`
  - role: primary ops/admin agent
- `agent-kolia`
  - channel: Matrix `claude_bot`
- `agent-sonnet`
  - channel: Matrix `sonnet`
- `agent-petya`
  - channel: Matrix `petya`

Default primary model:

- `openai-codex/gpt-5.3-codex`

## Important Dependencies

- `opcl` depends on `oracle-e2` for Matrix homeserver access at `matrix.utildesk.de`
- `oracle-e2` does not host the OpenClaw gateway
- `oracle-e2` currently appears to serve Matrix backend only, not a standalone Element deployment
- Element is observed as a client connecting into the Matrix API on `oracle-e2`

## Operational Notes

- OpenClaw gateway ports on `opcl` are loopback-bound in Docker inspection
- Matrix traffic is externally reachable through `oracle-e2`
- `ops-manager` admin functionality depends on the `ops-agent` extension loading correctly on `opcl`
- both hosts should be audited before significant messaging or routing changes

## Recommended Reading Order

1. `docs/infrastructure-map.md`
2. `docs/opcl-audit.md`
3. `docs/oracle-e2-audit.md`
4. `docs/runbook.md`
