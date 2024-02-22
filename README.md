# immo-eliza-scraping-Python_Pricers

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## 📒 Description

Immo-eliza-scraping is a Python program designed to scrape property listing data from immoweb, Belgium's leading real estate website, using a combination of techniques including BeautifulSoup, Scrapy, and threading. It gathers the unique listing URL for each active listing and then retrieves specific property data from each of the listings. The property data is then compiled into a CSV file for later use in data analysis, visualization, model training, and pricing forecasts. There are more than 10,000 active listing at any given time, so the scraping tools and code were written with performance optimization in mind.

## 📦 Repo structure

```
.
├── src/
│ └── scraper.py
├── main.py
└── README.md
```

## 🎮 Usage

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command in your terminal:

    ```
    pip install -r requirements.txt
    ```

3. Run the `main.py` file to execute the scraper:

    ```
    python main.py
    ```

4. The program will first scrape the URLs of active real estate listings from the immoweb webpages and then extract the property details from each listing. The resulting data will be saved to a CSV file named "real_estate_listing_data.csv" in the root directory.

5. The total execution time will be displayed in the terminal upon completion, estimated at ~6 minutes.

## ⏱️ Timeline

The development of this project took 4 days for completion.

## 📌 Personal Situation

This project was completed as part of the AI Boocamp at BeCode.org by team Python Pricers. 

Connect with the Python Pricers on LinkedIn:
1. [Bear Revels](https://www.linkedin.com/in/bear-revels/)
2. [Caroline](https://www.linkedin.com/in/bear-revels/)
3. [Geraldine Nadela](https://www.linkedin.com/in/geraldine-nadela-60827a11)
4. [Viktor](https://www.linkedin.com/in/bear-revels/)
