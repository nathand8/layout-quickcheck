#!/bin/bash
set -e -x

export CHROME_DRIVER_PATH=/home/p92/bin/chromedriver
export FIREFOX_DRIVER_PATH=/home/p92/bin/geckodriver

START=`date "+%m/%d/%Y %H:%M:%S"`
python3 src/compare.py -t 10000
DEFAULT_COUNT=$(find bugreportfiles/* -maxdepth 0 -type d -newermt "$START" | wc -l)

START=`date "+%m/%d/%Y %H:%M:%S"`
python3 src/compare.py -t 10000 -c ./config/test-grid.config.json
GRID_COUNT=$(find bugreportfiles/* -maxdepth 0 -type d -newermt "$START" | wc -l)

if command -v nightly-results &>/dev/null; then
    nightly-results Default "$DEFAULT_COUNT"
    nightly-results Grid "$GRID_COUNT"
fi
