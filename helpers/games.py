def check_count(items):
    try:
        if not len(items) > 1:
            return

        count = len(items[0])

        for item in items[1:]:
            if len(item) != count:
                raise Exception("Count mismatch")

    except:
        raise Exception("Count mismatch")


def package_games(game_titles, game_images, game_prices, game_sale_prices):
    collection = []

    for index in range(len(game_titles)):
        collection.append({
            "title": game_titles[index],
            "image": game_images[index],
            "price": game_prices[index],
            "sale_price": game_sale_prices[index],
        })

    return collection
