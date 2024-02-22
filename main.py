import time  # Import time module to measure execution time
import asyncio  # Import asyncio for asynchronous programming
from src.utils import run_scraper  # Import run_scraper function from src.utils module

start_time = time.time()  # Record start time of the program

if __name__ == "__main__":
    # Run the scraper asynchronously for 10 pages
    asyncio.run(run_scraper(10))

end_time = time.time()  # Record end time of the program
elapsed_time = end_time - start_time  # Calculate elapsed time
print(f"Elapsed time: {elapsed_time} seconds")  # Print the elapsed time