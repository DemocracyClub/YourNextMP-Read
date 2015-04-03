import os
import shutil
import json


SAMPLE_CONSTITUENCIES = [
    "65913"
]

for constituency_id in SAMPLE_CONSTITUENCIES:
    
    constituency_filename = "constituencies/id/{0}.json".format(constituency_id)
    
    shutil.copyfile(
        "_data/{0}".format(constituency_filename),
        "_data_small/{0}".format(constituency_filename),
    )
    
    constituency_data = json.loads(
        open("_data_small/{0}".format(constituency_filename)).read()
    )
    
    for person_id in constituency_data['ynmp']:
        person_filename = "people/id/{0}.json".format(person_id)
    
        shutil.copyfile(
            "_data/{0}".format(person_filename),
            "_data_small/{0}".format(person_filename),
        )
        