
import scrapy  # pip install scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, freeze_support  # used to crawl multiple spiders + handle freeze error
from bs4 import BeautifulSoup  # pip install bs4
import time
import pandas as pd  # pip install scrapy
import json

# from ./path/to/spidermodule import SpiderClass, SpiderClass  # -> Import the spider classes


# activate venv




class HouseSpider(scrapy.Spider):
    name = 'Immoweb_houses'
    start_urls = ['https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1']
    times = 0
    looptime = 200
    
    def parse(self, response):
        for houses in response.css('div.card--result__body'):
            page_link = houses.css('a.card__title-link::attr(href)').get()
            if 'real-estate-project' not in page_link:
                yield response.follow(page_link, callback=self.parse_link)
        self.times += 1
        next_page = f'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={self.times}'
        if self.times < self.looptime:  # Adjust this as needed for how many pages you want to scrape
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info('\n*\n   ~~~Last page finished.~~~\n*\n')

    def parse_link(self, response):
        # Inserting Bear's code:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)  # Find the script tag containing "window.classified = "
        script_content = script_tag.string  # Get the content of the script tag
        start_index = script_content.find("window.classified = ") + len("window.classified = ")  # Find the start index of the JSON data
        str_data = script_content[start_index:].strip().rstrip(";")  # Extract the JSON data as a string
        dict_data = json.loads(str_data)  # Parse the JSON data into a dictionary
        
        filtered_dict_data = self.json_extraction(dict_data, response.url)  # Little adjustment to fit in my code

        yield filtered_dict_data #returns filtered dict data to the scrapy pipeline

    def json_extraction(self, dict_data, url):
        selected_values = [  # Define a list of tuples specifying the desired attributes and their corresponding JSON paths
           ("ID", "id"),
           ("Street", "property.location.street"),
           ("HouseNumber", "property.location.number"),
           ("Box", "property.location.box"),
           ("Floor", "property.location.floor"),
           ("City", "property.location.locality"),
           ("PostalCode", "property.location.postalCode"),
           ("Region", "property.location.regionCode"),
           ("District", "property.location.district"),
           ("Province", "property.location.province"),
           ("PropertyType", "property.type"),
           ("PropertySubType", "property.subtype"),
           ("Price", "price.mainValue"),
           ("SaleType", "price.type"),
           ("ConstructionYear", "property.building.constructionYear"),
           ("BedroomCount", "property.bedroomCount"),
           ("LivingArea", "property.netHabitableSurface"),
           ("KitchenType", "property.kitchen.type"),
           ("Furnished", "transaction.sale.isFurnished"),
           ("Fireplace", "property.fireplaceExists"),
           ("Terrace", "property.hasTerrace"),
           ("TerraceArea", "property.terraceSurface"),
           ("Garden", "property.hasGarden"),
           ("GardenArea", "property.land.surface"),
           ("Facades", "property.building.facadeCount"),
           ("SwimmingPool", "property.hasSwimmingPool"),
           ("Condition", "property.building.condition"),
           ("EPCScore", "transaction.certificates.epcScore"),
           ("Latitude", "property.location.latitude"),
           ("Longitude", "property.location.longitude"),
           ("PropertyUrl", "url")
        ]
        filtered_dict_data = {}  # make this an empty dict & add the url key just before the return to ensure it's filled
        for new_key, old_key in selected_values:
            nested_keys = old_key.split(".")
            value = dict_data
            for nested_key in nested_keys:
                if isinstance(value, dict) and nested_key in value:
                    value = value[nested_key]                    
                else:
                    value = None
                    break
            if isinstance(value, bool):
                if value == True:
                    value = 1
                else:
                    value = 0
            filtered_dict_data[new_key] = value
        filtered_dict_data["PropertyUrl"] = url
        return filtered_dict_data

