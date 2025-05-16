from item import *

class Inventory_List:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item:Item):
        item_id = item.get_item_str_index()
        if item_id in self.inventory:
            self.inventory[item_id].append(item)
        else:
            self.inventory[item_id] = [item]
