import click
import uuid
import os
import pickle
import shutil
import time

from scrapy.crawler import CrawlerProcess

from .dg_spider import DGOpenDataSpider
from .build_catalog import get_info

@click.group(short_help="Scrape spatial extents and metadata from Digital Globe Open Data Program (disaster data)")
def dg_open_data():
    pass

@dg_open_data.command(name="build")
@click.option('--output', '-o', type=click.File(mode='w'))
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
        with open(output, 'wb') as fp:
            pickle.dump(md, fp)
        end = time.time()

        print("Getting metadata took {} seconds".format(end-start))

    finally:
        shutil.rmtree(outdir)