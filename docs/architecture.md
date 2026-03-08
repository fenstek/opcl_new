# System Architecture

This document describes the high-level flow of the OpenClaw environment on `opcl`.

## Service Flow

```text
User
  -> Telegram / Matrix
  -> OpenClaw Gateway
  -> Agents
  -> Tools and VPS operations
```

## Main Components

- `OpenClaw Gateway`: entry point for user requests
- `Agents`: execute operational and automation tasks
- `Matrix bridge`: integrates Matrix messaging flow
- `Telegram bridge`: integrates Telegram messaging flow
- `Docker`: runs application services
- `systemd`: manages host-level services
- `SSH`: primary remote access path to `opcl`

## Infrastructure Notes

- primary host: `opcl`
- provider: Hetzner
- operator environment: Windows PowerShell, Codex App, Claude Desktop

## Operational Boundaries

Changes to the following areas require audit-first handling:

- firewall
- SSH
- sudoers
- Docker networking
- critical systemd services

## Кратко По-Русски

Поток работы выглядит так: пользователь пишет в Telegram или Matrix, запрос проходит через OpenClaw Gateway, затем попадает в агентов, которые вызывают инструменты и операции на VPS `opcl`.
