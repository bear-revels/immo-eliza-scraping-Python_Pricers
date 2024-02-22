import requests
import csv
import time
import json
import threading
from bs4 import BeautifulSoup

start_time = time.time()

class ImmowebScraper:
    def __init__(self):
        self.lock = threading.Lock()
        self.all_urls = []

    def get_urls_from_page(self, page_num, session):
        root_url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page_num}"
        req = session.get(root_url)
        if req.status_code == 200:
            soup = BeautifulSoup(req.content, "html.parser")
            result_divs = soup.select('div.card--result__body')
            for div in result_divs:
                page_link = div.select_one('a.card__title-link')['href']
                if 'real-estate-project' not in page_link:
                    with self.lock:
                        self.all_urls.append(page_link)
        else:
            print("No url found.")

    def get_property_urls(self, num_of_pages, session=None):
        if session is None:
            session = requests.Session()

        threads = []
        for i in range(1, num_of_pages + 1):
            print(i)
            thread = threading.Thread(target=self.get_urls_from_page, args=(i, session))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        session.close()
        return self.all_urls

    def extract_details(url):  # Define a function to extract property details from the webpage
         
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

        r = requests.get(url)  # Send a GET request to the URL
        soup = BeautifulSoup(r.content, "html.parser")  # Create a BeautifulSoup object to parse the HTML content
        script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)  # Find the script tag containing "window.classified = "
        script_content = script_tag.string  # Get the content of the script tag
        start_index = script_content.find("window.classified = ") + len("window.classified = ")  # Find the start index of the JSON data
        str_data = script_content[start_index:].strip().rstrip(";")  # Extract the JSON data as a string
        dict_data = json.loads(str_data)  # Parse the JSON data into a dictionary

        filtered_dict_data = {}  # Initialize an empty dictionary to store filtered property details
        for new_key, old_key in selected_values:  # Iterate over the selected values
            nested_keys = old_key.split(".")  # Split the nested keys by dot notation
            value = dict_data  # Initialize the value with the parsed JSON data
            for nested_key in nested_keys:  # Iterate over the nested keys
                if isinstance(value, dict) and nested_key in value:  # Check if the value is a dictionary and the nested key exists
                    value = value[nested_key]  # Update the value with the nested value
                else:
                    value = None  # Set the value to None if the nested key does not exist
                    break
            if isinstance(value, bool):
                if value == True:
                    value = 1
                else:
                    value = 0
            filtered_dict_data[new_key] = value  # Assign the filtered value to the new key in the filtered dictionary
        filtered_dict_data["Property url"] = url  # Add the URL of the property to the filtered dictionary
        return filtered_dict_data   # Return the list of property details


    def write_to_csv(data_dict, csv_filename):
        keys = data_dict.keys()

        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)        
            writer.writeheader()        
            writer.writerow(data_dict)


    def write_dictlist_to_csv(data, csv_file):
        """
        Write a list of dictionaries to a CSV file.

        Args:
        - data (list of dict): List of dictionaries to be written to the CSV file.
        - csv_file (str): Path to the CSV file.

        Returns:
        - None
        """
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())

            # Write header
            writer.writeheader()

            # Write rows
            for row in data:
                writer.writerow(row)

        print(f'Data has been written to {csv_file}')
   

def write_json(content, file):
    with open(file, 'w') as json_file:
        json.dump(content, json_file, indent=4)

    print("Property URLs have been saved to:", file)

all_property_details = []
scraper = ImmowebScraper()
immo_urls = scraper.get_property_urls(300) 
for url in immo_urls:
    property_details = ImmowebScraper.extract_details(url)
    all_property_details.append(property_details)
end_time = time.time()
elapsed_time = end_time - start_time
ImmowebScraper.write_dictlist_to_csv(all_property_details, "all_property_details.csv")
print(f"Elapsed time: {elapsed_time} seconds")