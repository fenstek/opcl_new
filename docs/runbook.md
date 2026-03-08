# Operations Runbook

This document records operational procedures for the OpenClaw environment on `opcl`.

## Safety Checklist

Before changing infrastructure:

1. inspect the current state
2. back up relevant configuration
3. apply the smallest possible change
4. verify service health
5. document the result

## Core Verification Commands

Use these during audits and after changes:

- `docker ps`
- `docker compose ps`
- `systemctl status <service>`
- `df -h`
- `free -m`

## Standard Change Flow

### 1. Audit

- confirm the target service and scope
- collect current status
- review recent logs

### 2. Backup

- save the relevant configuration before edits
- note current values and file locations

### 3. Change

- apply a minimal patch
- avoid unrelated cleanups in the same change

### 4. Verify

- confirm the service is running
- check logs for new errors
- validate the user-facing path if applicable

### 5. Document

- update memory and runbook notes
- record follow-up risks or manual steps

## Critical Areas

Treat these as high-risk and audit first:

- firewall
- SSH
- sudoers
- Docker networking
- critical systemd services

## Open Items

- agent permissions verification
- Matrix routing verification
- deployment stabilization tasks
- automation hardening
