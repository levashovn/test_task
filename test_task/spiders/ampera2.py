import scrapy
from scrapy.loader import ItemLoader
from test_task.items import BlogItem


class AmperaSpider(scrapy.Spider):
    #Second spider with cleaned data using ItemLoader
    name="ampera2"

    start_urls= [
        'https://www.ampereanalysis.com/'
    ]

    #Response
    def parse(self, response):
        for blog in response.xpath("//div[@class='col-sm-6 col-md-4 item infinite-item']"):
            loader = ItemLoader(item=BlogItem(), selector=blog, response=response)
            loader.add_xpath('date', "substring-after(//div[@class='col-sm-6 col-md-4 item infinite-item']//span[@class='pad-10'],'-')")
            loader.add_xpath('author', "./div/span/span/a/b")
            loader.add_xpath('title', ".//div[@class='col-md-12']/h5//u")
            yield loader.load_item()
               
        
        #dealing with pagination, adding next page to a link 
        next_page = response.xpath("//a[@class='infinite-more-link']/@href").extract_first()

        if next_page is not None:
            next_page_link= response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)


            