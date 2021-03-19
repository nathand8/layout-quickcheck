# Browser Layout Testing - QuickCheck
This is a tool that uses randomized testing to find under-invalidation bugs in web browsers.

## Chromium Bugs Reported
This is a growing list of the bugs that have been reported in Chromium:
- blink_grid_0001 - https://bugs.chromium.org/p/chromium/issues/detail?id=1189755 
- blink_grid_0002 - https://bugs.chromium.org/p/chromium/issues/detail?id=1189762
- blink_grid_0003 - https://bugs.chromium.org/p/chromium/issues/detail?id=1190220 - page crash
Hundreds more bugs have not been reported. As of writing, sifting through bugs and preparing bug reports is the most time-intensive part of this process.

# Setup

### Install Python Requirements
```bash
pip3 install -r requirements.txt
```
(You can create a [python virtual environment](https://docs.python.org/3/tutorial/venv.html) if you want)

### Install Browser Drivers
Install the [Chrome Webdriver](https://chromedriver.chromium.org/getting-started), [Firefox Webdriver](https://github.com/mozilla/geckodriver/releases), and [Safari Webdriver](https://webkit.org/blog/6900/webdriver-support-in-safari-10/) (ships by default with MacOS).

##### On MacOS
```bash
brew install chromedriver
brew install geckodriver
xattr -d com.apple.quarantine /usr/local/bin/chromedriver
xattr -d com.apple.quarantine /usr/local/bin/geckodriver
# Safari Driver ships by default at /usr/bin/safaridriver
```

### Declare Paths to Browser Drivers

```bash
export CHROME_DRIVER_PATH="/usr/local/bin/chromedriver"
export FIREFOX_DRIVER_PATH="/usr/local/bin/geckodriver"    # Optional
export SAFARI_DRIVER_PATH="/usr/bin/safaridriver"          # Optional
```


# Run

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
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        path to config file to use
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

Licensed for use through the [MIT License](MIT-LICENSE).
