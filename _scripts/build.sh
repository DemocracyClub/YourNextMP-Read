#!/bin/bash

./_scripts/get_cv.sh
./_scripts/get_el.sh
./_scripts/get_em.sh
./_scripts/get_meet.sh
./_scripts/get_ynmp.sh
./_scripts/get_ynmp_numbers.sh

data_files=(
    _downloads/ynmp.popit.mysociety.org.export.json
    _data/mapit-WMC-generation-22.json
    _downloads/electionmentions.export.json
    _downloads/cv.export.json
    _downloads/meet.export.json
    _downloads/el.export.json
)

python _scripts/build_person_index.py "${data_files[@]}"
python _scripts/build_constituency_index.py "${data_files[@]}"
