"""
:Author: Manu Mathey-Prévot 
:Date: 13/02/2024
:Decription: Simple script to compile the distance between each node as the crow flies
by using the gps coordinates.
"""


import json

import geopy.distance


def main():
    with open("data/plans/Solbosch/general/solbosch_map.json", 'r') as f:
        data = json.load(f)

    latitudes = {}
    longitudes = {}
    for node in data['Solbosch']:
        latitudes[node['id']] = node['latitude']
        longitudes[node['id']] = node['longitude']

    for node in data['Solbosch']:
        for neighbor in node['neighbors']:
            neighbor['weight'] = round(geopy.distance.geodesic((latitudes[node['id']], longitudes[node['id']]),
                                                         (latitudes[neighbor['id']], longitudes[neighbor['id']])).m)

    # New json file with updated weights
    with open("data/exits_positions/solbosch_map_updated.json", 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()
