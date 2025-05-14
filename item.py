import datetime
from enum import Enum

class Condition(Enum):
    NULL = 0
    BATTLE_SCARRED = 1
    WELL_WORN = 2
    FIELD_TESTED = 3
    MINIMAL_WEAR = 4
    FACTORY_NEW = 5


class Item:
    def __init__(self, type:str, name:str, bought_price:float,quanity:int=1, condition:Condition = Condition.NULL, stattrack:bool = False, username:str = None, date:datetime = None):
        self.type = type.lower()
        self.name = name.lower()
        self.bought_price = bought_price
        self.quantity = quanity
        self.condition = condition
        self.stattrack = stattrack
        self.username = username
        self.date = date
        if date is None:
            self.date = datetime.datetime.now()

    def get_full_item_name(self):
        ##create full name: "sticker | parris 2025" or "statrack ak47 | anubis"
        pass

    def get_total_value(self):
        ##return quantity * bought price format float
        pass

    def add_quanity(self, value):
        ##add or subtrack amount, cannot be negative, or zero
        pass
    
    def get_condition(self):
        ##return string of condition, None of null
        pass