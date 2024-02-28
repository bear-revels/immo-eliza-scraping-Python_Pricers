import json
import requests
from bs4 import BeautifulSoup

url = "https://www.immoweb.be/en/classified/house/for-sale/bruxelles/1000/10984241"
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)
    if script_tag:
        script_content = script_tag.string
        start_index = script_content.find("window.classified = ") + len("window.classified = ")
        str_data = script_content[start_index:].strip().rstrip(";")
        print(json.loads(str_data))
    else:
        print("Script tag not found")
else:
    print("Error fetching URL:", response.status_code)