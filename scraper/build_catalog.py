import json
from multiprocessing.pool import ThreadPool

from osgeo import gdal

def link_generator(links_path):
    with open(links_path, 'r') as f:
        data = json.load(f)
        for item in data:
            event_name = list(item)[0]
            for link in item[event_name]:
                yield link

def gdalInfo(link):
    print(link)
    try:
        info = gdal.Info('/vsicurl/{}'.format(link), format='json', allMetadata=True)
        return info
    except:
        print("Caught an exception!")
        return None


def get_info(links_path):
    m = ThreadPool()
    response = m.map(gdalInfo, link_generator(links_path))
    return response
