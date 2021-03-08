#!/bin/bash
set -e -x

START=`date "+%m/%d/%Y %H:%M:%S"`
export CHROME_DRIVER_PATH=`which chomedriver`
export FIREFOX_DRIVER_PATH=`which geckodriver`
python3 src/compare.py -t 10000
COUNT=$(find bugreportfiles/* -maxdepth 0 -type d -newermt "$START" | wc -l)

if command -v nightly-results &>/dev/null; then
    nightly-results bugs "$COUNT"
fi
