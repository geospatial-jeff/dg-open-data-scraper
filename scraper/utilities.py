import pickle

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
                    'link': asset['description']
                }

                idx.insert(i,
                           bbox,
                           obj=payload)