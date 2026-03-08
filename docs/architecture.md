# System Architecture

This document describes the current high-level architecture of the OpenClaw environment.

The system currently spans two main hosts:

- `opcl`
- `oracle-e2`

For host-level details, see:

- `docs/infrastructure-map.md`
- `docs/opcl-audit.md`
- `docs/oracle-e2-audit.md`

## Architecture Overview

```text
Telegram user
  -> OpenClaw gateway on opcl
  -> Agent routing on opcl
  -> Tools / safe ops execution on opcl

Element user
  -> matrix.utildesk.de on oracle-e2
  -> nginx on oracle-e2
  -> Matrix-Conduit on oracle-e2
  -> Matrix bridge inside OpenClaw on opcl
  -> Agent routing on opcl
```

## Host Responsibilities

### opcl

`opcl` is the primary OpenClaw runtime and operations host.

Main responsibilities:

- runs the OpenClaw gateway
- stores runtime state and managed workspaces
- hosts agent runtime and routing logic
- connects to Telegram and Matrix as the active automation side
- runs the safe ops executor service
- runs `searxng` as a local service in the Docker network

Primary paths:

- `/opt/openclaw/app/openclaw/`
- `/opt/openclaw/state/`
- `/opt/openclaw/state/openclaw.json`
- `/opt/openclaw/workspace/`
- `/opt/openclaw/backups/`

### oracle-e2

`oracle-e2` is the Matrix-facing infrastructure host.

Main responsibilities:

- serves `matrix.utildesk.de`
- terminates HTTPS for Matrix traffic
- runs `matrix-conduit`
- provides the Matrix backend used by Element clients and OpenClaw Matrix accounts

Primary paths:

- `/home/ubuntu/conduit/docker-compose.yml`
- `/home/ubuntu/conduit/nginx.conf`
- `/home/ubuntu/conduit/conduit.toml`
- `/home/ubuntu/conduit/data`

## Main Components

### OpenClaw Gateway

Runs on `opcl` as container:

- `openclaw-openclaw-gateway-1`

Responsibilities:

- receives Telegram traffic
- connects to Matrix homeserver `https://matrix.utildesk.de`
- loads agent workspaces
- exposes internal gateway services
- routes requests to the correct agent

Observed bind shape:

- `127.0.0.1:18789`
- `127.0.0.1:18790`

### Agents

Observed agent set:

- `ops-manager`
- `agent-kolia`
- `agent-sonnet`
- `agent-petya`

Observed routing:

- `ops-manager` -> Telegram + Matrix `codex_bot`
- `agent-kolia` -> Matrix `claude_bot`
- `agent-sonnet` -> Matrix `sonnet`
- `agent-petya` -> Matrix `petya`

### Matrix Layer

Matrix responsibilities are split across two hosts:

- `oracle-e2` provides public Matrix endpoint and backend
- `opcl` runs Matrix-connected OpenClaw accounts inside the gateway

Observed Matrix homeserver:

- `https://matrix.utildesk.de`

Observed Matrix accounts in OpenClaw runtime:

- `@codex_bot:matrix.utildesk.de`
- `@claude_bot:matrix.utildesk.de`
- `@sonnet:matrix.utildesk.de`
- `@petya:matrix.utildesk.de`

### Telegram Layer

Telegram is handled directly by the OpenClaw gateway on `opcl`.

Observed role:

- Telegram is enabled in runtime config
- `ops-manager` is routed to Telegram

### Safe Ops Layer

Operational actions are anchored on `opcl`.

Observed components:

- `openclaw-ops-agent.service`
- `ops-agent` queue/results state under `/opt/openclaw/state/ops-agent/`
- `ops-manager` admin and ops tools through the `ops-agent` extension

## Communication Flows

### Telegram flow

1. User sends a message in Telegram.
2. OpenClaw gateway on `opcl` receives the request.
3. Gateway routes to the target agent.
4. Agent uses runtime state, tools, and safe ops execution on `opcl`.

### Matrix / Element flow

1. User opens Element as Matrix client.
2. Element connects to `matrix.utildesk.de`.
3. `oracle-e2` nginx handles HTTPS and proxies to Conduit.
4. Conduit serves Matrix API traffic.
5. OpenClaw gateway on `opcl` connects to that homeserver as configured in runtime.
6. Matrix events are routed into the corresponding OpenClaw agent.

## Important Dependencies

- `opcl` depends on `oracle-e2` for Matrix homeserver availability
- `oracle-e2` does not host the OpenClaw gateway
- Matrix user-facing access and OpenClaw Matrix bot connectivity meet at `matrix.utildesk.de`
- `ops-manager` admin capabilities depend on the `ops-agent` extension loading successfully

## Operational Boundaries

Treat these as audit-first areas:

- firewall
- SSH
- sudoers
- Docker networking
- critical systemd services

## Current Observations

- `opcl` is the execution and control plane
- `oracle-e2` is the Matrix ingress and backend plane
- Element is observed as a client, not as a standalone deployment on the audited servers
- the architecture is functional, but messaging/routing and agent-admin reliability still require careful verification
