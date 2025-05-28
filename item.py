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
    def __init__(self, type:str, name:str, bought_price:float,quanity:int=1, condition:Condition = Condition.NULL, stattrack:bool = False, username:str = ".", date:datetime = None):
        self.type = type.upper()
        self.name = name.upper()
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

    def add_quanity(self, value):
        ##add or subtrack amount, cannot be negative, or zero
        pass
    
    def get_condition_str(self):
        match self.condition:
            case Condition.NULL:
                return "NONE"
            case Condition.BATTLE_SCARRED:
                return "BATTLE_SCARRED"
            case Condition.WELL_WORN:
                return "WELL_WORN"
            case Condition.FIELD_TESTED:
                return "FIELD_TESTED"
            case Condition.MINIMAL_WEAR:
                return "MINIMAL_WEAR"
            case Condition.FACTORY_NEW:
                return "FACTORY_NEW"
            case _:
                return ""