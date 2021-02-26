# Browser Layout Testing - QuickCheck


## Setup

### Setup Python VirtualEnv (Optional)
```bash
python3 -m venv .env
source .env/bin/activate
```

### Install Python Requirements
```bash
pip install -r requirements.txt
```

### Install Selenium

### Install Browser Drivers
After installing, specify the driver paths through environment variables
```bash
export CHROME_DRIVER_PATH="/usr/local/bin/chromedriver"
export FIREFOX_DRIVER_PATH="/usr/local/bin/geckodriver"
```


## Run

### Start Web Server
Run a web server on port 8000 that serves files from the root of the repo.

For convenience, a script is provided
```bash
python3 src/threaded_web_server.py
```

### Run the Bug Finder
```bash
python3 src/compare.py
```


## Output

### Bug Reports

Bug reports are generated in `./bugreportfiles` by default.

Each bug report has the following files:
- `data.json`
    - Data about the bug
    - Variants - Other tests run on this bug (eg. other browsers or different window sizes)
    - HTML/Styles Used
    - Differences detected
- `minimized_bug.html` 
    - Minimal web page showcasing the bug
    - Open this page in a web browser and run `simpleRecreate()` in the console
- `min_bug_with_debug.html` 
    - Minimized HTML/CSS to showcase the bug, but with extra debugging tools
    - Open this page in a web browser and run `recreateTheProblem()` in the console
- `original_bug.html` 
    - Unminimized HTML/CSS 
    - Very large with extraneous styles
    - Open this page in a web browser and run `recreateTheProblem()` in the console

## Configuration

Configuration is done through environment variables.

| Environment Variable | Use | Default | Example |
|----------------------|-----|---------| ------- |
| `CHROME_DRIVER_PATH`    | Location of the Chrome driver. | N/A | `/path/to/chromedriver` |
| `FIREFOX_DRIVER_PATH`    | Location of the Firefox driver. | N/A | `/path/to/geckodriver` |
| `LAYOUT_FILE_DIR`    | Location to store generated layout files. | `cwd/layoutfiles` | `/path/to/layout/dir` |
| `RELATIVE_LAYOUT_PATH` | Path to test files from root of server. | `layoutfiles` | `relative/path` |
| `BUG_REPORT_FILE_DIR` | Location to store bug reports. | `cwd/bugreportfiles` | `/path/to/bug/reports` |
| `FAILURE_COUNT` | Stop testing after this many failures. | N/A | `10` |
| `TEST_COUNT` | Stop testing after this many total tests. | N/A | `1000` |

`TEST_COUNT` and `FAILURE_COUNT` are optional
- If neither is specified the script will run forever
- If both are specified, the first one reached will stop the script
