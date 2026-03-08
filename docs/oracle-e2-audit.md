# oracle-e2 Audit

This document records the verified infrastructure role of host `oracle-e2` as observed on 2026-03-08.

## Summary

`oracle-e2` is a separate infrastructure node from `opcl`.

Its observed role is:

- Matrix homeserver endpoint for agent and user chat traffic
- HTTPS reverse proxy for `matrix.utildesk.de`
- backend serving Matrix API requests used by Element clients

No separate Element server/container was found in the audited Docker stack.
Element was observed as a client connecting to the Matrix API on this host.

## Host Overview

- ssh target: `oracle-e2`
- hostname: `free-tier-e2`
- operating system: Ubuntu 22.04.5 LTS
- kernel: `6.8.0-1044-oracle`
- virtualization: KVM

## Resource Snapshot

Observed during audit:

- disk usage: `/` at about 12 percent used
- memory: about 956 MB total, about 390 MB used
- swap: disabled

## Running Services

Key running system services:

- `docker.service`
- `ssh.service`
- `fail2ban.service`
- `containerd.service`

Running messenger-related containers:

- `conduit_nginx_1` using `nginx:alpine`
- `conduit_conduit_1` using `matrixconduit/matrix-conduit:latest`

## Deployment Layout

Compose root:

- `/home/ubuntu/conduit/`

Key files:

- `/home/ubuntu/conduit/docker-compose.yml`
- `/home/ubuntu/conduit/nginx.conf`
- `/home/ubuntu/conduit/conduit.toml`

Data and cert paths:

- `/home/ubuntu/conduit/data`
- `/home/ubuntu/conduit/certbot/conf`
- `/home/ubuntu/conduit/certbot/www`

## Docker Topology

### nginx container

- publishes `80:80`
- publishes `443:443`
- mounts `nginx.conf` read-only
- mounts Let's Encrypt certs read-only
- mounts Certbot webroot read-only
- depends on `conduit`

### conduit container

- internal port: `6167`
- not published directly on the host
- mounted config: `/etc/conduit.toml` from host `conduit.toml`
- mounted data dir: `/var/lib/matrix-conduit` from host `./data`

## Network Shape

Observed host listeners:

- `22/tcp`
- `80/tcp`
- `443/tcp`

Observed request flow:

1. Element or bot client connects to `https://matrix.utildesk.de`
2. `nginx` terminates TLS on `oracle-e2`
3. `nginx` proxies requests to `conduit:6167`
4. Conduit serves Matrix API responses

## Verified Conduit Settings

Confirmed from `conduit.toml`:

- `server_name = "matrix.utildesk.de"`
- `address = "0.0.0.0"`
- `port = 6167`
- `database_path = "/var/lib/matrix-conduit"`
- `max_request_size = 20_000_000`
- `allow_registration = false`
- `allow_federation = true`
- `allow_check_for_updates = false`
- `trusted_servers = ["matrix.org"]`

## Verified nginx Settings

Confirmed from `nginx.conf`:

- HTTP on port `80` redirects to HTTPS
- TLS virtual host is configured for `matrix.utildesk.de`
- Matrix traffic is proxied to `http://conduit:6167`

## Element Observation

No standalone Element deployment was found in the audited Docker stack.

However, nginx access logs show live requests with user agent:

- `Element/1.12.11`

Observed request types include:

- `/_matrix/client/v3/sync`
- `/_matrix/client/v3/account/whoami`
- `/_matrix/client/v3/voip/turnServer`

Practical meaning:

- Element is being used as a client
- `oracle-e2` currently provides the Matrix backend that Element talks to

## Notes

- This audit did not modify the host.
- No secrets, tokens, or private certificate material are recorded here.
- If an Element web frontend exists, it is not part of the currently observed Docker deployment on `oracle-e2`.
