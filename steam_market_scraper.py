from constants import *
from item import *

import requests

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

    def test(self):
        r = requests.get('https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20AK-47%20%7C%20Legion%20of%20Anubis%20%28Well-Worn%29?filter=AK47&cc=us')
        print(r.text)
        print("\n\n\n")