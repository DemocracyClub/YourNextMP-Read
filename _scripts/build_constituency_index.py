import json
import sys
import time

ynmp_export_path = sys.argv[1]
mapit_export_path = sys.argv[2]
em_export_path = sys.argv[3]
cv_export_path = sys.argv[4]
meet_export_path = sys.argv[5]

mapit_export_path = json.load(open(mapit_export_path))

PERSON_CONSTITUENCIES = {}

# Build constituency data, starting with mapit
constituency_data = {constituency_id: {'mapit': mapit_data,
                                       'ynmp': [],}
                     for constituency_id, mapit_data in mapit_export_path.items()}

# Build YNMP data
ynmp_export = json.load(open(ynmp_export_path))

def build_person_candidacies(person):
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

    return candidacies

for person in ynmp_export['persons']:
    
    candidacies = build_person_candidacies(person)

    if 'ge2015' in candidacies:
        constituency_id = candidacies['ge2015']['constituency']['post_id']
        constituency_data[constituency_id]['ynmp'].append(person['id'])
        PERSON_CONSTITUENCIES[person['id']] = constituency_id

# Build EM data
election_mentions_export = json.load(open(em_export_path))

for constituency_id, links in election_mentions_export.items():
   constituency_data[constituency_id]['em'] = links 
 

# Build CV data
cv_export = json.load(open(cv_export_path))

for cv in cv_export:
    cv['person_id'] = str(cv['person_id'])
    constituency_id = PERSON_CONSTITUENCIES[str(cv['person_id'])]
    cv_list = constituency_data[constituency_id].get('cv', [])
    cv_list.append(cv)
    constituency_data[constituency_id]['cv'] = cv_list

# Build Meet data
meet_export = json.load(open(meet_export_path))

for event in meet_export['data']:
    if event['deleted']:
        continue
    if event['start']['timestamp'] < time.time():
        continue
    constituency_ids = event['mapitids']
    for constituency_id in constituency_ids:
        event_list = constituency_data[constituency_id].get('meet', [])
        event_list.append(event)
        constituency_data[constituency_id]['meet'] = event_list




for constituency_id, data in constituency_data.items(): 
    json.dump(data,
              open('_data/constituencies/id/{}.json'.format(constituency_id), 'w+'),
              indent=4,
              sort_keys=True)

#json.dump(people_constituency_2015, open('_data/people_constituency_2015_index.json', 'w+'), indent=4, sort_keys=True)

