import time
import asyncio
from datetime import datetime
from src.utils import give_time, run_scraper, copy_to_archive, remove_duplicates_from_csv  # Import functions from src.utils module

start_time = time.time()

if __name__ == "__main__":
    # Give the time start running program
    give_time()
    
    # Copy CSV file to Archive folder with today's date
    copy_to_archive("./data/all_property_details.csv")

    # Run the scraper asynchronously for # of pages entered
    asyncio.run(run_scraper(333))

    # Remove duplicates from the CSV file
    remove_duplicates_from_csv("./data/all_property_details.csv")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")