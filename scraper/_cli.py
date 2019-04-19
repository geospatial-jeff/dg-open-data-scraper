import click
import uuid
import os
import pickle
import shutil
import time

from scrapy.crawler import CrawlerProcess

from .dg_spider import DGOpenDataSpider
from .build_catalog import get_info
from .utilities import index_to_rtree, index_to_geojson

@click.group(short_help="Scrape spatial extents and metadata from Digital Globe Open Data Program (disaster data)")
def dg_open_data():
    pass

@dg_open_data.command(name="build")
@click.option('--output', '-o', type=click.File(mode='wb'))
def build(output):
    outdir = '/tmp/{}/'.format(uuid.uuid4())
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        # Crawl the DG open data portal
        outfile = os.path.join(outdir, 'links.json')

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': outfile
        })
        process.crawl(DGOpenDataSpider)
        # Blocked while crawling
        process.start()

        start = time.time()
        md = get_info(outfile)
        pickle.dump(md, output)
        end = time.time()

        print("Getting metadata took {} seconds".format(end-start))

    finally:
        shutil.rmtree(outdir)

@dg_open_data.command(name="translate")
@click.argument('index_file')
@click.option('--output', '-o', type=str)
@click.option('--format', '-f', type=str)
def translate(index_file, output, format):
    if format == 'rtree':
        index_to_rtree(index_file, output)
    elif format == 'geojson':
        index_to_geojson(index_file, output)

