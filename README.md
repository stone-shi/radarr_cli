# Radarr CLI

A simple Python-based Command Line Interface (CLI) and Gemini Skill for managing movies in a Radarr instance.

## Features

- **List Movies:** View your current movie library with client-side pagination.
- **Search Movies:** Search for new movies using TMDB via Radarr.
- **Add Movies:** Add movies to your library by TMDB ID.
- **System Status:** Quickly check the health and status of your Radarr instance.

## Prerequisites

- Python 3.x
- A running Radarr instance
- Radarr API Key

## Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:stone-shi/radarr_cli.git
   cd radarr_cli
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your Radarr URL and API Key:
   ```env
   RADARR_URL=https://your-radarr-url.com
   RADARR_API_KEY=your_api_key_here
   ```

## Usage

### List Movies
Lists movies currently in your Radarr library. Supports pagination.
```bash
# List first 20 movies
python radarr_cli.py list

# List page 2 with 10 movies per page
python radarr_cli.py list 2 10
```

### Search Movies
Search for movies to add.
```bash
python radarr_cli.py search "The Matrix"
```

### Add Movies
Add a movie to Radarr using its TMDB ID (found via the search command).
```bash
python radarr_cli.py add 603
```

### System Status
Check the status of the Radarr system.
```bash
python radarr_cli.py status
```

## Gemini Skill Integration

This project is also configured as a **Gemini Skill**. You can use it within the Gemini CLI environment to manage your Radarr instance using natural language.

The skill definition is located in `SKILL.md`.

## License

MIT
