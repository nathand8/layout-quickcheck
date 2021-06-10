from flask import Flask, request, abort
from flask.helpers import send_from_directory
from flask_cors import CORS
import os
import json

BUG_REPORT_DIR = '../../bug_reports'
JSON_FILENAME = 'data.json'
DEMO_FILENAME = 'min_bug_with_debug.html'

app = Flask(__name__)
CORS(app) # This allows CORS from all domains on all routes for testing

# Serve the bug files from the server
# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
@app.route('/api/bug_file/<path:path>')
def bugFile(path):
    return send_from_directory(BUG_REPORT_DIR, path)

@app.route('/api/bugs')
def allBugs():
    """
    Open the folder with all the bugs
    Get one bug report per sub-folder
    Send back data.json
    """
    reports = []
    bug_dirs = os.listdir(BUG_REPORT_DIR)
    bug_dirs.sort(reverse=True) # Sort by date
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
        bug['id'] = bug_dir
        return bug

if __name__ == '__main__':
    app.run()
