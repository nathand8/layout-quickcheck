# Browser Layout Testing - QuickCheck


# Setup

### Install Python Requirements
```bash
pip install -r requirements.txt
```
(You can create a [python virtual environment](https://docs.python.org/3/tutorial/venv.html) if you want)

### Install Browser Drivers
Install the Chrome Webdriver ([here](https://chromedriver.chromium.org/getting-started)).

Optionally, you can install the Firefox Webdriver ([here](https://github.com/mozilla/geckodriver/releases)) and the Safari Webdriver ([here](https://webkit.org/blog/6900/webdriver-support-in-safari-10/))

Declare the driver paths through environment variables
```bash
export CHROME_DRIVER_PATH="/usr/local/bin/chromedriver"

export FIREFOX_DRIVER_PATH="/usr/local/bin/geckodriver"    # Optional
export SAFARI_DRIVER_PATH="/usr/bin/safaridriver"          # Optional
```


# Run

### Start Web Server
```bash
python3 src/threaded_web_server.py
```
If a different web server is preferred, run the web server on port 8000 from the root of the repo.

### Run the Bug Finder
```bash
python3 src/compare.py
```


# Output

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

# Configuration

### Run Options

```bash
usage: compare.py [-h] [-v] [-b BUG_LIMIT] [-t TEST_LIMIT]

find bugs in browser layout calculation - run forever unless specified otherwise

examples: 
    compare.py -b 1         # Find one bug and quit 
    compare.py -t 2000      # Run 2000 tests and quit

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity (repeatable argument -v, -vv, -vvv, -vvvv)
  -b BUG_LIMIT, --bug-limit BUG_LIMIT
                        quit after finding this many bugs
  -t TEST_LIMIT, --test-limit TEST_LIMIT
                        quit after running this many tests
```

### Environment Variables

Configuration is done through environment variables.

| Environment Variable | Use | Default | Example |
|----------------------|-----|---------| ------- |
| `CHROME_DRIVER_PATH`    | Location of the Chrome driver. | N/A | `/usr/local/bin/chromedriver` |
| `FIREFOX_DRIVER_PATH`    | Location of the Firefox driver. | N/A | `/usr/local/bin/geckodriver` |
| `SAFARI_DRIVER_PATH`    | Location of the Safari driver. | N/A | `/usr/bin/safaridriver` |
| `BUG_REPORT_FILE_DIR` | Location to store bug reports. | `cwd/bugreportfiles` | `/path/to/bug/reports` |
| `LAYOUT_FILE_DIR`    | Location to store generated layout files. | `cwd/layoutfiles` | `/path/to/layout/dir` |
| `RELATIVE_LAYOUT_URL` | Path to test files from root of server. | `layoutfiles` | `relative/path` |


# FAQ


#### Running on Safari
If you get this error
```
selenium.common.exceptions.SessionNotCreatedException: Message: Could not create a session: You must enable the 'Allow Remote Automation' option in Safari's Develop menu to control Safari via WebDriver.
```

Try running this command (it may require a password)
```bash
safaridriver --enable
```


# Legal

Licensed for use throught the [MIT License](MIT-LICENSE).