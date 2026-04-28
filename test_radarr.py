import subprocess
import json

def run_cli(args):
    result = subprocess.run(['./venv/bin/python', 'radarr_cli.py'] + args, capture_output=True, text=True)
    return result

def test_status():
    print("Testing status...")
    result = run_cli(['status'])
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data['appName'] == 'Radarr'
    print("Status test passed.")

def test_search():
    print("Testing search...")
    result = run_cli(['search', 'Inception'])
    assert result.returncode == 0
    assert 'Inception' in result.stdout
    print("Search test passed.")

if __name__ == "__main__":
    try:
        test_status()
        test_search()
        print("All tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
