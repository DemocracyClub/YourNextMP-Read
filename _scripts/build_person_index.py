import json
import sys, os.path
from collections import defaultdict
from datetime import date, datetime

ynmp_export_path = sys.argv[1]
mapit_export_path = sys.argv[2]
em_export_path = sys.argv[3]
cv_export_path = sys.argv[4]
meet_export_path = sys.argv[5]
el_export_path = sys.argv[6]
el_person_export_path = sys.argv[7]
em_people_export_path = sys.argv[8]
em_people_quotes_export_path = sys.argv[9]

with open(ynmp_export_path) as f:
    ynmp_export = json.load(f)

def list_to_dict(data_list, key):
    """
    Converts a list of dicts in to a dict keyed on `key`
    """
    ret = {}
    for item in data_list:
        if key in item:
            cleaned_key = item[key].replace(' ', '_').replace('.', '-')
            ret[cleaned_key] = item
    return ret

def years_ago(earlier_date, later_date):
    """
    Taken from https://github.com/mysociety/yournextmp-popit/

    Calculate the number of years between two dates
    >>> years_ago(date(1976, 9, 13), date(2015, 1, 31))
    38
    >>> years_ago(date(1976, 1, 6), date(2015, 1, 31))
    39
    >>> years_ago(date(1982, 1, 1), date(2016, 2, 29))
    34
    """
    try:
        later_date_in_earlier_year = date(
            earlier_date.year, later_date.month, later_date.day
        )
    except ValueError:
        # It must have been February the 29th:
        later_date_in_earlier_year = date(earlier_date.year, 3, 1)
    if later_date_in_earlier_year > earlier_date:
        return later_date.year - earlier_date.year
    else:
        return (later_date.year - earlier_date.year) - 1

def find_wiki_title(person):
   if 'wikipedia' in person['links']:
        link = person['links']['wikipedia']

        if link['url'].startswith('http://en.wikipedia.org/wiki/'):
            wiki_title = link['url'][len('http://en.wikipedia.org/wiki/'):]
        elif link['url'].startswith('https://en.wikipedia.org/wiki/'):
            wiki_title = link['url'][len('https://en.wikipedia.org/wiki/'):]
        else:
            wiki_title = None

        return wiki_title


def party_to_rosette(person):
    DEFAULT_ROSETTE = "rosette-independent.png"
    ROSETTE_MAPPING = {
        'party:103': "rosette-alliance.png",
        'party:53': "rosette-labour.png",
        'joint-party:53-119': "rosette-labour.png",
        'party:52': "rosette-conservative.png",
        'joint-party:51-83': "rosette-conservative.png",
        'party:70': "rosette-dup.png",
        'party:63': "rosette-green.png",
        'party:90': "rosette-libdem.png",
        'party:77': "rosette-plaid-cymru.png",
        'party:362': "rosette-respect.png",
        'party:55': "rosette-sdlp.png",
        'party:39': "rosette-sinn-fein.png",
        'party:102': "rosette-snp.png",
        'party:85': "rosette-ukip.png",
    }
    if 'ge2015' in person['candidacies']:
        if 'elected' in person['candidacies']['ge2015']['constituency']:
            if person['candidacies']['ge2015']['constituency']['elected']:
                party_id = person['candidacies']['ge2015']['party']['id']
                if party_id in ROSETTE_MAPPING.keys():
                    return ROSETTE_MAPPING[party_id]
                return DEFAULT_ROSETTE


party_dict = {}
for party in ynmp_export['organizations']:
    if party['classification'] == "Party":
        party_dict[party['id']] = party

# Build CV data
with open(cv_export_path) as f:
    cv_export = json.load(f)

person_cvs = {}
for cv in cv_export:
    cv['person_id'] = str(cv['person_id'])
    person_cvs[cv['person_id']] = cv

# Build EL data
with open(el_person_export_path) as f:
    person_leaflets = json.load(f)

# EM data
with open(em_people_export_path) as f:
    em_export = json.load(f)

with open(em_people_quotes_export_path) as f:
    em_quotes_export = json.load(f)

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

              party_id = person['party_memberships'][ge_year]['id']
              images = party_dict[party_id]['images']
              if images:
                  person['party_emblem'] = images[0]
              else:
                  person['party_emblem'] = None

    if 'images' in person and person['images']:
        person['image_data'] = person['images'][0]

    person['contact_details'] = list_to_dict(
        person['contact_details'], key='type')

    person['identifiers'] = list_to_dict(
        person['identifiers'], key='scheme')

    person['links'] = list_to_dict(
        person['links'], key='note')

    # Calculate age in advance.  Will obviously get out of date!
    if 'birth_date' in person and person['birth_date']:
        if len(person['birth_date']) > 4:
            try:
                dob = datetime.strptime(person['birth_date'], '%Y-%m-%d').date()
                person['age'] = str(years_ago(dob, date.today()))
            except ValueError:
                pass
        else:
            approx_age = date.today().year - int(person['birth_date'])
            person['age'] = "{0} or {1}".format(approx_age - 1, approx_age)

    if person['gender']:
        person['gender'] = person['gender'].lower()

    person['candidacies'] = candidacies
    del person['standing_in']
    del person['party_memberships']

    if person['id'] in person_cvs:
        person['cv'] = person_cvs[person['id']]

    if person['id'] in person_leaflets:
        person['leaflets'] = person_leaflets[person['id']]

    person['mentions'] = em_export.get(person['id'])
    person['quotes'] = em_quotes_export.get(person['id'])

    if person['quotes']:
        person['quotes'] = person['quotes'][:10]

    wiki_title = find_wiki_title(person)

    if wiki_title:
        wiki_path = '_downloads/wikipedia/{}.json'.format(wiki_title)
        if os.path.exists(wiki_path):
            with open(wiki_path) as f:
                wiki_person = json.load(f)
            person['biography'] = wiki_person['first_para']

    person_rosette = party_to_rosette(person)
    if person_rosette:
        person['winner_rosette'] = person_rosette

    #constituency_id = person['candidacies']['ge2015']['constituency']['post_id']

    with open('_data/people/id/{}.json'.format(person['id']), 'w+') as f:
        json.dump(person, f, indent=4, sort_keys=True)

#json.dump(people_constituency_2015, open('_data/people_constituency_2015_index.json', 'w+'), indent=4, sort_keys=True)

