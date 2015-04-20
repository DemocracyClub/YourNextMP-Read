import json
import time

import requests


mapit_export_path = json.load(open("_data/mapit-WMC-generation-22.json"))

area_dict = {}

for area in mapit_export_path:
    req = requests.get("http://mapit.mysociety.org/area/{0}/geometry".format(
        area,
    ))
    req_json = req.json()
    if 'error' in req_json and req_json['error'] == "No polygons found":
        continue
    area_dict[area] = req_json
    time.sleep(2)

with open("_data/mapit-centres.json", 'w') as f:
    f.write(json.dumps(area_dict, indent=4))
