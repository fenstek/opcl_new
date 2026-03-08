# Project State

## Environment

Server provider:
Hetzner

Host:
opcl

Stack:

OpenClaw  
Docker  
Matrix bridge  
Telegram bridge  
Agent infrastructure  

## Repository structure

Root files:

- `AGENTS.md`
- `START_SESSION.md`
- `NEXT_STEPS.md`
- `HANDOFF.md`
- `README.md`

Project memory:

- `memory/project_state.md`
- `memory/system_map.md`
- `memory/host_access.md`
- `memory/decisions.md`

Documentation:

- `docs/architecture.md`
- `docs/runbook.md`
- `docs/server-audit-template.md`
- `docs/opcl-checklist.md`

Local Codex config:

- `.codex/bootstrap.md`
- `.codex/config.toml`

Skills:

- `skills/project-bootstrap`
- `skills/safe-ops-change`
- `skills/handoff-writer`
- `skills/server-audit`

## OpenClaw host structure

Primary host:

- `opcl`

Important paths on host:

- config: `/opt/openclaw/state/openclaw.json`
- state: `/opt/openclaw/state/`
- workspace: `/opt/openclaw/workspace/`
- app repo: `/opt/openclaw/app/openclaw/`
- ops queue: `/opt/openclaw/state/ops-agent/queue/`
- ops results: `/opt/openclaw/state/ops-agent/results/`

Main container:

- `openclaw-openclaw-gateway-1`

## Related infrastructure

Secondary host:

- `oracle-e2`

Purpose of `oracle-e2`:

- hosts Matrix homeserver access for agent communication
- serves `matrix.utildesk.de` over HTTPS via Dockerized `nginx`
- runs `matrix-conduit` as the Matrix backend used by Element clients

Verified `oracle-e2` layout on 2026-03-08:

- compose root: `/home/ubuntu/conduit/`
- compose file: `/home/ubuntu/conduit/docker-compose.yml`
- Conduit config: `/home/ubuntu/conduit/conduit.toml`
- Nginx config: `/home/ubuntu/conduit/nginx.conf`
- Conduit data: `/home/ubuntu/conduit/data`
- TLS cert path mounted from: `/home/ubuntu/conduit/certbot/conf`

Running containers on `oracle-e2`:

- `conduit_nginx_1`
- `conduit_conduit_1`

## Current focus

Stabilizing OpenClaw agent environment.

## Known issues

- possible routing and auth problems observed during setup
- agent-to-agent Matrix behavior has been fragile and needs verification
- admin-tool availability for `ops-manager` depends on the `ops-agent` extension loading cleanly

## Agent structure

Default primary model:

- `openai-codex/gpt-5.3-codex`

Configured agents in OpenClaw runtime:

- `ops-manager`
  - name: `Ops Manager`
  - workspace: `/home/node/.openclaw/workspace/ops-manager`
  - routes: `telegram`, `matrix/codex_bot`
  - tools: minimal profile + `ops-agent`, `ops_agent_run`, `ops_agent_memory`, `ops_agent_admin`
- `agent-kolia`
  - name: `Kolia`
  - workspace: `/home/node/.openclaw/workspace/agent-kolia`
  - model: `openai-codex/gpt-5.1`
  - route: `matrix/claude_bot`
- `agent-sonnet`
  - name: `Sonnet`
  - workspace: `/home/node/.openclaw/workspace/agent-sonnet`
  - model: `anthropic/claude-sonnet-4-6`
  - route: `matrix/sonnet`
  - extra tool: `exec`
- `agent-petya`
  - name: `Петя`
  - workspace: `/home/node/.openclaw/workspace/agent-petya`
  - model: `anthropic/claude-haiku-4-5`
  - route: `matrix/petya`
  - extra tool: `exec`

## Verified on 2026-03-08

- `ops-manager` is intended to have `ops_agent_admin` access in runtime config.
- A broken `ops-agent` extension caused admin-tool access to fail at load time.
- Restoring the last working `ops-agent` extension and restarting gateway returned the plugin to loaded state.
- `oracle-e2` is not hosting a separate Element container in the observed Docker stack.
- Element Desktop traffic was observed in nginx logs against `matrix.utildesk.de`, which indicates Element is used as a client against the Matrix homeserver on `oracle-e2`.
