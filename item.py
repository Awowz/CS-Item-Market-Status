import datetime
from enum import Enum
from constants import *

class Condition(Enum):
    NULL = 0
    BATTLE_SCARRED = 1
    WELL_WORN = 2
    FIELD_TESTED = 3
    MINIMAL_WEAR = 4
    FACTORY_NEW = 5


class Item:
    def __init__(self, type:str, name:str, bought_price:float,quanity:int=1, condition:Condition = Condition.NULL, stattrack:bool = False, username:str = ".", date:datetime = None):
        self.type = type.upper()
        self.name = name.title()
        self.bought_price = bought_price
        self.quantity = quanity
        self.condition = condition
        if isinstance(condition, str):
            self.condition = Item.get_condition_from_str(condition)
        self.stattrack = stattrack
        if username == None:
            username = "."
        self.username = username.upper()
        self.date = date
        if date is None:
            self.date = datetime.datetime.now()
        self.market_value = None

    def get_condition_from_str(str):
        match str:
            case "NONE":
                return Condition.NULL
            case "Battle-Scarred":
                return Condition.BATTLE_SCARRED
            case "Well-Worn":
                return Condition.WELL_WORN
            case "Field-Tested":
                return Condition.FIELD_TESTED
            case "Minimal Wear":
                return Condition.MINIMAL_WEAR
            case "Factory New":
                return Condition.FACTORY_NEW

    def get_full_item_name(self):
        ##create full name: "sticker | parris 2025" or "statrack ak47 | anubis"
        if self.stattrack:
            return f"Stattrack {self.type} | {self.name}"
        elif self.type == "CASE":
            return f"{self.name} {self.type}"
        return f"{self.type} | {self.name}"
    

    def get_item_str_index(self):
        buffer = f"{self.get_full_item_name()} | {self.get_condition_str()}"
        if self.username == None:
            return buffer
        return f"{self.username} | {buffer}"


    def get_total_value(self):
        ##return quantity * bought price format float
        pass

    def construct_string(self):
        if self.type.title() in CS_UNIQUE_ITEMS:
            return self.__get_case_key_string()
        elif "KNIFE" in self.type or self.type == "GLOVE":
            return self.__get_glove_kinfe_string()
        else:
            return self.__get_weapon_string()
        
    def construct_string_with_userID(self):
        return self.construct_string() + f": {self.username}"

    def __get_glove_kinfe_string(self):
        return f"{STAR} {self.__get_weapon_string()}"

    def __get_weapon_string(self):
        buffer = ""
        if self.stattrack:
            buffer += f"{STATTRACK} "
        if self.condition == Condition.NULL:
            buffer +=f"{self.type} | {self.name}"
        else:
            buffer +=f"{self.type} | {self.name} ({self.get_condition_str()})"
        return buffer

    def __get_case_key_string(self):
        buffer = ""
        buffer += f"{self.name} {self.type.title()}"
        return buffer


    def add_quanity(self, value):
        ##add or subtrack amount, cannot be negative, or zero
        pass
    
    def get_condition_str(self):
        match self.condition:
            case Condition.NULL:
                return "NONE"
            case Condition.BATTLE_SCARRED:
                return "Battle-Scarred"
            case Condition.WELL_WORN:
                return "Well-Worn"
            case Condition.FIELD_TESTED:
                return "Field-Tested"
            case Condition.MINIMAL_WEAR:
                return "Minimal Wear"
            case Condition.FACTORY_NEW:
                return "Factory New"
            case _:
                return ""
            
    def set_item_name(self, name:str):
        self.name = name

    def set_item_type(self, type:str):
        self.type = type

    def set_market_value(self, value):
        self.market_value = value
    
    def set_bought_price(self, value):
        self.bought_price = value

    def __str__(self):
        return self.construct_string_with_userID()
    
    def __repr__(self):
        return self.__str__()