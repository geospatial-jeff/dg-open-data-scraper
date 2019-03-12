# Digital Globe Open Data Scraper

Simple GDAL + Scrapy utility for pulling metadata from the Digital Globe Open Data program.  The goal is to generate an index for querying the Open Data program.  

## Usage

The library has a simple CLI which scrapes the Open Data program website to generate a list of available file paths.  The `gdal.Info` utility is used to read metadata about each file which is stored in a list, pickled, and written to the specified text file.
```
dg-open-data build --output data.txt
```

You can also trnslate the output text file to other data formats such as an Rtree:

```
dg-open-data translate data.txt --output rtree_index --format rtree
```

**Disclaimer:** There are a lot of images (~24,000) in the entire dataset so the above command can take a long time.  It took ~20 minutes to process the entire dataset with 100 threads on a t2.2xlarge EC2 instance.  