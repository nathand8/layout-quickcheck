#!/bin/bash
set -e -x

START=`date "+%m/%d/%Y %H:%M:%S"`
python3 src/compare.py -t 10000
DEFAULT_COUNT=$(find bug_reports/* -maxdepth 0 -type d -newermt "$START" | wc -l)

START=`date "+%m/%d/%Y %H:%M:%S"`
python3 src/compare.py -t 10000 -c ./config/preset-test-grid.config.json
GRID_COUNT=$(find bug_reports/* -maxdepth 0 -type d -newermt "$START" | wc -l)

if command -v nightly-results &>/dev/null; then
    nightly-results Default "$DEFAULT_COUNT"
    nightly-results Grid "$GRID_COUNT"
fi
