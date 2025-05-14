import unittest

from item import *

class TestTextNode(unittest.TestCase):
    def test_full_name(self):
        item = Item("Ak-47", "teST", 1)
        self.assertEqual(item.get_full_item_name(), "AK-47 | TEST")

    def test_full_name_stattrack(self):
        item = Item("Ak-47", "teST", 1, stattrack=True)
        self.assertEqual(item.get_full_item_name(), "Stattrack AK-47 | TEST")

if __name__ == "__main__":
    unittest.main()