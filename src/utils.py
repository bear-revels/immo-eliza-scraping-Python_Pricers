import csv
from .scraper import ImmowebScraper


def write_dictlist_to_csv(data, csv_file):
    '''
    Write a list of dictionaries to a CSV file.

    Args:
        data (list): A list of dictionaries containing data to be written to the CSV file.
        csv_file (str): The path to the CSV file to write the data to.

    Returns:
        None
    '''
    filtered_data = [row for row in data if row is not None]  # Filter out None values
    if filtered_data:
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=filtered_data[0].keys())
            writer.writeheader()
            writer.writerows(filtered_data)
        print(f'Data has been written to {csv_file}')
    else:
        print("No data to write.")


async def run_scraper(page_count=1):
    '''
    Asynchronously runs a web scraper to collect property details and writes them to a CSV file.

    Args:
        page_count (int, optional): The number of pages to scrape. Defaults to 1.

    Returns:
        None
    '''
    scraper = ImmowebScraper()
    all_property_details = await scraper.scrape(page_count)
    write_dictlist_to_csv(all_property_details, "././data/all_property_detaile(1s.csv")

