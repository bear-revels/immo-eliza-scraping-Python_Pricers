import csv  # Import CSV module for reading and writing CSV files
from datetime import datetime #Import datetime module to give the start_time when running program 
from .scraper import ImmowebScraper  # Import ImmowebScraper class from scraper module


def write_dictlist_to_csv(data, csv_file):
    """
    Write a list of dictionaries to a CSV file.

    Args:
        data (list of dict): List of dictionaries to be written to the CSV file.
        csv_file (str): Path to the CSV file.

    Returns:
        None
    """
    # Filter out None values from data
    filtered_data = [row for row in data if row is not None]
    if filtered_data:  # Check if filtered data is not empty
        with open(csv_file, 'w', newline='') as file:  # Open CSV file for writing
            writer = csv.DictWriter(file, fieldnames=filtered_data[0].keys())  # Create CSV DictWriter object
            writer.writeheader()  # Write header row to CSV file
            writer.writerows(filtered_data)  # Write rows to CSV file
        print(f'Data has been written to {csv_file}')  # Print success message
    else:
        print("No data to write.")  # Print message if no data to write


async def run_scraper(page_count=1):
    """
    Run the ImmowebScraper to scrape property details and write them to a CSV file.

    Args:
        page_count (int): Number of pages to scrape (default is 1).

    Returns:
        None
    """
    scraper = ImmowebScraper()  # Create an instance of ImmowebScraper
    all_property_details = await scraper.scrape(page_count)  # Scrape property details
    write_dictlist_to_csv(all_property_details, "././data/all_property_details.csv")
    # Write property details to CSV file

def give_time():
    c = datetime.now()
    print("Begin running at: ", c.strftime('%H:%M:%S'))    
    print("Data loading...")