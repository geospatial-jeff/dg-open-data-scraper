import pickle
import json

from rtree import index


def index_to_rtree(index_file, index_location):
    idx = index.Index(index_location)

    with open(index_file, 'rb') as f:
        data = pickle.load(f)
        i = 0
        for asset in data:
            if asset:
                geometry = asset['wgs84Extent']['coordinates']
                xcoords = [x[0] for x in geometry[0]]
                ycoords = [y[1] for y in geometry[0]]
                bbox = [min(xcoords), min(ycoords), max(xcoords), max(ycoords)]

                payload = {
                    'eo:epsg': asset['coordinateSystem']['wkt'].rsplit('"EPSG","', 1)[-1].split('"')[0],
                    'bbox': bbox,
                    'geometry': geometry,
                    'link': asset['description'].replace('/vsicurl/','')
                }

                idx.insert(i,
                           bbox,
                           obj=payload)

def index_to_geojson(index_file, geojson_location):

    feature_collection = {
        "type": "FeatureCollection",
        "features": []
    }

    with open(index_file, 'rb') as f:
        data = pickle.load(f)
        i = 0
        for asset in data:
            if asset:
                geometry = asset['wgs84Extent']['coordinates']

                feature = {
                    'type': 'Feature',
                    'properties': {
                        'id': id,
                        'eo:epsg': asset['coordinateSystem']['wkt'].rsplit('"EPSG","', 1)[-1].split('"')[0],
                        'eo:gsd': (asset['geoTransform'][1] + abs(asset['geoTransform'][-1])) / 2,
                        'link': asset['description'].replace('/vsicurl/', ''),
                    },
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': geometry
                    }
                }

                feature_collection['features'].append(feature)

    with open(geojson_location, 'w') as out_geoj:
        json.dump(feature_collection, out_geoj)