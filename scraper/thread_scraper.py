import requests
import threading
import time
import json
from bs4 import BeautifulSoup

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

def write_json(content, file):
    with open(file, 'w') as json_file:
        json.dump(content, json_file, indent=4)

    print("Property URLs have been saved to:", file)


start_time = time.time()

scraper = ImmowebScraper()
url_list = scraper.get_property_urls(1)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")  
print(str(len(url_list)) + ' urls')

# write_json(url_list, url_list.json)
