import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

load_dotenv()
CHROME_BINARY_LOCATION = os.getenv("CHROME_BINARY_LOCATION")

service = Service("./drivers/chromedriver")
options = webdriver.ChromeOptions()
options.binary_location = CHROME_BINARY_LOCATION
driver = webdriver.Chrome(service=service, options=options)

if __name__ == "__main__":
    driver.get("https://www.python.org")
    print(driver.title)
    driver.quit()
