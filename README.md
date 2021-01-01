# Browser Testing Through Layout Fuzzing

## Setup

### Dependencies

#### Python

[Poetry](https://python-poetry.org) is used for python package management.

* `poetry install` will install dependencies
* `poetry shell` will start a shell with the proper dependencies available

[Black](https://github.com/psf/black) is used for code formatting.

[flake8](https://flake8.pycqa.org/en/latest/) is used for code linting.

#### Javascript

[npm](https://www.npmjs.com/get-npm) is used for javascript dependencies and
for coordinating the javascript build

* `npm install` will install dependencies
* `npm run build` will build the javascript modules

## How to run

### Generate and compare an html file

#### First time steps:

1. `poetry install` - install python dependencies
2. `npm install` - install javascript dependencies
3. `npm run build` - build javascript files
4. `poetry shell` - start a shell to run the tester

#### Run the tester:

`./compare.py` or `python3 compare.py`

## Configuration

Configuration is done through environment variables.
The `.env` file is used for convenience instead of setting the variables in the shell.
A `.env.example` file is provided an easy base for creating the `.env` file.

| Environment Variable | Use | Default | Example |
|----------------------|-----|---------| ------- |
| `CHROME_DRIVER_PATH`    | Location of the chrome driver. | N/A | `/path/to/chromedriver` |
| `LAYOUT_FILE_DIR`    | Location to store generated layout files. | `cwd/layoutfiles` | `/path/to/layout/dir` |
| `RELATIVE_LAYOUT_PATH` | Path to test files from root of server. | `layoutfiles` | `relative/path` |
| `BUG_REPORT_FILE_DIR` | Location to store bug reports. | `cwd/bugreportfiles` | `/path/to/bug/reports` |
| `FAILURE_COUNT` | Stop testing after this many failures. | N/A | `10` |
| `TEST_COUNT` | Stop testing after this many total tests. | N/A | `1000` |

`TEST_COUNT` and `FAILURE_COUNT` are optional. If neither is specified the
script will run forever. Otherwise the first one reached will stop the script.

