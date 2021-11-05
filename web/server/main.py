from flask import Flask, request, abort
from flask.helpers import send_from_directory
import os
import json
import argparse

BUG_REPORT_DIR = '../../bug_reports'
STATIC_FILES_DIR = '../ui/build'
JSON_FILENAME = 'data.json'
DEMO_FILENAME = 'minified_bug.html'
# MINIMIZED_FILENAME = 'minimized_bug.html'

app = Flask(__name__, static_folder=os.path.join(STATIC_FILES_DIR, "static"))

# Serve up index.html for any file that doesn't match other paths
# This allows for front-end routing
@app.route('/')
@app.route('/<path:p>')
def indexFile(p = "index.html"):
    if os.path.exists(os.path.join(STATIC_FILES_DIR, p)): 
        return send_from_directory(STATIC_FILES_DIR, p)
    else:
        return send_from_directory(STATIC_FILES_DIR, "index.html")

# Serve the bug files from the server
# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
@app.route('/api/bug_file/<path:path>')
def bugFile(path):
    return send_from_directory(BUG_REPORT_DIR, path)

# Download the bug files
@app.route('/api/download/bug_file/<path:path>')
def bugFileDownload(path):
    return send_from_directory(BUG_REPORT_DIR, path, as_attachment=True)

@app.route('/api/bugs')
def allBugs():
    """
    Open the folder with all the bugs
    Get one bug report per sub-folder
    Send back data.json
    """
    reports = []
    bug_dirs = os.listdir(BUG_REPORT_DIR)
    bug_dirs.sort(reverse=True) # Sort by date with most recent at the top
    for dir in bug_dirs:
        bug = bugJson(dir)
        if bug:
            reports.append(bug)
        if len(reports) >= 100: # Quit Early (for testing only)
            return json.dumps(reports)
    return json.dumps(reports)

@app.route('/api/bug/<path:path>')
def oneBug(path):
    """
    Get a single bug JSON
    """
    bug = bugJson(path)
    if bug:
        return json.dumps(bug)
    else:
        abort(404)

def bugJson(bug_dir):
    """
    Get the json from a bug report and prepare it for the UI
    """
    json_filepath = os.path.join(BUG_REPORT_DIR, bug_dir, JSON_FILENAME) 

    if not os.path.exists(json_filepath):
        return None

    with open(json_filepath, 'r') as f:
        bug = json.loads(f.read())
        server = request.base_url.split("/api")[0]

        # Add urls to demo pages
        bug['demo_urls'] = {
            "dirty": f"{server}/api/bug_file/{bug_dir}/{DEMO_FILENAME}?state=dirty",
            "reloaded": f"{server}/api/bug_file/{bug_dir}/{DEMO_FILENAME}?state=reloaded",
        }
        bug['download_urls'] = {
            "full": f"{server}/api/download/bug_file/{bug_dir}/{DEMO_FILENAME}",
            # "minimized": f"{server}/api/download/bug_file/{bug_dir}/{MINIMIZED_FILENAME}",
        }
        bug['id'] = bug_dir
        return bug

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Run the UI server")
    parser.add_argument("-p", "--port", help="Run the server on a different port", type=int, default=5000)
    parser.add_argument("--public", help="Run the server on a different port", action="store_true")
    args = parser.parse_args()

    app.run(port=args.port, host=("0.0.0.0" if args.public else "localhost"))
