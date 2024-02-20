import requests
import json
import time
from bs4 import BeautifulSoup

def get_property_urls(base_url, page):
    
    # Construct the URL
    url = base_url + str(page)
    print('page: ' + str(page))

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all href tags 
        href_tags = soup.find_all(href=True)

        # Filter out the URLs that belong to the specified domain
        classified_urls = []
        for tag in href_tags:
            href = tag['href']
            if href.startswith('https://www.immoweb.be/en/classified/'):
                classified_urls.append(href)
                (print(href))

        # dump to 1 list:
        url_list = [item for sublist in classified_urls for item in sublist]        
    return url_list

# Define the pages to call 

base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page="
property_urls = []

# adding pauses to prevent web time out
for page in range(1,100):
    urls = get_property_urls(base_url, page)
    property_urls.append(urls)
time.sleep(1)
for page in range(100, 200):
    urls = get_property_urls(base_url, page)
    property_urls.append(urls)
time.sleep(1)
for page in range(200, 300):
    urls = get_property_urls(base_url, page)
    property_urls.append(urls)
time.sleep(1)
for page in range(300, 334):
    urls = get_property_urls(base_url, page)
    property_urls.append(urls)
time.sleep(1)

# Specify the file path where to save the JSON file
json_file_path = "property_urls.json"

# Write the property_urls list to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(property_urls, json_file, indent=4)

print("Property URLs have been saved to:", json_file_path)



