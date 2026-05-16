import os
import sys
import json
import math
import argparse
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

def print_table(data, headers):
    if not data:
        print("No data available.")
        return

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in data:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    # Print header
    header_str = " | ".join(f"{h:<{widths[i]}}" for i, h in enumerate(headers))
    print(header_str)
    print("-" * len(header_str))

    # Print rows
    for row in data:
        print(" | ".join(f"{str(val):<{widths[i]}}" for i, val in enumerate(row)))

def list_movies(args):
    response = requests.get(f"{API_BASE}/movie", headers=get_headers())
    response.raise_for_status()
    movies = response.json()
    
    if getattr(args, 'json', False):
        print(json.dumps(movies, indent=2))
        return

    total_movies = len(movies)
    total_pages = math.ceil(total_movies / args.size)
    
    page = args.page
    if page < 1: page = 1
    if page > total_pages and total_pages > 0: page = total_pages

    start = (page - 1) * args.size
    end = start + args.size
    paginated_movies = movies[start:end]

    print(f"\n--- Page {page} of {total_pages} ({total_movies} total movies) ---\n")
    
    table_data = []
    for m in paginated_movies:
        table_data.append([
            m['id'],
            m['title'],
            m['year'],
            'Yes' if m['monitored'] else 'No',
            m.get('status', 'Unknown')
        ])
    
    print_table(table_data, ["ID", "Title", "Year", "Monitored", "Status"])
    
    if page < total_pages:
        print(f"\nTip: Use '--page {page + 1}' for the next page.")

def get_movie(args):
    response = requests.get(f"{API_BASE}/movie/{args.id}", headers=get_headers())
    if response.status_code == 404:
        print(f"Movie with ID {args.id} not found.")
        return
    response.raise_for_status()
    movie = response.json()
    print(json.dumps(movie, indent=2))

def search_movie(args):
    params = {"term": args.term}
    response = requests.get(f"{API_BASE}/movie/lookup", headers=get_headers(), params=params)
    response.raise_for_status()
    results = response.json()
    
    if getattr(args, 'json', False):
        print(json.dumps(results, indent=2))
        return

    table_data = []
    for m in results:
        table_data.append([
            m.get('tmdbId'),
            m.get('title'),
            m.get('year'),
            m.get('remotePoster', 'N/A')[:50] + "..." if m.get('remotePoster') else 'N/A'
        ])
    
    print_table(table_data, ["TMDB ID", "Title", "Year", "Poster URL"])

def list_root_folders(args):
    response = requests.get(f"{API_BASE}/rootfolder", headers=get_headers())
    response.raise_for_status()
    folders = response.json()
    
    if getattr(args, 'json', False):
        print(json.dumps(folders, indent=2))
        return

    table_data = []
    for f in folders:
        free_space_gb = f.get('freeSpace', 0) / (1024**3)
        total_space_gb = f.get('totalSpace', 0) / (1024**3)
        table_data.append([
            f['id'],
            f['path'],
            f"{free_space_gb:.2f}/{total_space_gb:.2f} GB"
        ])
    
    print_table(table_data, ["ID", "Path", "Free/Total"])

def list_quality_profiles(args):
    response = requests.get(f"{API_BASE}/qualityprofile", headers=get_headers())
    response.raise_for_status()
    profiles = response.json()
    
    if getattr(args, 'json', False):
        print(json.dumps(profiles, indent=2))
        return

    table_data = []
    for p in profiles:
        table_data.append([p['id'], p['name']])
    
    print_table(table_data, ["ID", "Name"])

def add_movie(args):
    # Lookup movie first to get all details
    lookup_response = requests.get(f"{API_BASE}/movie/lookup/tmdb", headers=get_headers(), params={"tmdbId": args.tmdb_id})
    if lookup_response.status_code == 404:
        print(f"Movie with TMDB ID {args.tmdb_id} not found.")
        return
    lookup_response.raise_for_status()
    movie_data = lookup_response.json()

    # Determine Root Folder
    if args.root_folder:
        movie_data['rootFolderPath'] = args.root_folder
    else:
        root_response = requests.get(f"{API_BASE}/rootfolder", headers=get_headers())
        folders = root_response.json()
        if not folders:
            print("Error: No root folders configured in Radarr.")
            return
        movie_data['rootFolderPath'] = folders[0]['path']
    
    # Determine Quality Profile
    if args.quality_profile:
        movie_data['qualityProfileId'] = args.quality_profile
    else:
        profile_response = requests.get(f"{API_BASE}/qualityprofile", headers=get_headers())
        profiles = profile_response.json()
        if not profiles:
            print("Error: No quality profiles configured in Radarr.")
            return
        movie_data['qualityProfileId'] = profiles[0]['id']

    movie_data['monitored'] = not args.unmonitored
    movie_data['addOptions'] = {"searchForMovie": args.search}

    response = requests.post(f"{API_BASE}/movie", headers=get_headers(), json=movie_data)
    if response.status_code == 201:
        if getattr(args, 'json', False):
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Successfully added movie: {movie_data['title']}")
    else:
        print(f"Failed to add movie: {response.status_code}")
        print(response.text)