class ApartmentSpider(scrapy.Spider):
    name = 'Immoweb_apartments'
    start_urls = ['https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=1']
    times = 0
    looptime = 200

    def parse(self, response):
        for houses in response.css('div.card--result__body'):
            page_link = houses.css('a.card__title-link::attr(href)').get()
            if 'real-estate-project' not in page_link:
                yield response.follow(page_link, callback=self.parse_link)
        self.times += 1
        next_page = f'https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={self.times}'
        if self.times < self.looptime:  # Adjust this as needed for how many pages you want to scrape
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info('\n*\n   ~~~Last page finished.~~~\n*\n')

    def parse_link(self, response):
        # Inserting Bear's code:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)  # Find the script tag containing "window.classified = "
        script_content = script_tag.string  # Get the content of the script tag
        start_index = script_content.find("window.classified = ") + len("window.classified = ")  # Find the start index of the JSON data
        str_data = script_content[start_index:].strip().rstrip(";")  # Extract the JSON data as a string
        dict_data = json.loads(str_data)  # Parse the JSON data into a dictionary
        
        filtered_dict_data = self.json_extraction(dict_data, response.url)  # Little adjustment to fit in my code

        yield filtered_dict_data #returns filtered dict data to the scrapy pipeline

    def json_extraction(self, dict_data, url):
        selected_values = [  # Define a list of tuples specifying the desired attributes and their corresponding JSON paths
           ("ID", "id"),
           ("Street", "property.location.street"),
           ("HouseNumber", "property.location.number"),
           ("Box", "property.location.box"),
           ("Floor", "property.location.floor"),
           ("City", "property.location.locality"),
           ("PostalCode", "property.location.postalCode"),
           ("Region", "property.location.regionCode"),
           ("District", "property.location.district"),
           ("Province", "property.location.province"),
           ("PropertyType", "property.type"),
           ("PropertySubType", "property.subtype"),
           ("Price", "price.mainValue"),
           ("SaleType", "price.type"),
           ("ConstructionYear", "property.building.constructionYear"),
           ("BedroomCount", "property.bedroomCount"),
           ("LivingArea", "property.netHabitableSurface"),
           ("KitchenType", "property.kitchen.type"),
           ("Furnished", "transaction.sale.isFurnished"),
           ("Fireplace", "property.fireplaceExists"),
           ("Terrace", "property.hasTerrace"),
           ("TerraceArea", "property.terraceSurface"),
           ("Garden", "property.hasGarden"),
           ("GardenArea", "property.land.surface"),
           ("Facades", "property.building.facadeCount"),
           ("SwimmingPool", "property.hasSwimmingPool"),
           ("Condition", "property.building.condition"),
           ("EPCScore", "transaction.certificates.epcScore"),
           ("Latitude", "property.location.latitude"),
           ("Longitude", "property.location.longitude"),
           ("PropertyUrl", "url")
        ]
        filtered_dict_data = {}  # make this an empty dict & add the url key just before the return to ensure it's filled
        for new_key, old_key in selected_values:
            nested_keys = old_key.split(".")
            value = dict_data
            for nested_key in nested_keys:
                if isinstance(value, dict) and nested_key in value:
                    value = value[nested_key]                    
                else:
                    value = None
                    break
            if isinstance(value, bool):
                if value == True:
                    value = 1
                else:
                    value = 0
            filtered_dict_data[new_key] = value
        filtered_dict_data["PropertyUrl"] = url
        return filtered_dict_data
    

