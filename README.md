# Radarr CLI

A powerful CLI tool for managing your Radarr instance.

## Features
- **Library Management**: List, Get, Search, Add, Update, and Delete movies.
- **Activity Tracking**: Monitor active downloads (Queue) and view event history.
- **System Control**: Trigger Radarr commands (RSS Sync, Refresh) and manage indexers.
- **Configuration**: List root folders and quality profiles.
- **Output Formats**: Supports both human-readable tables and raw JSON output (`--json`).

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file:
   ```env
   RADARR_URL=https://your-radarr-url
   RADARR_API_KEY=your-api-key
   ```

## Usage
Refer to [SKILL.md](SKILL.md) for a full list of commands and examples.

## Example
```bash
# Search for a movie
python radarr_cli.py search "Inception"

# Add it by TMDB ID
python radarr_cli.py add 27205

# Check the queue
python radarr_cli.py queue
```
