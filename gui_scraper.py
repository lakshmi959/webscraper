import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
import csv
import json
import time
import logging
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

logging.info("Application Started")

# Main window
window = tk.Tk()

window.title("Advanced News Web Scraper")

window.geometry("900x700")

window.configure(bg="#f0f0f0")

# Title
title_label = tk.Label(
    window,
    text="Advanced News Web Scraper",
    font=("Arial", 20, "bold"),
    bg="#f0f0f0",
    fg="darkblue"
)

title_label.pack(pady=10)

# URL Label
url_label = tk.Label(
    window,
    text="Enter Website URL:",
    font=("Arial", 12),
    bg="#f0f0f0"
)

url_label.pack()

# URL Entry
url_entry = tk.Entry(
    window,
    width=80,
    font=("Arial", 11)
)

url_entry.pack(pady=5)

# Keyword Label
keyword_label = tk.Label(
    window,
    text="Enter Keyword:",
    font=("Arial", 12),
    bg="#f0f0f0"
)

keyword_label.pack()

# Keyword Entry
keyword_entry = tk.Entry(
    window,
    width=40,
    font=("Arial", 11)
)

keyword_entry.pack(pady=5)

# Output Box
output_box = scrolledtext.ScrolledText(
    window,
    width=100,
    height=25,
    font=("Consolas", 10)
)

output_box.pack(pady=10)

# Store news data
news_data = []

# Scraping Function
def scrape_news():

    output_box.delete(1.0, tk.END)

    # Clear old data
    news_data.clear()

    url = url_entry.get()
    keyword = keyword_entry.get().lower()

    # Validation
    if url == "":
        messagebox.showerror("Error", "Please enter website URL")
        return

    if keyword == "":
        messagebox.showerror("Error", "Please enter keyword")
        return

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    current_time = datetime.now()

    output_box.insert(
        tk.END,
        f"Scraping started at: {current_time}\n"
    )

    output_box.insert(
        tk.END,
        "=" * 100 + "\n\n"
    )

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        # Status Handling
        if response.status_code == 200:

            output_box.insert(
                tk.END,
                "Website connected successfully!\n\n"
            )

            logging.info("Website connected successfully")

        elif response.status_code == 404:

            output_box.insert(
                tk.END,
                "Website not found!\n"
            )

            logging.error("404 Website Not Found")

            return

        else:

            output_box.insert(
                tk.END,
                f"Failed with status code: {response.status_code}\n"
            )

            logging.error(
                f"Failed with status code {response.status_code}"
            )

            return

        # Parse HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Different selectors for websites
        if "ndtv" in url:

            headlines = soup.find_all(["h2", "h3"])

        elif "bbc" in url:

            headlines = soup.find_all("h2")

        elif "reuters" in url:

            headlines = soup.find_all("h3")

        elif "techcrunch" in url:

            headlines = soup.find_all("h3")

        elif "ycombinator" in url:

            headlines = soup.select(".titleline > a")

        else:

            headlines = soup.find_all("a")

        found = False

        # Loop through headlines
        for headline in headlines:

            title = headline.get_text(strip=True)

            # Skip empty titles
            if not title:
                continue

            # Keyword filtering
            if keyword in title.lower():

                found = True

                # Category Detection
                category = "General"

                if (
                    "ai" in title.lower()
                    or "technology" in title.lower()
                    or "software" in title.lower()
                ):

                    category = "Technology"

                elif (
                    "cricket" in title.lower()
                    or "football" in title.lower()
                    or "ipl" in title.lower()
                ):

                    category = "Sports"

                elif (
                    "election" in title.lower()
                    or "government" in title.lower()
                    or "modi" in title.lower()
                ):

                    category = "Politics"

                elif (
                    "movie" in title.lower()
                    or "music" in title.lower()
                    or "bollywood" in title.lower()
                ):

                    category = "Entertainment"

                # Display Output
                output_box.insert(
                    tk.END,
                    f"Title: {title}\n"
                )

                output_box.insert(
                    tk.END,
                    f"Category: {category}\n"
                )

                output_box.insert(
                    tk.END,
                    "-" * 100 + "\n"
                )

                # Save data
                news_data.append({
                    "title": title,
                    "category": category,
                    "scraped_time": str(current_time)
                })

                logging.info(f"Headline scraped: {title}")

                time.sleep(0.5)

        # If no headlines found
        if not found:

            output_box.insert(
                tk.END,
                "No matching headlines found.\n\n"
            )

            output_box.insert(
                tk.END,
                "Try keywords like:\n"
            )

            output_box.insert(
                tk.END,
                "AI\nIndia\ncricket\nModi\ntechnology\n"
            )

        # Save CSV
        with open(
            "news.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Title",
                "Category",
                "Scraped Time"
            ])

            for item in news_data:

                writer.writerow([
                    item["title"],
                    item["category"],
                    item["scraped_time"]
                ])

        logging.info("CSV file saved")

        # Save JSON
        with open(
            "news.json",
            "w",
            encoding="utf-8"
        ) as json_file:

            json.dump(
                news_data,
                json_file,
                indent=4
            )

        logging.info("JSON file saved")

        # Save Excel
        df = pd.DataFrame(news_data)

        df.to_excel(
            "news.xlsx",
            index=False
        )

        logging.info("Excel file saved")

        output_box.insert(
            tk.END,
            "\nFiles Saved Successfully:\n"
        )

        output_box.insert(
            tk.END,
            "news.csv\n"
        )

        output_box.insert(
            tk.END,
            "news.json\n"
        )

        output_box.insert(
            tk.END,
            "news.xlsx\n"
        )

        output_box.insert(
            tk.END,
            "scraper.log\n"
        )

    except requests.exceptions.Timeout:

        output_box.insert(
            tk.END,
            "Request timed out!\n"
        )

        logging.error("Request Timeout")

    except requests.exceptions.ConnectionError:

        output_box.insert(
            tk.END,
            "Connection error occurred!\n"
        )

        logging.error("Connection Error")

    except Exception as e:

        output_box.insert(
            tk.END,
            f"Error: {e}\n"
        )

        logging.error(f"Unexpected Error: {e}")

# Scrape Button
scrape_button = tk.Button(
    window,
    text="Scrape News",
    command=scrape_news,
    bg="lightblue",
    fg="black",
    font=("Arial", 14, "bold"),
    width=20
)

scrape_button.pack(pady=15)

# Run Application
window.mainloop()