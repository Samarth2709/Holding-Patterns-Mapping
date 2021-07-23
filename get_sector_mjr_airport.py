import pandas as pd
import os
import json


def convert_coords_list(coords: str):
    return list(map(float, coords.split(', ')))


def format_major_airports(filename="Major_airports.xlsx", df=None):
    if not df:
        path = os.path.join(os.getcwd(), 'Major_airports', filename)
        df = pd.read_excel(path)
    print(df.dtypes)

    with open('abbreviation_to_full_state_name.json', 'r') as abv:
        abv_map = json.load(abv)

    mjr_airports = {}
    for row in df.index:
        mjr_airports[df.loc[row, 'Airport Name']] = {'Coordinates': convert_coords_list(df.loc[row, 'Coordinates']),
                                                       'State': abv_map[df.loc[row, 'State']]}
    return mjr_airports


def get_all_center_data():
    all_centers = {}
    path = os.path.join(os.getcwd(), 'Aviation_Centers', 'Unziped-json', 'LowCenter2006.json')
    with open(path, 'r') as json_raw:
        jsondata = json.load(json_raw)
    return jsondata


def convert_to_feature(geom_coll):
    to_be_features = []
    # set of dicts

    for i in range(len(geom_coll['geometries'])):
        type_geo = geom_coll['geometries'][i]['type']
        name_geo = str(geom_coll['geometries'][i]['name'])
        coords_geo = geom_coll['geometries'][i]['coordinates']

        # single figure/set of points (feature) to be appended to 'features'
        index_dict_for_feature = {
            'type': 'Feature',
            'id': name_geo,
            'properties':{},
            'geometry': {
                'type': type_geo,
                'coordinates': coords_geo
            }
        }
        to_be_features.append(index_dict_for_feature)

    feature_coll = {'type': 'FeatureCollection',
                    'features': to_be_features}
    return feature_coll

# data = get_all_center_data()
# print(convert_to_feature(data['SuperSector2006']))


def get_len_center_set(center_data):
    # gets amount of features in center data set (feature collection)
    return len(center_data['features'])


def get_list_names_center_set(center_data):
    names = []
    for feature in center_data['features']:
        names.append(feature['id'])
    return names


def get_all_formatted_center_data():
    data = get_all_center_data()
    prop = {'data': convert_to_feature(data), 'len': get_len_center_set(convert_to_feature(data)),
            'names': get_list_names_center_set(convert_to_feature(data))}

    return prop

# data = get_all_formatted_center_data()
# print(data.keys())
# {"type":"GeometryCollection",
#  "geometries":[
#         {"coordinates":[]
#          "type":"Polygon",
#          "name":"ZAB65"}
#       ]
# }

# {"type": "FeatureCollection",
#   "features": [
#     {"type": "Feature",
#      'id': 0,
#      "properties": {},
#
#      "geometry": {
#           "type": "Polygon",
#           "coordinates": [-112.0372, 46.608058]
#       }
#     }
#   ]
# }'