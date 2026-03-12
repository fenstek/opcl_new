# System Map

## Primary host

opcl

## Secondary host

oracle-e2

## Server provider

Hetzner

## Core services

- OpenClaw Gateway
- Agents
- Matrix bridge
- Telegram bridge
- Matrix homeserver proxy/backend on `oracle-e2`

## Infrastructure

- Docker
- systemd
- SSH

## User environment

- Windows PowerShell
- Codex App
- Claude Desktop

## Repository layout

Operational docs:

- `docs/`

Persistent project memory:

- `memory/`

Session and workflow entry points:

- `AGENTS.md`
- `START_SESSION.md`
- `NEXT_STEPS.md`
- `HANDOFF.md`

Local repository skills:

- `skills/project-bootstrap`
- `skills/safe-ops-change`
- `skills/handoff-writer`
- `skills/server-audit`
- `skills/web-search-research`
- `skills/seo-analyst`
- `skills/google-search-console`
- `skills/webmaster`
- `skills/web-designer`
- `skills/web-programmer`

## Host layout

OpenClaw config:

- `/opt/openclaw/state/openclaw.json`

OpenClaw state:

- `/opt/openclaw/state/`

OpenClaw app repo:

- `/opt/openclaw/app/openclaw/`

Workspace root:

- `/opt/openclaw/workspace/`

Agent workspaces:

- `/opt/openclaw/workspace/ops-manager`
- `/opt/openclaw/workspace/agent-kolia`
- `/opt/openclaw/workspace/agent-sonnet`
- `/opt/openclaw/workspace/agent-petya`

Ops-agent runtime paths:

- `/opt/openclaw/state/ops-agent/queue/`
- `/opt/openclaw/state/ops-agent/results/`
- `/opt/openclaw/state/credentials/gsc/`

## oracle-e2 layout

Server role:

- Matrix infrastructure endpoint for Element and agent chat traffic

Operating system:

- Ubuntu 22.04.5 LTS

Messenger-related stack:

- Docker
- `nginx:alpine`
- `matrixconduit/matrix-conduit:latest`

Relevant paths:

- `/home/ubuntu/conduit/docker-compose.yml`
- `/home/ubuntu/conduit/nginx.conf`
- `/home/ubuntu/conduit/conduit.toml`
- `/home/ubuntu/conduit/data`

Observed network shape:

- public listeners: `80/tcp`, `443/tcp`, `22/tcp`
- `nginx` terminates TLS for `matrix.utildesk.de`
- `nginx` proxies requests to `conduit:6167`
- Conduit itself is only exposed inside the Docker network

Observed Conduit settings:

- `server_name = matrix.utildesk.de`
- `address = 0.0.0.0`
- `port = 6167`
- `database_path = /var/lib/matrix-conduit`
- `allow_registration = false`
- `allow_federation = true`
- `allow_check_for_updates = false`
- `trusted_servers = [\"matrix.org\"]`

Observed Element note:

- no separate Element server/container was found on `oracle-e2`
- nginx access logs show active requests from `Element/1.12.11` client to Matrix API endpoints on `matrix.utildesk.de`
- practical meaning: Element is being used as a client against the Matrix homeserver on `oracle-e2`

## Agent routing map

- `ops-manager` -> Telegram + Matrix account `codex_bot`
- `agent-kolia` -> Matrix account `claude_bot`
- `agent-sonnet` -> Matrix account `sonnet`
- `agent-petya` -> Matrix account `petya`

Observed and planned capability note:

- `agent-kolia` is the planned web-research and SEO-analysis agent profile
- local `searxng` on `opcl` is the intended search backend for that role
- `agent-petya` is the planned webmaster, web-designer, and web-programmer profile with `exec` access on `gateway`

## Matrix identities

- `ops-manager` = `@codex_bot:matrix.utildesk.de`
- `agent-kolia` = `@claude_bot:matrix.utildesk.de`
- `agent-sonnet` = `@sonnet:matrix.utildesk.de`
- owner = `@sergey:matrix.utildesk.de`
