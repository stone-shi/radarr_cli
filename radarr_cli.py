import os
import sys
import json
import math
import requests
from dotenv import load_dotenv

load_dotenv()

RADARR_URL = os.getenv("RADARR_URL")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")

if not RADARR_URL or not RADARR_API_KEY:
    print("Error: RADARR_URL and RADARR_API_KEY must be set in .env")
    sys.exit(1)

# Ensure URL doesn't have trailing slash
RADARR_URL = RADARR_URL.rstrip('/')
API_BASE = f"{RADARR_URL}/api/v3"

def get_headers():
    return {
        "X-Api-Key": RADARR_API_KEY,
        "Content-Type": "application/json"
    }

def list_movies(page=1, page_size=20):
    response = requests.get(f"{API_BASE}/movie", headers=get_headers())
    response.raise_for_status()
    movies = response.json()
    
    total_movies = len(movies)
    total_pages = math.ceil(total_movies / page_size)
    
    # Ensure page is within range
    if page < 1: page = 1
    if page > total_pages and total_pages > 0: page = total_pages

    start = (page - 1) * page_size
    end = start + page_size
    paginated_movies = movies[start:end]

    print(f"--- Page {page} of {total_pages} ({total_movies} total movies) ---")
    for movie in paginated_movies:
        print(f"[{movie['id']}] {movie['title']} ({movie['year']}) - {'Monitored' if movie['monitored'] else 'Unmonitored'}")
    
    if page < total_pages:
        print(f"\nTip: Use 'python radarr_cli.py list {page + 1} {page_size}' for the next page.")

def search_movie(term):
    params = {"term": term}
    response = requests.get(f"{API_BASE}/movie/lookup", headers=get_headers(), params=params)
    response.raise_for_status()
    results = response.json()
    for movie in results:
        print(f"{movie.get('title')} ({movie.get('year')}) - TMDB ID: {movie.get('tmdbId')}")

def get_root_folders():
    response = requests.get(f"{API_BASE}/rootfolder", headers=get_headers())
    response.raise_for_status()
    return response.json()

def get_quality_profiles():
    response = requests.get(f"{API_BASE}/qualityprofile", headers=get_headers())
    response.raise_for_status()
    return response.json()

def add_movie(tmdb_id, root_folder_path=None, quality_profile_id=None):
    # Lookup movie first to get all details
    lookup_response = requests.get(f"{API_BASE}/movie/lookup/tmdb", headers=get_headers(), params={"tmdbId": tmdb_id})
    lookup_response.raise_for_status()
    movie_data = lookup_response.json()

    if not root_folder_path:
        folders = get_root_folders()
        if not folders:
            print("Error: No root folders configured in Radarr.")
            return
        root_folder_path = folders[0]['path']
    
    if not quality_profile_id:
        profiles = get_quality_profiles()
        if not profiles:
            print("Error: No quality profiles configured in Radarr.")
            return
        quality_profile_id = profiles[0]['id']

    movie_data['rootFolderPath'] = root_folder_path
    movie_data['qualityProfileId'] = quality_profile_id
    movie_data['monitored'] = True
    movie_data['addOptions'] = {"searchForMovie": True}

    response = requests.post(f"{API_BASE}/movie", headers=get_headers(), json=movie_data)
    if response.status_code == 201:
        print(f"Successfully added movie: {movie_data['title']}")
    else:
        print(f"Failed to add movie: {response.status_code}")
        print(response.text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python radarr_cli.py [list|search|add|status]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        page = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        page_size = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        list_movies(page, page_size)
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: python radarr_cli.py search [term]")
            sys.exit(1)
        search_movie(sys.argv[2])
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: python radarr_cli.py add [tmdb_id]")
            sys.exit(1)
        add_movie(sys.argv[2])
    elif cmd == "status":
        response = requests.get(f"{API_BASE}/system/status", headers=get_headers())
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
