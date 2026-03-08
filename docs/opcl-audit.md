# opcl Audit

This document records the verified infrastructure role of host `opcl` as observed on 2026-03-08.

## Summary

`opcl` is the primary OpenClaw operations host.

Its observed role is:

- runs the OpenClaw gateway
- stores runtime state and agent workspaces
- hosts the safe ops executor service
- connects agent messaging to Telegram and Matrix
- runs a local `searxng` side service inside the OpenClaw Docker network

## Host Overview

- ssh target: `opcl`
- hostname: `ubuntu-opcl`
- operating system: Ubuntu 22.04.5 LTS
- kernel: `5.15.0-171-generic`
- provider: Hetzner
- virtualization: KVM

## Resource Snapshot

Observed during audit:

- disk usage: `/` at about 30 percent used
- memory: about 3815 MB total, about 732 MB used
- swap: disabled

## Running Services

Key running system services:

- `docker.service`
- `ssh.service`
- `fail2ban.service`
- `tailscaled.service`
- `openclaw-ops-agent.service`
- `containerd.service`

Running containers:

- `openclaw-openclaw-gateway-1` using `openclaw:local`
- `searxng` using `searxng/searxng:latest`

## Filesystem Layout

OpenClaw root:

- `/opt/openclaw/`

Important paths:

- app repo: `/opt/openclaw/app/openclaw/`
- runtime state: `/opt/openclaw/state/`
- main config: `/opt/openclaw/state/openclaw.json`
- workspaces: `/opt/openclaw/workspace/`
- backups: `/opt/openclaw/backups/`
- bridge files: `/opt/openclaw/bridge/`
- searxng config: `/opt/openclaw/searxng/`

Important state subpaths:

- `/opt/openclaw/state/agents`
- `/opt/openclaw/state/matrix-bridge`
- `/opt/openclaw/state/ops-agent`
- `/opt/openclaw/state/telegram`
- `/opt/openclaw/state/memory`
- `/opt/openclaw/state/workspace`

Agent workspaces:

- `/opt/openclaw/workspace/ops-manager`
- `/opt/openclaw/workspace/agent-kolia`
- `/opt/openclaw/workspace/agent-sonnet`
- `/opt/openclaw/workspace/agent-petya`

## Docker Topology

### OpenClaw gateway container

- container: `openclaw-openclaw-gateway-1`
- image: `openclaw:local`
- Docker network: `openclaw_default`
- host binds:
  - `/opt/openclaw/state -> /home/node/.openclaw`
  - `/opt/openclaw/workspace -> /home/node/.openclaw/workspace`
- published host ports:
  - `127.0.0.1:18789 -> 18789/tcp`
  - `127.0.0.1:18790 -> 18790/tcp`
- healthcheck present and healthy during audit

### searxng container

- container: `searxng`
- image: `searxng/searxng:latest`
- Docker network: `openclaw_default`
- host bind:
  - `/opt/openclaw/searxng -> /etc/searxng`
- internal port:
  - `8080/tcp`
- not published directly to the public host interface

## Network Shape

Observed host listeners:

- `22/tcp`
- `127.0.0.1:18789/tcp`
- `127.0.0.1:18790/tcp`
- Tailscale listeners

Practical meaning:

- OpenClaw gateway ports are bound to loopback only
- direct public exposure of gateway ports was not observed in `ss`
- SSH and Tailscale provide remote access paths

## Verified Runtime Structure

Observed from `openclaw.json`:

- default primary model: `openai-codex/gpt-5.3-codex`
- agent workspace root: `/home/node/.openclaw/workspace`
- configured agents:
  - `ops-manager`
  - `agent-kolia`
  - `agent-sonnet`
  - `agent-petya`

Observed routing:

- `ops-manager` -> Telegram + Matrix account `codex_bot`
- `agent-kolia` -> Matrix account `claude_bot`
- `agent-sonnet` -> Matrix account `sonnet`
- `agent-petya` -> Matrix account `petya`

Observed tool note:

- `ops-manager` is intended to use `ops-agent`, `ops_agent_run`, `ops_agent_memory`, and `ops_agent_admin`
- successful availability depends on the `ops-agent` extension loading correctly

## Messaging Notes

Observed from runtime config and logs:

- Matrix homeserver target is `https://matrix.utildesk.de`
- Telegram is enabled
- Matrix providers for `claude_bot`, `codex_bot`, `petya`, and `sonnet` start inside the gateway
- end-to-end encryption is active for Matrix sessions

## Audit Findings on 2026-03-08

- gateway container was healthy
- `ops-agent` plugin had previously failed because of a parse error in the local extension
- restoring the last working extension and restarting the gateway returned the plugin to loaded state
- gateway logs still show a doctor recommendation about migrating Matrix single-account top-level values into `channels.matrix.accounts.default`

## Notes

- This audit did not modify firewall, SSH, Docker networking, or critical systemd configuration.
- Secrets, tokens, and sensitive env values are intentionally omitted from this document.