def delete_movie(args):
    params = {
        "deleteFiles": args.delete_files,
        "addImportExclusion": args.exclude
    }
    response = requests.delete(f"{API_BASE}/movie/{args.id}", headers=get_headers(), params=params)
    if response.status_code == 200:
        if getattr(args, 'json', False):
            print(json.dumps({"status": "success", "message": f"Deleted movie {args.id}"}, indent=2))
        else:
            print(f"Successfully deleted movie with ID {args.id}")
    else:
        print(f"Failed to delete movie: {response.status_code}")
        print(response.text)

def update_movie(args):
    # Fetch current movie data first
    response = requests.get(f"{API_BASE}/movie/{args.id}", headers=get_headers())
    if response.status_code == 404:
        print(f"Movie with ID {args.id} not found.")
        return
    response.raise_for_status()
    movie_data = response.json()

    # Update fields if provided
    if args.monitored is not None:
        movie_data['monitored'] = args.monitored == "true"
    if args.quality_profile:
        movie_data['qualityProfileId'] = args.quality_profile

    response = requests.put(f"{API_BASE}/movie/{args.id}", headers=get_headers(), json=movie_data)
    if response.status_code == 202:
        if getattr(args, 'json', False):
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Successfully updated movie: {movie_data['title']}")
    else:
        print(f"Failed to update movie: {response.status_code}")
        print(response.text)

def system_status(args):
    response = requests.get(f"{API_BASE}/system/status", headers=get_headers())
    print(json.dumps(response.json(), indent=2))

