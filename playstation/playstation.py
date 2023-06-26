from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from helpers.games import *

url = "https://store.playstation.com/en-ca/category/dc464929-edee-48a5-bcd3-1e6f5250ae80/1?PS5=targetPlatforms" \
      "&FULL_GAME=storeDisplayClassification"
site = {"site": "playstation"}
image_link_xpath = "//img[@data-qa='ems-sdk-grid#productTile0#game-art#image#image']"
sort_icon_xpath = "//button[@data-qa='ems-sdk-grid-sort-filter-btn-mobile']"
sort_option_xpath = "//button[@data-qa='ems-sdk-collapsible-menu--sort']"
best_selling_xpath = "//div[@class='ems-sdk-collapsible-menu__item-list']/span[1]/label[2]"
games_ul_xpath = "//ul[@class='psw-grid-list psw-l-grid']"
game_image_xpath = "//div[contains(@class, 'psw-game-art__container')]/span[2]/img[1]"
game_title_xpath = "//span[contains(@data-qa, 'product-name')]"
game_price_xpath = "//s[contains(@data-qa, 'price-strikethrough')]"
game_sale_price_xpath = "//span[contains(@data-qa, 'display-price')]"


def cleanup_games(game_titles, game_images, game_prices, game_sale_prices):
    check_count([game_titles, game_images, game_sale_prices])

    # Remove free and included titles
    games_to_clean = []

    for index, price in enumerate(game_sale_prices):
        if price.text == "Free" or price.text == "Included":
            games_to_clean.append(index)

    if games_to_clean:
        for index in games_to_clean:
            game_images.pop(index)
            game_titles.pop(index)
            game_sale_prices.pop(index)

    check_count([game_prices, game_sale_prices])

    for i in range(len(game_titles)):
        game_titles[i] = game_titles[i].text
        game_images[i] = game_images[i].get_attribute("src").split("?", 1)[0]
        game_prices[i] = game_prices[i].text
        game_sale_prices[i] = game_sale_prices[i].text


def scrape_playstation(webdriver, db):
    try:
        webdriver.get(url)
        # Click the best-selling filter option
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, sort_icon_xpath))
        ).click()
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, sort_option_xpath))
        ).click()
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, best_selling_xpath))
        ).click()
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, sort_icon_xpath))
        ).click()
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, image_link_xpath))
        )

        games_ul = webdriver.find_element(By.XPATH, games_ul_xpath)
        game_titles = games_ul.find_elements(By.XPATH, game_title_xpath)
        game_images = games_ul.find_elements(By.XPATH, game_image_xpath)
        game_prices = games_ul.find_elements(By.XPATH, game_price_xpath)
        game_sale_prices = games_ul.find_elements(By.XPATH, game_sale_price_xpath)

        cleanup_games(game_titles, game_images, game_prices, game_sale_prices)
        games = package_games(game_titles, game_images, game_prices, game_sale_prices)
        db.replace_one(site, {**site, "games": games}, True)

        webdriver.close()
        print('Playstation success')

    except TimeoutException:
        print("Playstation timed out")
