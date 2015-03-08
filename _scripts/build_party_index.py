import json
import sys

ynmp_export_path = sys.argv[1]

ynmp_export = json.load(open(ynmp_export_path))

party_id = {}

for org in ynmp_export['organizations']:
    if org['classification'] == 'Party':
        party_id[org['id']] = org

json.dump(party_id, open('_data/party_id_index.json', 'w+'), indent=4, sort_keys=True)

