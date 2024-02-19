
import scrapy

# activate venv
# $ scrapy crawl Immoweb -O Immopages.json
class ImmowebSpider(scrapy.Spider):
    name = 'Immoweb'
    start_urls = ['https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page=1']
    times = 0
    def parse(self, response):
            # print(f'processing: {response.url}')
            for houses in response.css('div.card--result__body'):
                yield {
                    # 'property_type': houses.css('a.card__title-link::text').get().strip(),
                    # 'price': houses.css().attrib[''],
                    'link': houses.css('a.card__title-link').attrib['href'],
                }
            self.times += 1
            next_page = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={self.times}'
            if self.times < 3:
                yield response.follow(next_page, callback=self.parse)

        # yield scraped_info #scrapy uses yield instead of return
