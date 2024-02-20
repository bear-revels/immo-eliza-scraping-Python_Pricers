from bs4 import BeautifulSoup  # Import BeautifulSoup for web scraping
import json  # Import json for working with JSON data
import requests  # Import requests for making HTTP requests
import time  # Import time for measuring performance

# Initialize the performance counter
start_time = time.perf_counter()

url = "https://www.immoweb.be/en/classified/villa/for-sale/overijse/3090/11150716"  # Define the URL of the webpage to scrape
r = requests.get(url)  # Send a GET request to the URL
soup = BeautifulSoup(r.content, "html.parser")  # Create a BeautifulSoup object to parse the HTML content

property_details = []  # Initialize an empty list to store property details extracted from the webpage
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

def extract_details(url):  # Define a function to extract property details from the webpage
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
    property_details.append(filtered_dict_data)  # Append the filtered dictionary to the list of property details
    print(property_details)  # Print the list of property details

extract_details(url)  # Call the extract_details function with the specified URL

# Calculate the elapsed time
elapsed_time = time.perf_counter() - start_time  # Calculate the elapsed time
print(f"Elapsed time: {elapsed_time:.2f} seconds")  # Print the elapsed time
