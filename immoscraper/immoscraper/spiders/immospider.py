
import scrapy

# activate venv
class ImmowebSpider(scrapy.Spider):
    name = 'Immoweb_houses'
    start_urls = ['https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1']
    times = 0
    def parse(self, response):
            for houses in response.css('div.card--result__body'):
                page_link = houses.css('a.card__title-link').attrib['href']
                if 'real-estate-project' not in page_link:
                    yield {
                        'link': page_link,
                    }
            self.times += 1
            next_page = f'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={self.times}'
            if self.times < 2:
                yield response.follow(next_page, callback=self.parse)
            else:
                self.logger.info('\n*\n   ~~~Last page finished.~~~\n*\n')

class ImmowebSpider(scrapy.Spider):
    name = 'Immoweb_apartments'
    start_urls = ['https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=1']
    times = 0
    def parse(self, response):
            for houses in response.css('div.card--result__body'):
                page_link = houses.css('a.card__title-link').attrib['href']
                if 'real-estate-project' not in page_link:
                    yield {
                        'link': page_link,
                    }
            self.times += 1
            next_page = f'https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={self.times}'
            if self.times < 2:
                yield response.follow(next_page, callback=self.parse)
            else:
                self.logger.info('\n*\n   ~~~Last page finished.~~~\n*\n')

# When inside crawler folder $ scrapy crawl [name] -O Immo[name].json -> or .csv => creates an output file
                

from bs4 import BeautifulSoup
import scrapy

class ImmowebSpider(scrapy.Spider):
    name = 'Immoweb_apartments_upgraded'
    start_urls = ['https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=1']
    times = 0

    def parse(self, response):
        for houses in response.css('div.card--result__body'):
            page_link = houses.css('a.card__title-link::attr(href)').get()
            if 'real-estate-project' not in page_link:
                # Instead of yielding the link, follow it to scrape more details using another callback
                yield response.follow(page_link, callback=self.parse_apartment)
        self.times += 1
        next_page = f'https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={self.times}'
        if self.times < 2:  # Adjust this as needed for how many pages you want to scrape
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info('\n*\n   ~~~Last page finished.~~~\n*\n')

    def parse_apartment(self, response):
        # Use BeautifulSoup to parse the apartment details
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example of extracting the title with BeautifulSoup
        id = soup.find('id').get_text(strip=True) if soup.find('id') else 'No id found'
        price = ('[insert way to do that]')
        # Extract other details as needed
        # ...
        yield {
            'id': id,
            'price': price,
            # Include other extracted details here
        }