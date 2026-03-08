# Next Steps

## Current Priorities

1. Stabilize the OpenClaw deployment.
2. Verify agent permissions and execution boundaries.
3. Verify Matrix routing and message flow.
4. Improve project and ops documentation.
5. Automate operations safely.

## Recommended Order

### 1. Agent Permissions

- confirm which agents are active
- verify available tools and expected permission boundaries
- record any auth or execution failures

### 2. Matrix Routing

- verify inbound and outbound message path
- check bridge logs for delivery or auth errors
- confirm the expected room or routing target

### 3. Deployment Stability

- inspect running containers and host services
- review recent failures and restart patterns
- check resource pressure on disk and memory

### 4. Documentation

- keep runbook procedures current
- update memory files after meaningful changes
- keep handoff notes ready for the next session

### 5. Safe Automation

- automate only repeated, low-risk checks first
- avoid direct changes to critical networking or access layers without audit
- document verification steps for every automation

## Session Output Expectations

For each completed work session, leave behind:

- updated docs or memory notes
- a short verification summary
- clearly stated follow-up actions
