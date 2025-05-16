import unittest

from item import *

class TestTextNode(unittest.TestCase):
    def test_full_name(self):
        item = Item("Ak-47", "teST", 1)
        self.assertEqual(item.get_full_item_name(), "AK-47 | TEST")

    def test_full_name_stattrack(self):
        item = Item("Ak-47", "teST", 1, stattrack=True)
        self.assertEqual(item.get_full_item_name(), "Stattrack AK-47 | TEST")

    def test_id_full_name(self):
        item = Item("Ak-47", "teST", 1, condition=Condition.BATTLE_SCARRED, username="tester1")
        self.assertEqual(item.get_item_str_index(), "tester1 | AK-47 | TEST | BATTLE SCARRED")
        
    def test_id_full_name_no_user(self):
        item = Item("Ak-47", "teST", 1, condition=Condition.BATTLE_SCARRED)
        self.assertEqual(item.get_item_str_index(), "AK-47 | TEST | BATTLE SCARRED")

if __name__ == "__main__":
    unittest.main()