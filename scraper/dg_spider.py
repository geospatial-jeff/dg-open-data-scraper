import scrapy

class DGOpenDataSpider(scrapy.Spider):
    name = 'dg-open-data'
    start_urls = [
        'https://www.digitalglobe.com/ecosystem/open-data',
    ]

    def parse(self, response):
        """
        Base scraper which scrapes each disaster link
        """
        divs = response.css('.subsection__body')
        for item in divs:
            disaster_link = item.xpath('./a/@href').getall()
            if len(disaster_link) > 0 and 'ecosystem' in disaster_link[0]:
                disaster_link = response.urljoin(disaster_link[0])
                yield scrapy.Request(disaster_link, callback=self.parse_disaster)


    def parse_disaster(self, response):
        links = []
        event_name = response.url.split('/')[-1]
        pre_event = response.xpath('//*[@id="table--pre-event"]//tbody//tr//td/a/@href').getall()
        post_event = response.xpath('//*[@id="table--post-event"]//tbody//tr//td/a/@href').getall()
        for link in pre_event:
            if link.endswith('.tif'):
                links.append(link)

        for link in post_event:
            if link.endswith('.tif'):
                links.append(link)

        yield {event_name: links}