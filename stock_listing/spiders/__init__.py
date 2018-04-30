# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from datetime import datetime as dt
import scrapy
from stock_listing.items import StockItem

def convert_volume(old_volume):
        # Convert sales volume from string like "6.32M" to int of 6320
        # Can convert thousands (K), millions (M) and billions (B)
        # Numbers are in x1000 (i.e 160.4=160.400)
    try:
        sep = old_volume.index(".")
        nr_after = len(old_volume)-sep-2
        app = old_volume[sep+1:(sep+nr_after+1)]
        if "K" in old_volume:
            app_0 = "".join("0" for x in range(0,3-nr_after))
            new_val = float(old_volume[0:sep] + app + app_0)
        elif "M" in old_volume:
            app_0 = "".join("0" for x in range(0,6-nr_after))
            new_val = float(old_volume[0:sep] + app + app_0)
        elif "B" in old_volume:
            app_0 = "".join("0" for x in range(0,9-nr_after))
            new_val = float(old_volume[0:sep] + app + app_0)
        else:
            new_val = float(old_volume)
    except:
        print("An error occured.")
        new_val = 0.0
    
    return new_val/1e3

class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['money.cnn.com']
    handle_httpstatus_all = True

    start_urls = [
        'http://www.money.cnn.com/data/markets/sandp/?page=1'
    ]

    def parse(self, response):
        ## Parse thru listings
        for company in response.css('table.wsod_dataTable.wsod_dataTableBig tbody tr'):
            item = StockItem()

            item['date'] = dt.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            item['acronym'] = company.css('td a::text').extract_first()
            item['name'] = company.css('td::text').extract()[0][1:]
            current_pe = company.css('td::text').extract()[1]
            try:
                item['pe_val'] = float(current_pe.replace(",",""))
            except:
                item['pe_val'] = 0.0
            current_volume = company.css('td::text').extract()[2]
            item['volume'] = convert_volume(current_volume)
            current_price = company.css('td span::text').extract()[0]
            try:
                item['price'] = float(current_price.replace(",",""))
            except:
                item['price'] = 0.0

            yield item

        current_page_nr = ''.join(x for x in response.url if x.isdigit())
        if int(current_page_nr) < 34:
            next_page_nr = int(current_page_nr)+1
            next_page = response.url
            next_page = next_page.replace(current_page_nr,str(next_page_nr))
            yield scrapy.Request(next_page, callback=self.parse)