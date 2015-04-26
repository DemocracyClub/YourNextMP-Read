import sys, os.path
import requests
import json

url = "http://en.wikipedia.org/w/api.php?titles={}&format=json&action=query&prop=extracts&exintro=&explaintext="

ynmp_export_path = sys.argv[1]
ynmp_export = json.load(open(ynmp_export_path))

for person in ynmp_export['persons']:
    person_path = '_downloads/wikipedia/person_{}.json'.format(person['id'])
    if os.path.exists(person_path):
        continue

    for link in person['links']:
        if link['note'] == 'wikipedia':
            if link['url'].startswith('http://en.wikipedia.org/wiki/'):
                wiki_title = link['url'][len('http://en.wikipedia.org/wiki/'):]
            elif link['url'].startswith('https://en.wikipedia.org/wiki/'):
                wiki_title = link['url'][len('https://en.wikipedia.org/wiki/'):]
            else:
                wiki_title = None

            api_url = url.format(wiki_title)

            resp = requests.get(api_url).json()

            try:
                full = resp['query']['pages'][resp['query']['pages'].keys()[0]]
            except KeyError, e:
                print e
                continue
            
            if 'extract' in full:
                first_para = full['extract'].split('\n')[0]
            else:
                continue

            print link['url']
            print first_para 
            print

            obj = {'first_para': first_para,
                   'full': full}

            #person_dumped = json.load(open('_data/people/id/{}.json'.format(person['id']), 'r'))
            #person_dumped['biography'] = first_para
            
            json.dump(obj, open(person_path, 'w+'), indent=4, sort_keys=True)
