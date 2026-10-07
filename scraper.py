import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import logging
import pandas as pd

from datetime import datetime
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Logging setup
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Scraping started")

# User input
url = input("Enter website URL: ")
keyword = input("Enter keyword: ")

# Current date and time
current_time = datetime.now()

print(Fore.CYAN + "\nScraping started at:")
print(Fore.YELLOW + str(current_time))
print(Fore.MAGENTA + "-" * 50)

# Headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Store data
news_data = []

try:
    # Send request
    response = requests.get(url, headers=headers, timeout=10)

    # Status handling
    if response.status_code == 200:
        print(Fore.GREEN + "Website connected successfully!")
        logging.info("Website connected successfully")

    elif response.status_code == 404:
        print(Fore.RED + "Website not found!")
        logging.error("404 Website not found")

    else:
        print(Fore.RED + f"Failed to connect! Status code: {response.status_code}")
        logging.error(f"Failed with status code {response.status_code}")

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract headlines
    headlines = soup.find_all("a")

    # Loop through headlines
    for headline in headlines:

        title = headline.text.strip()
        link = headline.get("href")

        # Ignore empty titles
        if not title:
            continue

        # Keyword filtering
        if keyword.lower() in title.lower():

            # Category detection
            category = "General"

            if "ai" in title.lower() or "technology" in title.lower():
                category = "Technology"

            elif "cricket" in title.lower() or "football" in title.lower():
                category = "Sports"

            elif "election" in title.lower() or "government" in title.lower():
                category = "Politics"

            elif "movie" in title.lower() or "music" in title.lower():
                category = "Entertainment"

            # Display output
            print(Fore.GREEN + "\nTitle: " + title)
            print(Fore.BLUE + "Link: " + str(link))
            print(Fore.YELLOW + "Category: " + category)
            print(Fore.MAGENTA + "-" * 50)

            # Save data
            news_data.append({
                "title": title,
                "link": link,
                "category": category,
                "scraped_time": str(current_time)
            })

            # Logging
            logging.info(f"Headline scraped: {title}")

            # Delay
            time.sleep(1)

    # Save CSV
    with open("news.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Title",
            "Link",
            "Category",
            "Scraped Time"
        ])

        for item in news_data:
            writer.writerow([
                item["title"],
                item["link"],
                item["category"],
                item["scraped_time"]
            ])

    logging.info("CSV file saved successfully")

    # Save JSON
    with open("news.json", "w", encoding="utf-8") as json_file:
        json.dump(news_data, json_file, indent=4)

    logging.info("JSON file saved successfully")

    # Save Excel
    df = pd.DataFrame(news_data)

    df.to_excel("news.xlsx", index=False)

    logging.info("Excel file saved successfully")

    print(Fore.CYAN + "\nScraping completed successfully!")
    print(Fore.YELLOW + "Files created:")
    print(Fore.GREEN + "news.csv")
    print(Fore.GREEN + "news.json")
    print(Fore.GREEN + "news.xlsx")
    print(Fore.GREEN + "scraper.log")

except requests.exceptions.Timeout:
    print(Fore.RED + "Request timed out!")
    logging.error("Request timeout")

except requests.exceptions.ConnectionError:
    print(Fore.RED + "Connection error!")
    logging.error("Connection error")

except Exception as e:
    print(Fore.RED + "Error:", e)
    logging.error(f"Unexpected error: {e}")