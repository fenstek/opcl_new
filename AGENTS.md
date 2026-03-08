# OpenClaw Operations Project

This repository manages operations and automation of the OpenClaw environment on host `opcl`.

## Environment

Primary host:
opcl

Infrastructure:
Docker
systemd
SSH

User environment:
Windows PowerShell
Codex App

## Project goals

Stabilize OpenClaw deployment  
Automate operations  
Build AI agent infrastructure  
Document operational procedures  

## Memory files

Before making changes always read:

memory/project_state.md  
NEXT_STEPS.md  
HANDOFF.md  

## Safety rules

Never change without audit first:

firewall  
ssh  
sudoers  
docker networking  
systemd critical services  

Workflow:

inspect state  
backup configs  
apply minimal patch  
verify services  
update docs
