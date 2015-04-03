import json
import sys

ynmp_export_path = sys.argv[1]
mapit_export_path = sys.argv[2]
em_export_path = sys.argv[3]

mapit_export_path = json.load(open(mapit_export_path))

# Build constituency data, starting with mapit
constituency_data = {constituency_id: {'mapit': mapit_data,
                                       'ynmp': [],}
                     for constituency_id, mapit_data in mapit_export_path.items()}

# Build YNMP data
ynmp_export = json.load(open(ynmp_export_path))

for person in ynmp_export['persons']:
    # Remove stuff we don't need
    del person['versions']

    candidacies = {}
    for ge_year in ['2010', '2015']:
        if person['standing_in'] and person['party_memberships'] and \
                ge_year in person['standing_in'] and \
                ge_year in person['party_memberships'] and \
                person['standing_in'][ge_year] and \
                person['party_memberships'][ge_year]:
            candidacy = {'party': person['party_memberships'][ge_year],
                         'constituency': person['standing_in'][ge_year],
                         'year': int(ge_year),}

            candidacies['ge{}'.format(ge_year)] = candidacy

    person['candidacies'] = candidacies
    del person['standing_in']
    del person['party_memberships']

    if 'ge2015' in person['candidacies']:
        constituency_id = person['candidacies']['ge2015']['constituency']['post_id']
   
        constituency_data[constituency_id]['ynmp'].append(person)

# Build EM data
election_mentions_export = json.load(open(em_export_path))

for constituency_id, links in election_mentions_export.items():
   constituency_data[constituency_id]['em'] = links 
 
for constituency_id, data in constituency_data.items(): 
    json.dump(data,
              open('_data/constituencies/id/{}.json'.format(constituency_id), 'w+'),
              indent=4,
              sort_keys=True)

#json.dump(people_constituency_2015, open('_data/people_constituency_2015_index.json', 'w+'), indent=4, sort_keys=True)

