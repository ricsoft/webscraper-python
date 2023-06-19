from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Playstation store ps5/full game/deals
url = 'https://store.playstation.com/en-ca/category/dc464929-edee-48a5-bcd3-1e6f5250ae80/1?PS5=targetPlatforms' \
      '&FULL_GAME=storeDisplayClassification'
image_link = '//img[@data-qa="ems-sdk-grid#productTile0#game-art#image#image"]'
games_ul_xpath = '//ul[@class="psw-grid-list psw-l-grid"]'
game_image_xpath = '//div[contains(@class, "psw-game-art__container")]/span[2]/img[1]'
game_title_xpath = '//span[contains(@data-qa, "product-name")]'
game_price_xpath = '//s[contains(@data-qa, "price-strikethrough")]'
game_sale_price_xpath = '//span[contains(@data-qa, "display-price")]'


def cleanup_games(game_titles, game_images, game_sale_prices):
    # Remove free and included titles
    games_to_clean = []

    for index, price in enumerate(game_sale_prices):
        if price.text == "Free" or price.text == "Included":
            games_to_clean.append(index)

    if not games_to_clean:
        return

    for index in games_to_clean:
        game_images.pop(index)
        game_titles.pop(index)
        game_sale_prices.pop(index)


def package_games(game_titles, game_images, game_prices, game_sale_prices):
    collection = []
    count = len(game_titles)

    if len(game_images) != count or len(game_prices) != count or len(game_sale_prices) != count:
        raise Exception("Playstation count mismatch")

    for index in range(count):
        collection.append({
            "title": game_titles[index].text,
            "image": game_images[index].get_attribute("src").split("?", 1)[0],
            "price": game_prices[index].text,
            "sale_price": game_sale_prices[index].text,
        })

    print(collection)


def scrape_playstation(webdriver):
    try:
        webdriver.get(url)
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, image_link))
        )

        games_ul = webdriver.find_element(By.XPATH, games_ul_xpath)
        game_titles = games_ul.find_elements(By.XPATH, game_title_xpath)
        game_images = games_ul.find_elements(By.XPATH, game_image_xpath)
        game_prices = games_ul.find_elements(By.XPATH, game_price_xpath)
        game_sale_prices = games_ul.find_elements(By.XPATH, game_sale_price_xpath)

        cleanup_games(game_titles, game_images, game_sale_prices)
        package_games(game_titles, game_images, game_prices, game_sale_prices)

    except TimeoutException:
        print("Playstation timed out")
