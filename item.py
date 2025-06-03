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
        self.stattrack = stattrack
        if username == None:
            username = "."
        self.username = username.upper()
        self.date = date
        if date is None:
            self.date = datetime.datetime.now()

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
        if self.type == "CASE" or self.type == "KEY":
            return self.__get_case_key_string()
        elif "KNIFE" in self.type or self.type == "GLOVE":
            return self.__get_glove_kinfe_string()
        else:
            return self.__get_weapon_string()

    def __get_glove_kinfe_string(self):
        return f"{STAR} {self.__get_weapon_string()}"

    def __get_weapon_string(self):
        buffer = ""
        if self.stattrack:
            buffer += f"{STATTRACK} "
        buffer +=f"{self.type} | {self.name} ({self.get_condition_str()})"#TODO change condition TEXT
        return buffer

    def __get_case_key_string(self):
        buffer = ""
        buffer += f"{self.name} {self.type}"
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