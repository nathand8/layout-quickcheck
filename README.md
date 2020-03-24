# Browser Testing Through Layout Fuzzing

## How to run

### Generate and compare an html file

`./compare.py` or `python3 compare.py`

### Compare a specified file

`./compare.py path/to/file` or `python3 compare.py path/to/file`

## Options

| Environment Variable | Use | Default |
|----------------------|-----|---------|
| `SERVO_DIRECTORY`    | Location of the servo git repository. | `cwd/../servo` |
| `LAYOUT_FILE_DIR`    | Location to store generated layout files. | `cwd/layoutfiles` |

