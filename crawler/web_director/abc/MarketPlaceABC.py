from abc import ABC, abstractmethod


class MarketPlaceABC(ABC):

    @abstractmethod
    def get_root_page(self):
        pass

    @abstractmethod
    def get_general_start_page_url(self):
        pass

    @abstractmethod
    def get_general_page_url(self):
        pass

    @abstractmethod
    def sale_item_name_regex(self):
        pass

    @abstractmethod
    def seller_name_regex(self):
        pass

    @abstractmethod
    def seller_description_regex(self):
        pass

    @abstractmethod
    def seller_block_regex(self):
        pass

    @abstractmethod
    def seller_url_regex(self):
        pass

    @abstractmethod
    def price_regex(self):
        pass

    @abstractmethod
    def date_regex(self):
        pass

    @abstractmethod
    def attributes_regex(self):
        pass
