import csv  # Import CSV module for reading and writing CSV files
import json  # Import JSON module for working with JSON data
import asyncio  # Import asyncio module for asynchronous programming
import aiohttp  # Import aiohttp module for making asynchronous HTTP requests
import random  # Import random module for generating random numbers
from bs4 import BeautifulSoup  # Import BeautifulSoup from bs4 module for parsing HTML

class ImmowebScraper:
    """
    A class for scraping property details from Immoweb.
    """

    def __init__(self):
        """
        Initialize ImmowebScraper object.
        """
        self.lock = asyncio.Lock()  # Create a lock for asynchronous synchronization
        self.all_urls = []  # Initialize an empty list to store all property URLs
        self.retry_urls = []  # Initialize an empty list to store URLs that need to be retried
        self.failed_urls = []  # Initialize an empty list to store URLs that failed

    async def get_urls_from_page(self, root_url, page_num, session):
        """
        Get URLs of properties from a specific page.

        :param root_url: Root URL template (str).
        :param page_num: Page number to fetch URLs from (int).
        :param session: aiohttp ClientSession object.
        """
        async with session.get(root_url.format(page_num=page_num)) as response:
            # Send a GET request to the specified page URL
            if response.status == 200:  # Check if the response status is OK (200)
                html = await response.text()  # Get the HTML content of the response
                soup = BeautifulSoup(html, "html.parser")  # Create a BeautifulSoup object to parse HTML
                result_divs = soup.select('div.card--result__body')  # Select all result divs
                for div in result_divs:  # Iterate over each result div
                    page_link = div.select_one('a.card__title-link')['href']  # Extract property URL
                    if 'real-estate-project' not in page_link:  # Check if it's not a project URL
                        async with self.lock:  # Acquire the lock to safely update the list
                            self.all_urls.append(page_link)  # Append the URL to the list
            else:
                print(f"No URLs found for {root_url.format(page_num=page_num)}")  # Print message if no URLs found

        await asyncio.sleep(random.uniform(1, 3))  # Introduce random delay before processing next page

    async def get_property_details(self, url, session):
        """
        Get details of a property.

        :param url: URL of the property (str).
        :param session: aiohttp ClientSession object.
        :return: Dictionary containing property details.
        """
        retry_attempts = 3  # Set maximum retry attempts
        for attempt in range(retry_attempts):  # Iterate over retry attempts
            try:
                async with session.get(url) as response:  # Send a GET request to the URL
                    if response.status == 200:  # Check if the response status is OK (200)
                        html = await response.text()  # Get the HTML content of the response
                        soup = BeautifulSoup(html, "html.parser")  # Create a BeautifulSoup object
                        script_tag = soup.find("script", string=lambda text: text and "window.classified =" in text)
                        # Find the script tag containing property details
                        if script_tag:  # Check if script tag exists
                            script_content = script_tag.string  # Get the content of the script tag
                            start_index = script_content.find("window.classified = ") + len("window.classified = ")
                            str_data = script_content[start_index:].strip().rstrip(";")
                            # Extract JSON data as a string
                            return json.loads(str_data)  # Parse JSON data into a dictionary
                    else:
                        return None  # Return None if response status is not OK
            except aiohttp.ClientError:  # Handle client errors
                if attempt == retry_attempts - 1:  # Check if it's the last retry attempt
                    print(f"Failed to retrieve property details for {url}")  # Print failure message
                else:
                    print(f"Retrying ({attempt+1}/{retry_attempts}) to retrieve property details for {url}")
                    # Print retry attempt message
                    await asyncio.sleep(random.uniform(1, 3))  # Introduce delay before retry
            except asyncio.TimeoutError:  # Handle timeout errors
                if attempt == retry_attempts - 1:  # Check if it's the last retry attempt
                    print(f"Timed out while retrieving property details for {url}")  # Print timeout message
                else:
                    print(f"Retrying ({attempt+1}/{retry_attempts}) due to timeout for {url}")
                    # Print retry attempt message
                    await asyncio.sleep(random.uniform(1, 3))  # Introduce delay before retry

        # If all retry attempts fail, add the URL to the list of failed URLs
        self.failed_urls.append(url)
        return None

    async def extract_details(self, url, session):
        """
        Extract details of a property.

        :param url: URL of the property (str).
        :param session: aiohttp ClientSession object.
        :return: Dictionary containing property details.
        """
        selected_values = [
            # List of selected property details
        ]

        property_details = await self.get_property_details(url, session)  # Get property details
        if property_details:  # Check if property details exist
            filtered_dict_data = {}  # Initialize dictionary to store filtered details
            for new_key, old_key in selected_values:  # Iterate over selected values
                nested_keys = old_key.split(".")  # Split nested keys by dot notation
                value = property_details  # Initialize value with property details
                for nested_key in nested_keys:  # Iterate over nested keys
                    value = value.get(nested_key)  # Get nested value
                    if value is None:  # Check if nested value is None
                        break  # Break loop if nested value is None
                if isinstance(value, bool):  # Check if value is boolean
                    value = int(value)  # Convert boolean value to integer
                filtered_dict_data[new_key] = value  # Add filtered value to dictionary
            filtered_dict_data["Property url"] = url  # Add property URL to dictionary
            return filtered_dict_data  # Return dictionary containing property details

    async def scrape(self, num_of_pages):
        """
        Scrape property details.

        :param num_of_pages: Number of pages to scrape (int).
        :return: List of dictionaries containing property details.
        """
        async with aiohttp.ClientSession() as session:  # Create aiohttp ClientSession object
            tasks = []  # Initialize list to store asynchronous tasks
            urls = [
                "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={page_num}",
                "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={page_num}"
            ]
            # List of URLs to scrape properties from
            for url in urls:  # Iterate over URLs
                for i in range(1, num_of_pages + 1):  # Iterate over specified number of pages
                    tasks.append(self.get_urls_from_page(url, i, session))  # Add task to list
            await asyncio.gather(*tasks)  # Gather and await all tasks

            tasks = [self.extract_details(url, session) for url in self.all_urls]  # Create tasks for property details
            results = await asyncio.gather(*tasks)  # Gather and await all tasks

            # Retry failed URLs
            for url in self.retry_urls:  # Iterate over retry URLs
                result = await self.extract_details(url, session)  # Get property details
                if result:  # Check if property details exist
                    results.append(result)  # Append property details to results list

            # Write failed URLs to 'failed_urls.csv' file
            if self.failed_urls:  # Check if failed URLs exist
                with open('failed_urls.csv', 'w', newline='') as file:  # Open file for writing
                    writer = csv.writer(file)  # Create CSV writer object
                    writer.writerow(['Failed URLs'])  # Write header
                    writer.writerows([[url] for url in self.failed_urls])  # Write failed URLs to file

            return results  # Return list of dictionaries containing property details