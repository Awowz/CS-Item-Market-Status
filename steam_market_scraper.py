from constants import *
from item import *

class Steam_Market_Scraper():
    def __init__(self):
        pass

    def construct_url_listing(self, item:Item) ->str:
        pass

    def construct_url_search(self, item:Item) ->str:
        pass

    def __check_valid_listing(self):
        pass

    def __check_valid_search(self):
        pass

    def get_item_value(self, item:Item) ->float:
        #construct listing if valid, return value.
        #else construct search, if valid return value
        #if no results. return -1
        pass