#!/bin/bash

if [ "$1" == "staging" ]; then
    echo "BUILDING FROM STAGING DATABASE"
    ./_scripts/get_ynmp_staging.sh
else
    ./_scripts/get_ynmp.sh
fi

./_scripts/get_cv.sh
./_scripts/get_el.sh
./_scripts/get_em.sh
./_scripts/get_meet.sh

./_scripts/get_ynmp_numbers.sh

data_files=(
    _downloads/ynmp.popit.mysociety.org.export.json
    _data/mapit-WMC-generation-22.json
    _downloads/electionmentions.export.json
    _downloads/cv.export.json
    _downloads/meet.export.json
    _downloads/el.export.json
    _downloads/el_person.export.json
    _downloads/electionmentions.export.people.json
    _downloads/electionmentions.export.people.quotes.json
)

python ./_scripts/get_wikipedia_extracts.py "${data_files[@]}"

python _scripts/build_person_index.py "${data_files[@]}"
python _scripts/build_constituency_index.py "${data_files[@]}"

python _scripts/build_data_small.py