class HouseApartmentSpider(scrapy.Spider):
    name = 'Immoweb_houses'
    start_urls = ['https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page=1']
    times = 0
    looptime = 200
    
    def parse(self, response):
        for houses in response.css('div.card--result__body'):
            page_link = houses.css('a.card__title-link::attr(href)').get()
            if 'real-estate-project' not in page_link:
                yield response.follow(page_link, callback=self.parse_link)
        self.times += 1
        next_page = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={self.times}'
        if self.times < self.looptime:  # Adjust this as needed for how many pages you want to scrape
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info('\n*\n   ~~~Last page finished.~~~\n*\n')

    def parse_link(self, response):
        # Inserting Bear's code:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)  # Find the script tag containing "window.classified = "
        script_content = script_tag.string  # Get the content of the script tag
        start_index = script_content.find("window.classified = ") + len("window.classified = ")  # Find the start index of the JSON data
        str_data = script_content[start_index:].strip().rstrip(";")  # Extract the JSON data as a string
        dict_data = json.loads(str_data)  # Parse the JSON data into a dictionary
        
        filtered_dict_data = self.json_extraction(dict_data, response.url)  # Little adjustment to fit in my code

        yield filtered_dict_data #returns filtered dict data to the scrapy pipeline

    def json_extraction(self, dict_data, url):
        selected_values = [  # Define a list of tuples specifying the desired attributes and their corresponding JSON paths
           ("ID", "id"),
           ("Street", "property.location.street"),
           ("HouseNumber", "property.location.number"),
           ("Box", "property.location.box"),
           ("Floor", "property.location.floor"),
           ("City", "property.location.locality"),
           ("PostalCode", "property.location.postalCode"),
           ("Region", "property.location.regionCode"),
           ("District", "property.location.district"),
           ("Province", "property.location.province"),
           ("PropertyType", "property.type"),
           ("PropertySubType", "property.subtype"),
           ("Price", "price.mainValue"),
           ("SaleType", "price.type"),
           ("ConstructionYear", "property.building.constructionYear"),
           ("BedroomCount", "property.bedroomCount"),
           ("LivingArea", "property.netHabitableSurface"),
           ("KitchenType", "property.kitchen.type"),
           ("Furnished", "transaction.sale.isFurnished"),
           ("Fireplace", "property.fireplaceExists"),
           ("Terrace", "property.hasTerrace"),
           ("TerraceArea", "property.terraceSurface"),
           ("Garden", "property.hasGarden"),
           ("GardenArea", "property.land.surface"),
           ("Facades", "property.building.facadeCount"),
           ("SwimmingPool", "property.hasSwimmingPool"),
           ("Condition", "property.building.condition"),
           ("EPCScore", "transaction.certificates.epcScore"),
           ("Latitude", "property.location.latitude"),
           ("Longitude", "property.location.longitude"),
           ("PropertyUrl", "url")
        ]
        filtered_dict_data = {}  # make this an empty dict & add the url key just before the return to ensure it's filled
        for new_key, old_key in selected_values:
            nested_keys = old_key.split(".")
            value = dict_data
            for nested_key in nested_keys:
                if isinstance(value, dict) and nested_key in value:
                    value = value[nested_key]                    
                else:
                    value = None
                    break
            if isinstance(value, bool):
                if value == True:
                    value = 1
                else:
                    value = 0
            filtered_dict_data[new_key] = value
        filtered_dict_data["PropertyUrl"] = url
        return filtered_dict_data


def process_setup(spider_class, output_file):
    # Sets up out a spider's settings & the intended output
        settings = get_project_settings()  #-> get the configurations like it would run from command line
        # Setting up output
        settings.set('FEEDS', {
            output_file: {
                'format': 'csv',
                'overwrite': True,
            },
        })

        # Trying different methods for not getting banned:
            # Method 1: Adjust the Download Delay
        # settings.set('DOWNLOAD_DELAY', 3)  # Delay in seconds
                # Method 2: Use AutoThrottle
        settings.set('AUTOTHROTTLE_ENABLED', True)
        settings.set('AUTOTHROTTLE_START_DELAY', 0.01)  # Initial delay in seconds
        settings.set('AUTOTHROTTLE_MAX_DELAY', 60)  # Maximum delay in seconds

        process = CrawlerProcess(settings=settings)
        process.crawl(spider_class)
        process.start()

def run_spider(spider_class, output_file):
    p = Process(target=process_setup, args=(spider_class, output_file))
    p.start()
    p.join()

def merge_csv_files(output='merged_data.csv'):
    apartments = pd.read_csv('apartments_querry.csv')
    houses = pd.read_csv('houses_querry.csv')
    merged = pd.concat([apartments, houses])
    merged.to_csv(output, index=True)


if __name__ == '__main__':
    freeze_support()
    start_time = time.time()
    run_spider(ApartmentSpider, 'apartments_querry.csv')
    run_spider(HouseSpider, 'houses_querry.csv')
    merge_csv_files()
    # run_spider(HouseApartmentSpider, 'house+apartment_querry.csv')
    end_time = time.time()
    print(f"Spiders and CSV finished in {end_time - start_time} seconds.")

# from root folder with venv active (immo-eliza-scraping...):
    # $ python ./immoscraper/immoscraper/spiders/immospider.py
