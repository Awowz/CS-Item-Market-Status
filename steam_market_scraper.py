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

    def __check_valid_listing(self, item:Item):
        payload = self.__generate_market_hash_payload(item.construct_string())
        r = requests.get(STEAM_MARKET_BASE_URL, params=payload)
        response = r.json()
        if response['success'] == False:
            raise Exception("fatal flaw, steam api failed to GET info")
        print(response['success'])
        if STEAM_PRICE_KEY in response:
            return response
        else:
            return None

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
        item = Item("Aug", "StoRM", 1, condition=Condition.FACTORY_NEW, username="tester1")
        print(item.construct_string())
        self.__check_valid_listing(item)
        #r = requests.get('https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20AK-47%20%7C%20Legion%20of%20Anubis%20%28Well-Worn%29?filter=AK47&cc=us')
        #print(r.text)
        #print("\n\n\n")

        #https://steamcommunity.com/market/priceoverview/?country=US&currency=3&appid=730&market_hash_name=AWP%20|%20Electric%20Hive%20(Factory%20New)

        #https://stackoverflow.com/questions/22616644/steam-market-currency-and-xml-format