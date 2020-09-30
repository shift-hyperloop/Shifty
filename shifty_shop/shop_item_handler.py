import os

import requests

from shop_item import ShopItem

class ShopItemHandler:

    def __init__(self):
        self.endpoint = os.environ.get('SHOP_ITEM_ENDPOINT')

    def get_all_items(self):
        shop_items = set()
        url = os.path.join(self.endpoint, 'all_items')
        try:
            result = requests.get(url=url).json()
            for item in result:
                shop_item = ShopItem()
                shop_item.id = item['uuid']
                shop_item.name = item['name']
                shop_item.price = item['price']
                shop_item.image_url = item['image_url']
                shop_items.add(shop_item)

        except Exception as e:
            print('Something went wrong!')
            # TODO: Handle in some way
        return shop_items