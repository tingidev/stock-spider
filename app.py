## v2.0
## Date 30-04-2018
## Tingi Dev

## Script to crawl stock listings and store in MongoDB

import logging
from datetime import date
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stock_listing.spiders import StockSpider
from emailer.daily_listing_emailer import email_last_scraped_listing
#from twisted.internet import reactor, defer
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.log import configure_logging

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # only run on weekdays
    day_today = date.strftime(date.today(), '%A').lower()
    if day_today != 'saturday' and date_today != 'sunday':
        crawler = CrawlerProcess(get_project_settings())

        crawler.crawl(StockSpider)
        crawler.start() # the script will block here until the crawling is finished

        email_last_scraped_listing()
        logger.info('Scrape complete and email sent.')
    else:
        logger.info('Script skipped weekend')
else:
    logger.info('Script did not run')