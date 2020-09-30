from shop_item_handler import ShopItemHandler

class Shop:

    def __init__(self):
        self.shop_item_handler = ShopItemHandler()
        self.shop_items = self.shop_item_handler.get_all_items()

