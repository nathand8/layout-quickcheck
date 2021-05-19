from flask import Flask, request
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
    # Open the folder with all the bugs
    # Get one bug report per folder
    # Send back data.json
    reports = []
    for dir in os.listdir(BUG_REPORT_DIR):
        json_filepath = os.path.join(BUG_REPORT_DIR, dir, JSON_FILENAME) 
        with open(json_filepath, 'r') as f:
            bug = json.loads(f.read())
            server = request.base_url.split("/api")[0]
            bug['demo_urls'] = {
                "dirty": f"{server}/api/bug_file/{dir}/{DEMO_FILENAME}?state=dirty",
                "reloaded": f"{server}/api/bug_file/{dir}/{DEMO_FILENAME}?state=reloaded",
            }
            reports.append(bug)
        if len(reports) >= 100: # Quit Early (for testing only)
            return json.dumps(reports)
    return json.dumps(reports)

if __name__ == '__main__':
    app.run()
