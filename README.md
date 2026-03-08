# OpenClaw Operations

This repository manages the OpenClaw operational environment on host `opcl`.

## Purpose

- stabilize the OpenClaw deployment
- automate routine operations safely
- document infrastructure and procedures
- support agent-based operational workflows

## Environment

- host: `opcl`
- provider: Hetzner
- infrastructure: Docker, systemd, SSH
- operator environment: Windows PowerShell, Codex App

## Core Services

- OpenClaw Gateway
- Agents
- Matrix bridge
- Telegram bridge

## Project Workflow

Before making infrastructure changes:

1. inspect current state
2. back up configs
3. apply a minimal patch
4. verify services
5. update documentation

Do not change critical areas without audit first:

- firewall
- SSH
- sudoers
- Docker networking
- critical systemd services

## Repository Context

Start with these files:

- `AGENTS.md`
- `memory/project_state.md`
- `NEXT_STEPS.md`
- `HANDOFF.md`
- `START_SESSION.md`

Useful docs:

- `docs/architecture.md`
- `docs/runbook.md`
- `memory/system_map.md`
- `memory/host_access.md`

## Current Priorities

- stabilize the OpenClaw deployment
- verify agent permissions
- verify Matrix routing
- improve documentation
- automate operations safely
