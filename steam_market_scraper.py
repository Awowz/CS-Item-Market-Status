from constants import *
from item import *

import requests

class Steam_Market_Scraper():
    def __init__(self):
        self.__payload = {COUNTRY_KEY:COUNTRY_VALUE, CURRENCY_KEY:CURRENCY_VALUE, APPID_KEY:COUNTER_STRIKE_APP_ID}
        pass

    def construct_url_listing(self, item:Item) ->str:
        pass

    def construct_url_search(self, item:Item) ->str:
        pass

    def __check_valid_listing(self):
        pass

    def __check_valid_search(self):
        pass

    def __generate_market_hash_payload(self, hash:str) ->dict:
        payload = self.__payload
        payload[MARKET_HASH_KEY] = hash
        return payload

    def get_item_value(self, item:Item) ->float:
        #construct listing if valid, return value.
        #else construct search, if valid return value
        #if no results. return -1
        pass

    def test(self):
        print(self.__generate_market_hash_payload("testing"))
