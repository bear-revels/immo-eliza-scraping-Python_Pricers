import time
import asyncio
from src.scraper import ImmowebScraper
from src.utils import write_dictlist_to_csv

async def main():
    scraper = ImmowebScraper()
    all_property_details = await scraper.scrape(1)
    write_dictlist_to_csv(all_property_details, "./data/all_property_details.csv")


start_time = time.time()

if __name__ == "__main__":
    asyncio.run(main())

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")