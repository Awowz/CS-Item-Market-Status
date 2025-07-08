from constants import *
from item import *
from bs4 import BeautifulSoup
import time
import re
import requests

class Steam_Market_Scraper():
    def __init__(self):
        self.__payload = {COUNTRY_KEY:COUNTRY_VALUE, CURRENCY_KEY:CURRENCY_VALUE, APPID_KEY:COUNTER_STRIKE_APP_ID}
        self.__search_payload = {START_KEY:START_VALUE, COUNT_KEY:COUNT_VALUE,LANGUAGE_KEY:LANGUAGE_VALUE,CURRENCY_KEY:CURRENCY_VALUE,APPID_KEY:COUNTER_STRIKE_APP_ID}
        self.__all_conditions = ["Battle-Scarred","Well-Worn", "Field-Tested", "Minimal Wear", "Factory New"]
        self.__stored_items_for_sessions = {}

    def __is_item_in_session(self, item:Item):
        if item.construct_string() not in self.__stored_items_for_sessions:
            return None
        suggested_item = self.__stored_items_for_sessions[item.construct_string()]
        return suggested_item
        

    def __check_valid_listing(self, item:Item):
        print(f"Checking for item \"{item.construct_string()}\" on market...")
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
        return self.__filter_currency_to_float(response[STEAM_PRICE_KEY])

    def __search_for_possible_name(self, r:requests.Response) -> str:
        soup = BeautifulSoup(r.content, 'html.parser')
        val = soup.select_one("#result_0_name")
        if val == None:
            return None
        return val.text

    def __search_for_price(self, r:requests.Response):
        soup = BeautifulSoup(r.content, 'html.parser')
        val = soup.select_one(".sale_price")
        return self.__filter_currency_to_float(val.text)

    def __generate_market_hash_payload(self, hash:str) ->dict:
        payload = self.__payload
        payload[MARKET_HASH_KEY] = hash
        return payload
    
    def __generate_query_payload(self, query:str) ->dict:
        payload = self.__search_payload
        payload[QUERY_SEARCH_KEY] = query
        return payload
    
    def __filter_out_for_name(self, text) -> tuple: ##returns (item type, item name)
        text = text.replace(f"{STAR} ", "")
        text = text.replace(f"{STATTRACK} ", "")
        for x in self.__all_conditions:
            text = text.replace(f" ({x})", "")
        if "|" in text:
            match_str = re.search("([^\\|]+) \\| (.+)", text)
            item_type = match_str.group(1)
            item_name = match_str.group(2)
            return (item_type, item_name)
        for x in CS_UNIQUE_ITEMS:
            if x in text:
                item_name = text.replace(x, "")
                return (x, item_name)
        raise Exception("item is outside of the scope of this project")
    
    def __filter_currency_to_float(self, string:str) ->float:
        match_str = re.search("[^\\d]*([\\d\\,\\.]+)[^\\d]*", string)
        raw = match_str.group(1)
        if "," in raw and "." not in raw:
            raw = raw.replace(",", ".")
        else:
            raw = raw.replace(",", "")
        try:
            value = float(raw)
            return value
        except ValueError:
            print("This currency is not suppored and could not be converted")
            return -1

    def __query_search_item(self, item:Item) -> Item:
        payload = self.__generate_query_payload(item.construct_string())
        r = requests.get(STEAM_MARKET_SEARCH_URL, params=payload)
        possible_item_name = self.__search_for_possible_name(r)
        if possible_item_name == None:
            raise Exception(f"No items have been found from item: {item.construct_string()}. please edit the item and correctly spell it")
        item_price = self.__search_for_price(r)
        if item_price == None:
            print("found an error")
            raise Exception(f"No listings have been found for item: {item.construct_string()}.\nPlease edit the item and correctly spell it, then try again...")
        print(f"{TEXT_WARNING}{item.construct_string()} could not be found{TEXT_ENDC}.\nCloses search results returned: {possible_item_name}\n")
        possible_item_correction = self.__filter_out_for_name(possible_item_name)
        temp_item = item
        temp_item.set_item_type(possible_item_correction[0])
        temp_item.set_item_name(possible_item_correction[1])
        temp_item.set_market_value(item_price)
        return temp_item


    def get_item_value(self, item:Item) ->Item:
        previous_session = self.__is_item_in_session(item)
        old_item_name_placeholder = item.construct_string()
        if previous_session != None:
            return previous_session
        print(f"Searching for item, {item.construct_string()}...\nPutting delay on request to not overwhelm servers, please wait....")
        time.sleep(STEAM_QUERY_DELAY)
        item_price = self.__retrieve_market_value(item)
        copied_item = item
        copied_item.set_market_value(item_price)
        if item_price == None:
            print(f"{TEXT_WARNING}No items found{TEXT_ENDC}.\nDoing general table search, please wait...")
            time.sleep(STEAM_QUERY_DELAY)
            copied_item = self.__query_search_item(copied_item)
        self.__stored_items_for_sessions[old_item_name_placeholder] = copied_item
        return copied_item

    def test(self):
        item = Item("aug", "stormm", 1, condition=Condition.FACTORY_NEW, username="tester1")
        new_item = self.get_item_value(item)
        print(new_item.market_value)
        print(new_item.construct_string())