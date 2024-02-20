import requests
from bs4 import BeautifulSoup
import json

session = requests.Session()
def get_property_urls(num_page, session):
    all_urls = []
    for i in range (1, num_page + 1):
        print(i)
        root_url = f'https://www.immoweb.be/en/search/house-and-apertment/for-sale?countries=BE&page={i}'
        req = session.get(root_url)
        content = req.content
        soup = BeautifulSoup(content, "html.parser")
        if req.status_code == 200:
            all_urls.extend(tag.get("href")for tag in soup.find_all("a", attrs={"class":"card__title-link"}))
        else:
            print("No url found")
            break
    print(f"Number of properties: {len(all_urls)}")
    return all_urls

urls = get_property_urls(200, session)
json_file_path = "property_urls.json"
with open(json_file_path, "w") as json_file:
    json.dump(urls, json_file, indent=4)

print("Property URLs have been saved to:", json_file_path)


