from web_director.abc import MarketPlaceABC


class CustomMarketPlace(MarketPlaceABC.MarketPlaceABC):

    def __init__(self, name):
        self.name = name
        self.root_page_url = ""
        self.general_start_page_url = ""
        self.general_item_url = ""
        self._sale_item_name_regex = {}
        self._seller_name_regex = {}
        self._seller_description_regex = {}
        self._seller_url_regex = {}
        self._seller_block_regex = {}
        self._price_regex = {}
        self._date_regex = {}
        self._attributes_regex = {}

    def get_root_page(self):
        return self.root_page_url

    def get_general_start_page_url(self):
        return self.general_start_page_url

    def get_general_page_url(self):
        return self.general_item_url

    def sale_item_name_regex(self):
        return self._sale_item_name_regex

    def seller_name_regex(self):
        return self._seller_name_regex

    def seller_description_regex(self):
        return self._seller_description_regex

    def seller_url_regex(self):
        return self._seller_url_regex

    def seller_block_regex(self):
        return self._seller_block_regex

    def price_regex(self):
        return self._price_regex

    def date_regex(self):
        return self._date_regex

    def attributes_regex(self):
        return self._attributes_regex

