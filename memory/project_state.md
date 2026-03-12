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

Third-party imports:

- `third_party/oci-arm-host-capacity`

Local Codex config:

- `.codex/bootstrap.md`
- `.codex/config.toml`

Skills:

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
  - intended capability: web research through local `searxng`
  - intended skills: `web-search-research`, `seo-analyst`
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
  - intended skills: `webmaster`, `web-designer`, `web-programmer`, `seo-analyst`, `google-search-console`

## Verified on 2026-03-08

- `ops-manager` is intended to have `ops_agent_admin` access in runtime config.
- A broken `ops-agent` extension caused admin-tool access to fail at load time.
- Restoring the last working `ops-agent` extension and restarting gateway returned the plugin to loaded state.
- `oracle-e2` is not hosting a separate Element container in the observed Docker stack.
- Element Desktop traffic was observed in nginx logs against `matrix.utildesk.de`, which indicates Element is used as a client against the Matrix homeserver on `oracle-e2`.

## Verified on 2026-03-09

- `openclaw-ops-agent.service` runs as user `openclaw-ops` with UID `998`.
- `/opt/openclaw/state/openclaw.json` remained owned by `opcl:opcl`.
- The file ACL for `openclaw-ops` was corrected from an ineffective entry with `mask::---` to effective `rw-`.
- Directory traversal on `/opt/openclaw/state` was already allowed for `openclaw-ops`, so no owner change or broad chmod was needed.
- Access was verified from UID `998` by opening `openclaw.json` for read/write and creating plus renaming a temporary file inside the state directory.
- `channels.matrix.accounts.petya.groupAllowFrom` was added for `@sergey`, `@codex_bot`, `@claude_bot`, and `@sonnet`.
- The `petya` Matrix account still has the `trialog` room `!V-PNS_zYPuJIi17YdvBu3-Uc2XCQ8AfVUjbD8sBfHZ8` with `autoReply: true`.
- Gateway logs showed a config hot reload for `channels.matrix.accounts.petya.groupAllowFrom`, and the container returned to healthy state after restart.
- Repository skill set was extended with `web-search-research` and `seo-analyst` for planned use by `agent-kolia`.
- A shared managed skill `google-search-console` was prepared for agent use through the OpenClaw managed skills directory.
- A Google Search Console service account credential was stored outside the repository under the host credentials path and verified against `sc-domain:tools.utildesk.de` and `sc-domain:fensteco.de`.
- Repository skill set was extended with `webmaster`, `web-designer`, and `web-programmer` for planned use by `agent-petya`.
