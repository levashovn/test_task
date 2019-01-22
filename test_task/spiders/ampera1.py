import scrapy


class AmperaSpider(scrapy.Spider):
    #First spider with uncleaned data 
    name="ampera1"

    start_urls= [
        'https://www.ampereanalysis.com/'
    ]

    #Response
    def parse(self, response):
        for blog in response.xpath("//div[@class='col-sm-6 col-md-4 item infinite-item']"):
            yield {
                "date" : blog.xpath( "substring-after(//div[@class='col-sm-6 col-md-4 item infinite-item']//span[@class='pad-10'],'-')").extract_first(),
                "author" : blog.xpath( "./div/span/span/a/b/text()").extract_first(),
                "title" : blog.xpath( ".//div[@class='col-md-12']/h5//u/text()").extract_first(),
            }           
        
        #dealing with pagination, adding next page to a link 
        next_page = response.xpath("//a[@class='infinite-more-link']/@href").extract_first()

        if next_page is not None:
            next_page_link= response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)


            