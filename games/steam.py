from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from helpers.games import *

url = "https://store.steampowered.com/specials/?flavor=contenthub_newandtrending"
site = {"site": "steam"}
games_div_xpath = "//div[@class='facetedbrowse_FacetedBrowseItems_NO-IP']"
game_image_xpath = games_div_xpath + "//div[contains(@class, 'salepreviewwidgets_HeaderCapsuleImageContainer_" \
                                     "')]//img[contains(@class, 'salepreviewwidgets_CapsuleImage_')]"
game_title_xpath = games_div_xpath + "//div[contains(@class, 'salepreviewwidgets_StoreSaleWidgetTitle_')]"
game_price_xpath = games_div_xpath + "//div[contains(@class, 'salepreviewwidgets_StoreOriginalPrice_')]"
game_sale_price_xpath = games_div_xpath + "//div[contains(@class, 'salepreviewwidgets_StoreSalePriceBox_')]"


def cleanup_games(game_titles, game_images, game_prices, game_sale_prices):
    titles_to_keep = []
    for index, title in enumerate(game_titles):
        if title.text:
            titles_to_keep.append(title.text)

    game_titles[:] = list(titles_to_keep)
    del game_images[1::2]
    check_count([game_titles, game_images, game_prices, game_sale_prices])

    for i in range(len(game_titles)):
        game_images[i] = game_images[i].get_attribute("src").split("?", 1)[0]
        game_prices[i] = f"${game_prices[i].text.replace('C$ ', '')}"
        game_sale_prices[i] = f"${game_sale_prices[i].text.replace('C$ ', '')}"


def scrape_steam(webdriver, db):
    try:
        webdriver.get(url)
        WebDriverWait(webdriver, 5).until(
            ec.visibility_of_element_located((By.XPATH, game_image_xpath))
        )

        games_div = webdriver.find_element(By.XPATH, games_div_xpath)
        game_titles = games_div.find_elements(By.XPATH, game_title_xpath)
        game_images = games_div.find_elements(By.XPATH, game_image_xpath)
        game_prices = games_div.find_elements(By.XPATH, game_price_xpath)
        game_sale_prices = games_div.find_elements(By.XPATH, game_sale_price_xpath)

        cleanup_games(game_titles, game_images, game_prices, game_sale_prices)
        games = package_games(game_titles, game_images, game_prices, game_sale_prices)
        db.replace_one(site, {**site, "games": games}, True)

        webdriver.close()
        print('Steam success')

    except TimeoutException:
        print("Steam timed out")
