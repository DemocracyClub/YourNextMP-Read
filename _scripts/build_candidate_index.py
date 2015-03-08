import json
import sys

ynmp_export_path = sys.argv[1]

ynmp_export = json.load(open(ynmp_export_path))

people_id = {}
people_constituency_2015 = {}

for person in ynmp_export['persons']:
    # Remove stuff we don't need
    del person['versions']

    candidacies = {}
    for ge_year in ['2010', '2015']:
        if person['standing_in'] and person['party_memberships'] and \
           ge_year in person['standing_in'] and \
           ge_year in person['party_memberships'] and\
           person['standing_in'][ge_year] and \
           person['party_memberships'][ge_year]:
            candidacy = {'party': person['party_memberships'][ge_year],
                         'constituency': person['standing_in'][ge_year],
                         'year': int(ge_year),}

            candidacies['ge{}'.format(ge_year)] = candidacy

    person['candidacies'] = candidacies
    del person['standing_in']
    del person['party_memberships']

    people_id[person['id']] = person

    if 'ge2015' in person['candidacies']:
        constituency_id = person['candidacies']['ge2015']['constituency']['post_id']
        if constituency_id not in people_constituency_2015:
            people_constituency_2015[constituency_id] = []
        
        people_constituency_2015[constituency_id].append(person['id'])

json.dump(people_id, open('_data/people_id_index.json', 'w+'), indent=4, sort_keys=True)
json.dump(people_constituency_2015, open('_data/people_constituency_2015_index.json', 'w+'), indent=4, sort_keys=True)

