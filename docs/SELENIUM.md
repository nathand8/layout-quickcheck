# Selenium Setup

### Install Python Requirements
```bash
pip3 install -r requirements.txt
pip3 install -e .
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
python3 src/lqc_selenium/runner.py
```

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

Example: Run with config file
```bash
python3 src/lqc_selenium/runner.py -c ./config/my-config.json
```

See more about configurations [here](docs/CONFIGURATION.md).

# Output

### Bug Reports

Bug reports are generated in `./bugreportfiles` by default.

Each bug report has the following files:
- `data.json`
    - Data about the bug
    - Variants - Other tests run on this bug (eg. other browsers or different window sizes)
    - HTML/Styles Used
    - Differences detected
- `minified_bug.html` 
    - Minimized HTML/CSS to showcase the bug
    - Extra debugging tools are in `debugging_tools.js`
    - Open this page in a web browser and run `checkForBug()` in the console
    - Open this page in a web browser and run `simpleRecreate()` to log the differences in the console
- `original_bug.html` 
    - Unminimized HTML/CSS 
    - Very large with extraneous styles
    - Open this page in a web browser and run `checkForBug()` in the console

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