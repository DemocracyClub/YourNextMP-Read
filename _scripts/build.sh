#!/bin/bash


if [ ! -f _downloads/electionmentions.export.json ]; then
    ./_scripts/get_em.sh
fi

if [ ! -f _downloads/ynmp.popit.mysociety.org.export.json ]; then
    ./_scripts/get_ynmp.sh
fi

if [ ! -f _downloads/cv.export.json ]; then
    ./_scripts/get_cv.sh
fi

if [ ! -f _downloads/meet.export.json ]; then
    ./_scripts/get_meet.sh
fi

if [ ! -f _downloads/el.export.json ]; then
    ./_scripts/get_el.sh
fi

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
