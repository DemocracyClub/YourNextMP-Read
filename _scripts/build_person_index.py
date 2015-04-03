import json
import sys
from datetime import date, datetime

ynmp_export_path = sys.argv[1]

ynmp_export = json.load(open(ynmp_export_path))

def list_to_dict(data_list, key):
    """
    Converts a list of dicts in to a dict keyed on `key`
    """
    ret = {}
    for item in data_list:
        if key in item:
            cleaned_key = item[key].replace(' ', '_')
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
    
    person['contact_details'] = list_to_dict(
        person['contact_details'], key='type')

    person['links'] = list_to_dict(
        person['links'], key='note')
    
    # Calculate age in advance.  Will obvioulsy get out of date!
    if 'birth_date' in person and person['birth_date']:
        dob = datetime.strptime(person['birth_date'], '%Y-%m-%d').date()
        person['age'] = years_ago(dob, date.today())
    
    person['candidacies'] = candidacies
    del person['standing_in']
    del person['party_memberships']

    #if 'ge2015' in person['candidacies']:
    #    constituency_id = person['candidacies']['ge2015']['constituency']['post_id']
        
    json.dump(person, open('_data/people/id/{}.json'.format(person['id']), 'w+'), indent=4, sort_keys=True)

#json.dump(people_constituency_2015, open('_data/people_constituency_2015_index.json', 'w+'), indent=4, sort_keys=True)

