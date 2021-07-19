import json
import os

geometry_jsonfile = ''
path = os.path.join(os.getcwd(), 'Aviation_Centers', 'Unziped-json', geometry_jsonfile)
with open(path, 'r') as raw_geometry_json:
    geometry_json_data = json.load(raw_geometry_json)

feature_coll = {"type": "FeatureCollection",
                "features": []}
base_feature = {"type": "Feature",
                'properties':{}}

def get_data_geometry(geometry_data):
    pass
# {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "id": 1
#       "properties": {
#         "population": 200
#       },
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-112.0372, 46.608058]
#       }
#     }
#   ]
# }
