import csv
import time
import json
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup

start_time = time.time()

class ImmowebScraper:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.all_urls = []

    async def get_urls_from_page(self, page_num, session):
        root_url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page_num}"
        async with session.get(root_url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                result_divs = soup.select('div.card--result__body')
                for div in result_divs:
                    page_link = div.select_one('a.card__title-link')['href']
                    if 'real-estate-project' not in page_link:
                        async with self.lock:
                            self.all_urls.append(page_link)
            else:
                print("No url found.")
        
        # Introduce a random delay between 1 and 3 seconds before processing the next page
        await asyncio.sleep(random.uniform(1, 3))

    async def get_property_details(self, url, session):
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)
                if script_tag:
                    script_content = script_tag.string
                    start_index = script_content.find("window.classified = ") + len("window.classified = ")
                    str_data = script_content[start_index:].strip().rstrip(";")
                    return json.loads(str_data)
            return None

    async def extract_details(self, url, session):
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
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(1, num_of_pages + 1):
                tasks.append(self.get_urls_from_page(i, session))
            await asyncio.gather(*tasks)
            
            tasks = [self.extract_details(url, session) for url in self.all_urls]
            return await asyncio.gather(*tasks)

    @staticmethod
    def write_dictlist_to_csv(data, csv_file):
        if data:
            with open(csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f'Data has been written to {csv_file}')
        else:
            print("No data to write.")

async def main():
    scraper = ImmowebScraper()
    all_property_details = await scraper.scrape(100)
    ImmowebScraper.write_dictlist_to_csv(all_property_details, "all_property_details.csv")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

if __name__ == "__main__":
    asyncio.run(main())