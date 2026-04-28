# Radarr CLI Skill

A skill for managing movies in a Radarr instance.

## Description
This skill allows searching for movies, listing the current library, and adding new movies to Radarr.

## Usage
The skill interacts with a Radarr instance via its API.

### Commands

#### List Movies
Lists movies in the Radarr library with pagination.
```bash
# Default: page 1, size 20
python radarr_cli.py list

# Specific page and size
python radarr_cli.py list 2 10
```

#### Search Movie
Search for a movie by title.
```bash
python radarr_cli.py search "Inception"
```

#### Add Movie
Add a movie to Radarr by its TMDB ID.
```bash
python radarr_cli.py add 27205
```

#### System Status
Check the status of the Radarr instance.
```bash
python radarr_cli.py status
```

## Setup
1. Create a `.env` file with `RADARR_URL` and `RADARR_API_KEY`.
2. Install dependencies: `pip install requests python-dotenv`.
