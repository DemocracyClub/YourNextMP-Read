#!/bin/sh

_scripts/get_ynmp.sh
python _scripts/build_person_index.py
python _scripts/build_constituency_index.py

