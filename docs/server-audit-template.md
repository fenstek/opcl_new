# Server Audit Template

Use this template before making infrastructure changes on `opcl`.

## Audit Scope

- target host:
- target service:
- reason for audit:
- requested by:
- date:

## Current State

### Running Services

- Docker containers:
- Compose services:
- Relevant systemd units:

### Resource Usage

- disk:
- memory:
- CPU or load:

### Logs and Errors

- recent errors:
- restart loops:
- auth issues:
- routing issues:

## Commands Run

- `docker ps`
- `docker compose ps`
- `systemctl status <service>`
- `df -h`
- `free -m`
- relevant log commands

## Findings

- healthy components:
- degraded components:
- suspected root causes:
- blockers or risks:

## Safe Change Plan

1. backup targets:
2. minimal change to apply:
3. verification steps:
4. rollback plan:

## Outcome

- change applied:
- verification result:
- follow-up actions:
