import unittest

from item import *
from inventory_lsit import Inventory_List

class TestTextNode(unittest.TestCase):
    def test_inventory_items(self):
        item1 = Item("Ak-47", "teST", 1)
        item2 = Item("M4A1", "pi data link", 1, username="tester4")
        inv = Inventory_List()
        inv.add_item(item1)
        inv.add_item(item2)
        self.assertEqual(inv.inventory[item1.get_item_str_index()][0].name, "TEST")
        self.assertEqual(inv.inventory[item2.get_item_str_index()][0].name, "PI DATA LINK")
        

if __name__ == "__main__":
    unittest.main()