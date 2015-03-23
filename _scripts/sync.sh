#!/bin/sh

_scripts/get_ynmp.sh
python _scripts/build_person_index.py _downloads/ynmp.popit.mysociety.org.export.json
python _scripts/build_constituency_index.py _downloads/ynmp.popit.mysociety.org.export.json _data/mapit-WMC-generation-22.json

