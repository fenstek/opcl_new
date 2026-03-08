---

name: server-audit

description: Audit server state before making operational changes

---



When infrastructure tasks are requested:



Collect current state:



docker ps

docker compose ps

systemctl status

df -h

free -m



Check logs of relevant services.



Return summary:



running services

errors

resource usage

recent failures

