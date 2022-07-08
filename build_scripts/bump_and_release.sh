#!/usr/bin/env bash

/bin/bash bump.sh $1 || exit 1
/bin/bash release.sh || exit 1
