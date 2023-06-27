import sys

from helpers.db import load_database
from helpers.webdriver import web_driver
from games.playstation import scrape_playstation
from games.nintendo import scrape_nintendo
from games.steam import scrape_steam

available_args = [
    "playstation",
    "nintendo",
    "steam"
]

if __name__ == "__main__":
    webdriver = web_driver()
    db = load_database()

    site = sys.argv[1] if sys.argv[1:] else ""

    if site == available_args[0]:
        scrape_playstation(webdriver, db)
    elif site == available_args[1]:
        scrape_nintendo(webdriver, db)
    elif site == available_args[2]:
        scrape_steam(webdriver, db)
    else:
        print("Usage: scrape.py playstation")
        print("Available args:", ", ".join(map(str, available_args)))

    webdriver.quit()
