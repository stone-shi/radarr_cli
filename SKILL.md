---
name: radarr
description: Manage Radarr (movies) via its API. List, search, add, and monitor movies.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    user-invocable: true
---

# Radarr CLI Skill

A skill for managing movies and system settings in a Radarr instance.

## Description
This skill allows searching for movies, managing the library, viewing active downloads, and triggering system commands in Radarr. It supports raw JSON output for all commands using the `--json` flag.

## Usage
The skill interacts with a Radarr instance via its API.

### Global Options
- `--json`: Output the result as a raw JSON string.

### Commands

#### Library Management
```bash
# List movies
python radarr_cli.py list [--page PAGE] [--size SIZE]

# Get movie details
python radarr_cli.py get <movie_id>

# Search for movies to add
python radarr_cli.py search "<term>"

# Add a movie
python radarr_cli.py add <tmdb_id> [--root-folder PATH] [--quality-profile ID] [--unmonitored] [--search]

# Update a movie
python radarr_cli.py update <movie_id> [--monitored true|false] [--quality-profile ID]

# Delete a movie
python radarr_cli.py delete <movie_id> [--delete-files] [--exclude]
```

#### Activity & History
```bash
# View active downloads
python radarr_cli.py queue [--page PAGE] [--size SIZE]

# View event history
python radarr_cli.py history [--page PAGE] [--size SIZE]
```

#### System & Configuration
```bash
# List root folders
python radarr_cli.py root-folders

# List quality profiles
python radarr_cli.py quality-profiles

# Check system status
python radarr_cli.py status

# Trigger a command
python radarr_cli.py command <name> [--params JSON_STRING]

# Manage indexers
python radarr_cli.py indexer list
python radarr_cli.py indexer test <id>
```

## Setup
1. Create a `.env` file with `RADARR_URL` and `RADARR_API_KEY`.
2. Install dependencies: `pip install requests python-dotenv`.
