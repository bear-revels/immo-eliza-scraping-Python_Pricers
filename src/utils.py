import csv
import shutil
import os
from datetime import datetime
from pathlib import Path
from .scraper import ImmowebScraper


def copy_to_archive(csv_file):
    """
    Copy the CSV file to the Archive folder and rename it with the last modified date of the original file.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        None
    """
    archive_folder = Path("././data/Archive")
    archive_folder.mkdir(parents=True, exist_ok=True)  # Create Archive folder if it doesn't exist

    # Get the last modified timestamp of the original CSV file
    last_modified_timestamp = os.path.getmtime(csv_file)
    last_modified_date = datetime.fromtimestamp(last_modified_timestamp)
    formatted_date = last_modified_date.strftime("%m%d%Y")

    # Construct the new file name with the last modified date
    file_name = f"all_property_details_{formatted_date}.csv"
    destination = archive_folder / file_name

    shutil.copyfile(csv_file, destination)
    print(f"CSV file copied to Archive folder: {destination}")

def remove_duplicates_from_csv(csv_file):
    """
    Remove duplicates from a CSV file based on the 'ID' column, keeping the last version encountered.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        None
    """
    # Read existing data from CSV file
    existing_data = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        existing_data = [row for row in reader]

    # Remove duplicates based on the 'ID' column, keeping the last version encountered
    unique_data = {row['ID']: row for row in reversed(existing_data)}.values()

    # Write unique data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=existing_data[0].keys())
        writer.writeheader()
        for row in unique_data:
            writer.writerow(row)

    print(f'Duplicates removed from {csv_file}')  # Print success message

def write_dictlist_to_csv(data, csv_file):
    """
    Append a list of dictionaries to a CSV file and remove duplicates based on the 'ID' column,
    keeping the last version encountered. Update ListingCloseDate with today's date for rows where
    no duplicate is found.

    Args:
        data (list of dict): List of dictionaries to be appended to the CSV file.
        csv_file (str): Path to the CSV file.

    Returns:
        None
    """
    # Filter out None values from data
    filtered_data = [row for row in data if row is not None]
    if filtered_data:  # Check if filtered data is not empty
        # Add today's date to ListingCloseDate for rows where no duplicate is found
        for row in filtered_data:
            if not row.get("ListingCloseDate"):
                row["ListingCloseDate"] = datetime.now().strftime("%m/%d/%Y")

        # Append new data to CSV file
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=filtered_data[0].keys())
            for row in filtered_data:
                writer.writerow(row)

        print(f'Data has been appended to {csv_file}')  # Print success message
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