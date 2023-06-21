import sys

from helpers.db import load_database
from helpers.webdriver import web_driver
from playstation.playstation import scrape_playstation

available_args = [
    "playstation",
    "nintendo"
]

if __name__ == "__main__":
    webdriver = web_driver()
    webdriver.implicitly_wait(5)
    db = load_database()

    site = sys.argv[1] if sys.argv[1:] else ""

    if site == available_args[0]:
        scrape_playstation(webdriver, db)
    else:
        print("Usage: scrape.py playstation")
        print("Available args:", ", ".join(map(str, available_args)))

    webdriver.quit()
