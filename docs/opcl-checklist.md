# opcl Checklist

Use this checklist for the first-pass operational review of host `opcl`.

## Access

- confirm `ssh opcl` works
- confirm the current operator context and time on host

## Host Health

- check disk usage with `df -h`
- check memory with `free -m`
- check uptime and load

## Containers

- run `docker ps`
- run `docker compose ps` in the relevant stack directory
- note unhealthy or restarting containers

## systemd

- inspect relevant units with `systemctl status`
- note failed units
- review recent critical journal entries

## Messaging Path

- verify Telegram bridge status
- verify Matrix bridge status
- note auth, routing, or delivery errors

## Agent Layer

- confirm agent processes or containers are running
- verify expected tools and permissions
- record denied actions or missing environment values

## Change Safety

- identify whether firewall, SSH, sudoers, Docker networking, or critical systemd services are involved
- if yes, perform audit and backup before any patch

## Session Closeout

- update `HANDOFF.md` if priorities changed
- update `NEXT_STEPS.md` if the order of work changed
- record verification notes in docs or memory files
