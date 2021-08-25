#!/bin/bash
set -e -x

PATH="$HOME/firefox:$PATH"
python3 -m pip install -e .

START=`date "+%m/%d/%Y %H:%M:%S"`
python3 src/lqc_selenium/runner.py -t 10000 -c ./config/preset-test-grid.config.json
CHROME_COUNT=$(find bug_reports -maxdepth 1 -type d -newermt "$START" | wc -l)

START=`date "+%m/%d/%Y %H:%M:%S"`
python3 src/lqc_selenium/runner.py -t 10000 -c ./config/nightly-firefox.json
FFX_COUNT=$(find bug_reports -maxdepth 1 -type d -newermt "$START" | wc -l)

if command -v nightly-results &>/dev/null; then
    nightly-results "$(google-chrome --version)" "$CHROME_COUNT"
    nightly-results "$(firefox --version)" "$FFX_COUNT"
fi
