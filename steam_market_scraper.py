from constants import *
from item import *
from bs4 import BeautifulSoup

import requests

class Steam_Market_Scraper():
    def __init__(self):
        self.__payload = {COUNTRY_KEY:COUNTRY_VALUE, CURRENCY_KEY:CURRENCY_VALUE, APPID_KEY:COUNTER_STRIKE_APP_ID}
        self.__search_payload = {START_KEY:START_VALUE, COUNT_KEY:COUNT_VALUE,LANGUAGE_KEY:LANGUAGE_VALUE,CURRENCY_KEY:CURRENCY_VALUE,APPID_KEY:COUNTER_STRIKE_APP_ID}
        #?start=0&count=1&l=english&currency=1&appid=730&q=slate
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
        if STEAM_PRICE_KEY in response:
            return response
        else:
            return None

    def __retrieve_market_value(self, item:Item):
        response = self.__check_valid_listing(item)
        if response == None:
            return None
        return response[STEAM_PRICE_KEY]

    def __search_for_possible_name(self, r:requests.Response) -> str:
        soup = BeautifulSoup(r.content, 'html.parser')
        val = soup.select_one("#result_0_name")
        return val.text

    def __search_for_price(self, r:requests.Response):
        soup = BeautifulSoup(r.content, 'html.parser')
        val = soup.select_one(".sale_price")
        return val.text

    def __generate_market_hash_payload(self, hash:str) ->dict:
        payload = self.__payload
        payload[MARKET_HASH_KEY] = hash
        return payload
    
    def __generate_query_payload(self, query:str) ->dict:
        payload = self.__search_payload
        payload[QUERY_SEARCH_KEY] = query
        return payload

    def get_item_value(self, item:Item) ->Item:
        item_price = self.__retrieve_market_value(item)
        if item_price == None:
            payload = self.__generate_query_payload(item.construct_string())
            r = requests.get(STEAM_MARKET_SEARCH_URL, params=payload)
            possible_item_name = self.__search_for_possible_name(r)
            item_price = self.__search_for_price(r)
            print(f"could not find item {item.construct_string()}. search results returned: {possible_item_name}\nupdating entry")
            #todo: update item fields into no object
        #set price in new bject, return object.
        print(item_price)
        pass

    def test(self):
        item = Item("Aug", "StoRm", 1, condition=Condition.FACTORY_NEW, username="tester1")
        print(item.construct_string())
        self.get_item_value(item)
        #r = requests.get('https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20AK-47%20%7C%20Legion%20of%20Anubis%20%28Well-Worn%29?filter=AK47&cc=us')
        #print(r.text)
        #print("\n\n\n")

        #https://steamcommunity.com/market/priceoverview/?country=US&currency=3&appid=730&market_hash_name=AWP%20|%20Electric%20Hive%20(Factory%20New)

        #https://stackoverflow.com/questions/22616644/steam-market-currency-and-xml-format