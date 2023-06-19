import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

load_dotenv()
CHROME_BINARY_LOCATION = os.getenv("CHROME_BINARY_LOCATION")


def web_driver():
    service = Service("./drivers/chromedriver")
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_BINARY_LOCATION
    return webdriver.Chrome(service=service, options=options)
