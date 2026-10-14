
import requests
import csv
import time
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

url = "https://quotes.toscrape.com/"
user_agent = "StudentWebScraper/1.0"

# Check robots.txt
parsed_url = urlparse(url)
robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

robots = RobotFileParser()
robots.set_url(robots_url)

try:
    robots.read()

    if not robots.can_fetch(user_agent, url):
        print("Scraping is not allowed for this URL.")
    else:
        headers = {"User-Agent": user_agent}

        # Fetch the webpage
        response = requests.get(
            url, headers=headers, timeout=10
        )
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract entries
        entries = soup.find_all("span", class_="text")

        # Save entries to CSV
        with open(
            "headlines.csv", "w",
            newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(["Headline"])

            for entry in entries:
                writer.writerow([entry.get_text(strip=True)])

        print(f"Saved {len(entries)} entries to headlines.csv")
        time.sleep(2)

except requests.RequestException as error:
    print("Request failed:", error)
except Exception as error:
    print("An error occurred:", error)
