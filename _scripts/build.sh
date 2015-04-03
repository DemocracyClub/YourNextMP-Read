#!/bin/sh


if [ ! -f _downloads/electionmentions.export.json ]; then
    ./_scripts/get_em.sh
fi

if [ ! -f _downloads/ynmp.popit.mysociety.org.export.json ]; then
    ./_scripts/get_ynmp.sh
fi

if [ ! -f _downloads/cv.export.json ]; then
    ./_scripts/get_cv.sh
fi

data_files=(
    _downloads/ynmp.popit.mysociety.org.export.json
    _data/mapit-WMC-generation-22.json
    _downloads/electionmentions.export.json
    _downloads/cv.export.json
)

python _scripts/build_person_index.py "${data_files[@]}"
python _scripts/build_constituency_index.py "${data_files[@]}"
