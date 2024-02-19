
import scrapy

class ImmowebSpider(scrapy.spider):
    name = 'Immoweb'
    allowed_domains = ['https://www.immoweb.be/en']
    start_urls = ['https://www.immoweb.be/en/search/house-and-apartment/for-sale']

    def parse(self, response):
        print(f'processing: {response.url}')
        # Extracting the data (xpath)
        #property_type = url has : classified/-> apartment <-/for-sale
        price = response.xpath('//p[@class="classified__price"]').extract()
        immo_id = response.xpath('//p[@class="classified__price"]').extract()

        row_data = zip(immo_id, price)

        #Making the data row wise
        for item in row_data:
            scraped_info = {
                #key: value
                'page': response.url,
                'id': immo_id,
                'price': price
            }
        yield scraped_info