import requests
import csv
import time
import json
from bs4 import BeautifulSoup


class Immoscraper:
    """
    A class for scraping property details from Immoweb.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_property_urls(num_of_pages, session=None):
        """
        Gets a list of URLs of properties for sale from Immoweb.

        :param num_of_pages: Number of Immoweb pages to process (int).
        :param session: Optional session object for requests (requests.Session).
        :return: List of all property URLs in the specified page(s) (list).
        """
        if session is None:
            session = requests.Session()

        all_urls = []

        for i in range(1, num_of_pages + 1):
            root_url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={i}"
            req = session.get(root_url)
            soup = BeautifulSoup(req.content, "html.parser")

            if req.status_code == 200:
                result_divs = soup.select('div.card--result__body')
                for div in result_divs:
                    page_link = div.select_one('a.card__title-link')['href']
                    all_urls.append(page_link)
            else:
                print("No URL found.")
                break

        session.close()

        return all_urls

    @staticmethod
    def extract_details(url):
        """
        Extracts property details from the webpage.

        :param url: URL of the property (str).
        :return: Dictionary containing property details.
        """
        selected_values = [
            ("ID", "id"),
            ("Street", "property.location.street"),
            ("HouseNumber", "property.location.number"),
            # Add more selected values here
            ("PropertyUrl", "url")
        ]

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)
        script_content = script_tag.string
        start_index = script_content.find("window.classified = ") + len("window.classified = ")
        str_data = script_content[start_index:].strip().rstrip(";")
        dict_data = json.loads(str_data)

        filtered_dict_data = {}
        for new_key, old_key in selected_values:
            nested_keys = old_key.split(".")
            value = dict_data
            for nested_key in nested_keys:
                if isinstance(value, dict) and nested_key in value:
                    value = value[nested_key]
                else:
                    value = None
                    break
            filtered_dict_data[new_key] = value
        filtered_dict_data["Property url"] = url
        return filtered_dict_data

    @staticmethod
    def write_dictlist_to_csv(data, csv_file):
        """
        Write a list of dictionaries to a CSV file.

        :param data: List of dictionaries to be written to the CSV file.
        :param csv_file: Path to the CSV file (str).
        :return: None
        """
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f'Data has been written to {csv_file}')


def write_json(content, file):
    """
    Write content to a JSON file.

    :param content: Content to be written (list, dict, etc.).
    :param file: Path to the JSON file (str).
    :return: None
    """
    with open(file, 'w') as json_file:
        json.dump(content, json_file, indent=4)

    print("Property URLs have been saved to:", file)


start_time = time.time()

immo_urls = Immoscraper.get_property_urls(1)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")