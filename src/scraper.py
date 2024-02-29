import csv
import json
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup

class ImmowebScraper:
    """
    A class for scraping property details from Immoweb.
    """

    def __init__(self):
        """
        Initialize ImmowebScraper object.
        """
        self.lock = asyncio.Lock()
        self.all_urls = []
        self.retry_urls = []
        self.failed_urls = []
        self.semaphore = asyncio.Semaphore(10)  # Limit concurrency to 10 requests

    async def get_urls_from_page(self, root_url, page_num, session):
        """
        Get URLs of properties from a specific page.

        :param root_url: Root URL template (str).
        :param page_num: Page number to fetch URLs from (int).
        :param session: aiohttp ClientSession object.
        """
        async with self.semaphore:
            async with session.get(root_url.format(page_num=page_num)) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    result_divs = soup.select('div.card--result__body')
                    if not result_divs:
                        return
                    for div in result_divs:
                        page_link = div.select_one('a.card__title-link')['href']
                        if 'real-estate-project' not in page_link:
                            async with self.lock:
                                self.all_urls.append(page_link)
                await asyncio.sleep(random.uniform(1, 5))

    async def get_property_details(self, url, session):
        """
        Get details of a property with a backoff retry strategy.

        :param url: URL of the property (str).
        :param session: aiohttp ClientSession object.
        :return: Dictionary containing property details.
        """
        retry_attempts = 3
        base_delay = 2  # Initial delay in seconds
        for attempt in range(retry_attempts):
            try:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)
                        if script_tag:
                            script_content = script_tag.string
                            start_index = script_content.find("window.classified = ") + len("window.classified = ")
                            str_data = script_content[start_index:].strip().rstrip(";")
                            return json.loads(str_data)
                        else:
                            # If script tag not found, wait and retry
                            await asyncio.sleep(base_delay * (2 ** attempt))
                    else:
                        return None
            except aiohttp.ClientError:
                pass  # Retry automatically with backoff delay
            except asyncio.TimeoutError:
                pass  # Retry automatically with backoff delay

        self.failed_urls.append(url)
        return None

    async def extract_details(self, url, session):
        """
        Extract details of a property.

        :param url: URL of the property (str).
        :param session: aiohttp ClientSession object.
        :return: Dictionary containing property details.
        """
        selected_values = [
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

        property_details = await self.get_property_details(url, session)
        if property_details:
            filtered_dict_data = {}
            for new_key, old_key in selected_values:
                nested_keys = old_key.split(".")
                value = property_details
                for nested_key in nested_keys:
                    value = value.get(nested_key)
                    if value is None:
                        break
                if isinstance(value, bool):
                    value = int(value)
                filtered_dict_data[new_key] = value
            filtered_dict_data["Property url"] = url
            return filtered_dict_data

    async def scrape(self, num_of_pages):
        """
        Scrape property details.

        :param num_of_pages: Number of pages to scrape (int).
        :return: List of dictionaries containing property details.
        """
        async with aiohttp.ClientSession() as session:  # Create aiohttp ClientSession object
            tasks = []  # Initialize list to store asynchronous tasks
            urls = [
                "https://www.immoweb.be/en/search/apartment/for-sale/antwerp/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/west-flanders/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/east-flanders/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/limburg/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/flemish-brabant/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/hainaut/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/liege/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/luxembourg/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/namur/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/walloon-brabant/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale/brussels/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/antwerp/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/west-flanders/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/east-flanders/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/limburg/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/flemish-brabant/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/hainaut/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/liege/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/luxembourg/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/namur/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/walloon-brabant/province?countries=BE&priceType=SALE_PRICE&page={page_num}",
                "https://www.immoweb.be/en/search/house/for-sale/brussels/province?countries=BE&priceType=SALE_PRICE&page={page_num}"
            ]
            # List of URLs to scrape properties from
            for url in urls:
                for i in range(1, num_of_pages + 1):
                    tasks.append(self.get_urls_from_page(url, i, session))
            await asyncio.gather(*tasks)

            tasks = [self.extract_details(url, session) for url in self.all_urls]
            results = await asyncio.gather(*tasks)

            if self.failed_urls:
                with open('failed_urls.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Failed URLs'])
                    writer.writerows([[url] for url in self.failed_urls])

            return results