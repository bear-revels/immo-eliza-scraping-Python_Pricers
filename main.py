import time
import asyncio
from src.utils import run_scraper

start_time = time.time()

if __name__ == "__main__":
    asyncio.run(run_scraper(10))

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")