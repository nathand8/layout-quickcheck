# Browser Layout Testing - QuickCheck

![LQC logo](logo.png)

This is a tool that uses randomized testing to find under-invalidation
bugs in web browsers. It's already found a lot of bugs in Chrome: 
[1137427](https://bugs.chromium.org/p/chromium/issues/detail?id=1137427),
[1166887](https://bugs.chromium.org/p/chromium/issues/detail?id=1166887),
[1189755](https://bugs.chromium.org/p/chromium/issues/detail?id=1189755) (fixed),
[1189762](https://bugs.chromium.org/p/chromium/issues/detail?id=1189762),
[1190220](https://bugs.chromium.org/p/chromium/issues/detail?id=1190220) (fixed),
[1219641](https://bugs.chromium.org/p/chromium/issues/detail?id=1219641),
[1224721](https://bugs.chromium.org/p/chromium/issues/detail?id=1224721),
and
[1229681](https://bugs.chromium.org/p/chromium/issues/detail?id=1229681).
As of writing, sifting through bugs and preparing bug reports is the
most time-intensive part of this process.

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

### Config

Configuration is done through a `config.json` file. Several preset examples are available in the `./config` folder.

```bash
python3 src/compare.py -c ./config/my-config.json
```


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
