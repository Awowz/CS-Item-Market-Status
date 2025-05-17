from item import *
import sqlite3
from constants import *

class Inventory_List:
    def __init__(self):
        self.sql_connection = sqlite3.connect(SQL_FILE_NAME)
        self.sql_inventory = self.sql_connection.cursor()

    def create_table(self):
        query = f"SELECT name FROM sqlite_master WHERE type='table' and name='{SQL_INVENTORY_TABLE_NAME}';"
        listOfTables = self.sql_inventory.execute(query).fetchall()
        if listOfTables != []:
            return
        #query = f"CREATE TABLE {SQL_INVENTORY_TABLE_NAME}({SQL_INVENTORY_INDEX} int, );"
        

 
        

    def import_from_google_sheets(self):
        pass
