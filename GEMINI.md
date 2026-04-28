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
- [x] Initialize project and `.env`
- [x] Implement `list-movies`
- [x] Implement `search-movie`
- [x] Implement `add-movie`
- [x] Create `SKILL.md`
- [x] Add verification tests
- [x] Implement client-side pagination for `list-movies`
