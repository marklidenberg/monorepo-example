#!/usr/bin/env bash
python $MONOREPO_PATH/tools/run_files_by_pattern.py "*build_and_test.sh" --root "$MONOREPO_PATH/source"
