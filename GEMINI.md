# Radarr CLI Skill

A CLI tool and Gemini Skill for managing a Radarr instance.

## Context
- **Radarr URL:** `https://radarr.local.shifamily.com`
- **API Key:** `0ee5aea4565a4a909ed839b4ebb6da77` (Stored in `.env` for the CLI)

## Architecture
- `radarr_cli.py`: The main Python CLI tool.
- `SKILL.md`: Skill definition for Gemini CLI/OpenClaw.
- `.env`: Environment variables for sensitive info.

## Roadmap
- [x] Use Radarr API V3 documentation.
- [x] Implement core movie management (List, Add, Delete, Update).
- [x] Implement activity and history tracking (Queue, History).
- [x] Implement system commands and indexer management.
- [x] Add JSON output support.
- [ ] Add more settings-related API endpoints.

