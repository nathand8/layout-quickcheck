from flask import Flask
from flask_cors import CORS
import os
import json

BUG_REPORT_DIR = '../../bugreportfiles'
JSON_FILENAME = 'data.json'

app = Flask(__name__)
CORS(app) # This allows CORS from all domains on all routes for testing

@app.route('/bugs')
def allBugs():
    # Open the folder with all the bugs
    # Get one bug report per folder
    # Send back data.json
    json_filepaths = [os.path.join(BUG_REPORT_DIR, dir, JSON_FILENAME) for dir in os.listdir(BUG_REPORT_DIR)]

    reports = []
    for json_filepath in json_filepaths:
        with open(json_filepath, 'r') as f:
            reports.append(json.loads(f.read()))
        if len(reports) >= 10: # Quit Early (for testing only)
            return json.dumps(reports)
    return json.dumps(reports)

if __name__ == '__main__':
    app.run()
