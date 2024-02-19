from bs4 import BeautifulSoup
import pandas as pd
import json
import requests
from io import StringIO

url = "https://www.immoweb.be/en/classified/villa/for-sale/overijse/3090/11150716"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find the script tag containing "window.classified = "
script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)

if script_tag:
    # Extract the content of the script tag
    script_content = script_tag.string
    
    # Find the index of "window.classified = "
    start_index = script_content.find("window.classified = ") + len("window.classified = ")
    
    if start_index != -1:
        # Extract everything after "window.classified = " and remove the trailing semicolon
        json_data = script_content[start_index:].strip().rstrip(";")

        # Convert JSON data to DataFrame using StringIO
        df = pd.read_json(StringIO(json_data), typ='series')

        # Print the new DataFrame
        print(df)
    else:
        print("No JSON data found after 'window.classified = '.")
else:
    print("No script tag found with 'window.classified = '.")