from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from helpers.games import *

url = "https://www.nintendo.com/store/games/best-sellers/"
site = {"site": "nintendo"}
deals_option_xpath = "//label[@for='deals-35']"
platform_dropdown_xpath = "//div[contains(@class, 'FilteredPageResultsstyles__StickyWrapper')]/div[3]"
switch_option_xpath = "//input[@name='Nintendo Switch']"
wishlist_button_xpath = "//button[contains(@class, 'WishlistButtonstyles__Heart')]"
games_div_xpath = "//div[contains(@class, 'SearchLayout__FilterResultsGrid')]"
game_title_xpath = "//div[contains(@class, 'tilestyles__TitleWrapper')]/h2[contains(@class, 'Headingstyles__Styled')]"
game_image_xpath = "//div[contains(@class, 'Imagestyles__ImageWrapper')]/img"
price_xpath = "//span[contains(@class, 'Pricestyles__MSRP')]"
sale_price_xpath = "//span[contains(@class, 'Pricestyles__SalePrice')]"


def cleanup_games(game_titles, game_images, game_prices, game_sale_prices):
    game_images.pop(0)
    check_count([game_titles, game_images, game_prices, game_sale_prices])

    for i in range(len(game_prices)):
        game_titles[i] = game_titles[i].text
        game_images[i] = game_images[i].get_attribute("src")
        game_prices[i] = f"${game_prices[i].text.split('$')[1]}"
        game_sale_prices[i] = f"${game_sale_prices[i].text.split('$')[1]}"


def scrape_nintendo(webdriver, db):
    try:
        webdriver.get(url)
        # Click deals and switch platform options
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, deals_option_xpath))
        ).click()
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, platform_dropdown_xpath))
        ).click()
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, switch_option_xpath))
        ).click()
        WebDriverWait(webdriver, 5).until(
            ec.element_to_be_clickable((By.XPATH, wishlist_button_xpath))
        )

        games_div = webdriver.find_element(By.XPATH, games_div_xpath)
        game_titles = games_div.find_elements(By.XPATH, game_title_xpath)
        game_images = games_div.find_elements(By.XPATH, game_image_xpath)
        game_prices = games_div.find_elements(By.XPATH, price_xpath)
        game_sale_prices = games_div.find_elements(By.XPATH, sale_price_xpath)

        cleanup_games(game_titles, game_images, game_prices, game_sale_prices)
        games = package_games(game_titles, game_images, game_prices, game_sale_prices)
        db.replace_one(site, {**site, "games": games}, True)

        webdriver.close()
        print('Nintendo success')

    except TimeoutException:
        print("Nintendo timed out")
