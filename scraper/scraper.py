import requests
import csv
import time
import json
from bs4 import BeautifulSoup

class Immoscraper:

    def __init__(self):
        pass
    

    def get_property_urls(num_of_pages, session=None):
        '''Gets a list of URLs of properties for sale from immoweb.

        :param num_of_pages: Number of immoweb pages to process (int).
        :param session: Optional session object for requests (requests.Session).
        :return: List of all property URLs in the specified page(s) (list).
        '''
        # If session is not provided, create a new session
        if session is None:
            session = requests.Session()

        # Initialize an empty list to store property URLs
        all_urls = []

        # Iterate through the specified number of pages
        for i in range(1, num_of_pages + 1):
            # Construct the URL for the current page
            root_url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={i}"
        
            # Send a GET request to the current page URL
            req = session.get(root_url)
        
            # Parse the HTML content of the response
            soup = BeautifulSoup(req.content, "html.parser")
        
            # Check if the request was successful (status code 200)
            if req.status_code == 200:
                # Extract property URLs from the parsed HTML
                result_divs = soup.select('div.card--result__body')
                for div in result_divs:
                    # Extract the URL from the current div and append it to the list
                    page_link = div.select_one('a.card__title-link')['href']
                    all_urls.append(page_link)
            else:
                # If the request was not successful, print a message and exit the loop
                print("No URL found.")
                break
    
        # Close the session to release resources
        session.close()
    
        # Return the list of property URLs
        return all_urls


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


start_time = time.time()

immo_urls = Immoscraper.get_property_urls(1)  # to test only getting the urls list

#all_property_details = []  # to test the whole script
#for url in immo_urls:     
#    print(url)
#    property_details = Immoscraper.extract_details(url)
#    all_property_details.append(property_details)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


#Immoscraper.write_dictlist_to_csv(all_property_details, "all_property_details.csv")
# write_json(immo_urls, "url_list.json")