def list_queue(args):
    params = {
        "page": args.page,
        "pageSize": args.size,
        "includeUnknownMovieItems": True
    }
    response = requests.get(f"{API_BASE}/queue", headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    
    if getattr(args, 'json', False):
        print(json.dumps(data, indent=2))
        return

    records = data.get('records', [])
    total_records = data.get('totalRecords', 0)
    
    print(f"\n--- Queue: {total_records} items ---\n")
    
    table_data = []
    for r in records:
        movie_title = r.get('movie', {}).get('title', 'Unknown')
        table_data.append([
            r['id'],
            movie_title,
            r['status'],
            f"{r['sizeleft'] / (1024**2):.2f}" if 'sizeleft' in r else 0, # MB
            r.get('timeleft', 'N/A')
        ])
    
    print_table(table_data, ["ID", "Movie", "Status", "Size Left (MB)", "Time Left"])

def list_history(args):
    params = {
        "page": args.page,
        "pageSize": args.size,
        "sortKey": "date",
        "sortDirection": "descending"
    }
    response = requests.get(f"{API_BASE}/history", headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    
    if getattr(args, 'json', False):
        print(json.dumps(data, indent=2))
        return

    records = data.get('records', [])
    total_records = data.get('totalRecords', 0)
    
    print(f"\n--- History: {total_records} records ---\n")
    
    table_data = []
    for r in records:
        movie_title = r.get('movie', {}).get('title', 'Unknown')
        table_data.append([
            r['id'],
            movie_title,
            r['eventType'],
            r['date']
        ])
    
    print_table(table_data, ["ID", "Movie", "Event", "Date"])

def trigger_command(args):
    payload = {"name": args.name}
    if args.params:
        payload.update(json.loads(args.params))
    
    response = requests.post(f"{API_BASE}/command", headers=get_headers(), json=payload)
    if response.status_code == 201:
        if getattr(args, 'json', False):
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Command '{args.name}' triggered successfully.")
            print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to trigger command: {response.status_code}")
        print(response.text)

def list_indexers(args):
    response = requests.get(f"{API_BASE}/indexer", headers=get_headers())
    response.raise_for_status()
    indexers = response.json()
    
    if getattr(args, 'json', False):
        print(json.dumps(indexers, indent=2))
        return

    table_data = []
    for i in indexers:
        table_data.append([
            i['id'],
            i['name'],
            i['implementation'],
            'Yes' if i['enable'] else 'No'
        ])
    
    print_table(table_data, ["ID", "Name", "Implementation", "Enabled"])

def test_indexer(args):
    # First get indexer details
    response = requests.get(f"{API_BASE}/indexer/{args.id}", headers=get_headers())
    if response.status_code == 404:
        print(f"Indexer with ID {args.id} not found.")
        return
    response.raise_for_status()
    indexer_data = response.json()

    # Test it
    test_response = requests.post(f"{API_BASE}/indexer/test", headers=get_headers(), json=indexer_data)
    if test_response.status_code == 200:
        if getattr(args, 'json', False):
            print(json.dumps({"status": "success", "indexer": indexer_data['name']}, indent=2))
        else:
            print(f"Indexer '{indexer_data['name']}' test successful.")
    else:
        print(f"Indexer '{indexer_data['name']}' test failed: {test_response.status_code}")
        print(test_response.text)

def main():
    # Common parser for global flags
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--json", action="store_true", help="Output as JSON")

    parser = argparse.ArgumentParser(description="Radarr CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List
    list_parser = subparsers.add_parser("list", parents=[common_parser], help="List movies in library")
    list_parser.add_argument("--page", type=int, default=1, help="Page number")
    list_parser.add_argument("--size", type=int, default=20, help="Page size")
    list_parser.set_defaults(func=list_movies)

    # Get
    get_parser = subparsers.add_parser("get", parents=[common_parser], help="Get details for a specific movie")
    get_parser.add_argument("id", type=int, help="Movie ID (Radarr ID)")
    get_parser.set_defaults(func=get_movie)

    # Search
    search_parser = subparsers.add_parser("search", parents=[common_parser], help="Search for movies to add")
    search_parser.add_argument("term", help="Search term")
    search_parser.set_defaults(func=search_movie)

    # Add
    add_parser = subparsers.add_parser("add", parents=[common_parser], help="Add a movie to library")
    add_parser.add_argument("tmdb_id", type=int, help="TMDB ID of the movie")
    add_parser.add_argument("--root-folder", help="Root folder path")
    add_parser.add_argument("--quality-profile", type=int, help="Quality profile ID")
    add_parser.add_argument("--unmonitored", action="store_true", help="Add as unmonitored")
    add_parser.add_argument("--search", action="store_true", help="Search for movie immediately")
    add_parser.set_defaults(func=add_movie)

    # Root Folders
    root_parser = subparsers.add_parser("root-folders", parents=[common_parser], help="List root folders")
    root_parser.set_defaults(func=list_root_folders)

    # Quality Profiles
    quality_parser = subparsers.add_parser("quality-profiles", parents=[common_parser], help="List quality profiles")
    quality_parser.set_defaults(func=list_quality_profiles)

    # Status
    status_parser = subparsers.add_parser("status", parents=[common_parser], help="Show system status")
    status_parser.set_defaults(func=system_status)

    # Delete
    delete_parser = subparsers.add_parser("delete", parents=[common_parser], help="Delete a movie from library")
    delete_parser.add_argument("id", type=int, help="Movie ID (Radarr ID)")
    delete_parser.add_argument("--delete-files", action="store_true", help="Also delete movie files")
    delete_parser.add_argument("--exclude", action="store_true", help="Add to import exclusions")
    delete_parser.set_defaults(func=delete_movie)

    # Update
    update_parser = subparsers.add_parser("update", parents=[common_parser], help="Update movie settings")
    update_parser.add_argument("id", type=int, help="Movie ID (Radarr ID)")
    update_parser.add_argument("--monitored", choices=["true", "false"], help="Set monitored status")
    update_parser.add_argument("--quality-profile", type=int, help="Set quality profile ID")
    update_parser.set_defaults(func=update_movie)

    # Queue
    queue_parser = subparsers.add_parser("queue", parents=[common_parser], help="List active downloads")
    queue_parser.add_argument("--page", type=int, default=1, help="Page number")
    queue_parser.add_argument("--size", type=int, default=20, help="Page size")
    queue_parser.set_defaults(func=list_queue)

    # History
    history_parser = subparsers.add_parser("history", parents=[common_parser], help="List history of events")
    history_parser.add_argument("--page", type=int, default=1, help="Page number")
    history_parser.add_argument("--size", type=int, default=20, help="Page size")
    history_parser.set_defaults(func=list_history)

    # Command
    command_parser = subparsers.add_parser("command", parents=[common_parser], help="Trigger a Radarr command")
    command_parser.add_argument("name", help="Command name (e.g., RssSync, RefreshMovie)")
    command_parser.add_argument("--params", help="JSON string of additional parameters")
    command_parser.set_defaults(func=trigger_command)

    # Indexers
    indexer_parser = subparsers.add_parser("indexer", parents=[common_parser], help="Manage indexers")
    indexer_subparsers = indexer_parser.add_subparsers(dest="indexer_command", help="Indexer command")
    
    idx_list_parser = indexer_subparsers.add_parser("list", parents=[common_parser], help="List indexers")
    idx_list_parser.set_defaults(func=list_indexers)
    
    idx_test_parser = indexer_subparsers.add_parser("test", parents=[common_parser], help="Test an indexer")
    idx_test_parser.add_argument("id", type=int, help="Indexer ID")
    idx_test_parser.set_defaults(func=test_indexer)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)

if __name__ == "__main__":
    main()
