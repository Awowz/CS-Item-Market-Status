from item import *
import sqlite3
from constants import *

class Inventory_List:
    def __init__(self):
        self.sql_connection = sqlite3.connect(SQL_FILE_NAME)
        self.sql_inventory = self.sql_connection.cursor()
        self.create_table()

    def create_table(self):
        query = f"SELECT name FROM sqlite_master WHERE type='table' and name='{SQL_INVENTORY_TABLE_NAME}';"
        listOfTables = self.sql_inventory.execute(query).fetchall()
        if listOfTables != []:
            print("table exists")
            return
        query = f'''CREATE TABLE {SQL_INVENTORY_TABLE_NAME}
        (
        {SQL_INVENTORY_INDEX} {SQL_INVENTORY_INDEX_VAR} PRIMARY KEY,
        {SQL_INVENTORY_ITEM_TYPE} {SQL_INVENTORY_ITEM_TYPE_VAR},
        {SQL_INVENTORY_ITEM_NAME} {SQL_INVENTORY_ITEM_NAME_VAR},
        {SQL_INVENTORY_CONDITION} {SQL_INVENTORY_CONDITION_VAR},
        {SQL_INVENTORY_STATTRACK} {SQL_INVENTORY_STATTRACK_VAR},
        {SQL_INVENTORY_USERNAME} {SQL_INVENTORY_USERNAME_VAR}        
        );'''
        self.sql_inventory.execute(query).fetchall()
        
    def add_item(self, item:Item):
        query = f'''INSERT INTO {SQL_INVENTORY_TABLE_NAME}({SQL_INVENTORY_ITEM_TYPE}, {SQL_INVENTORY_ITEM_NAME}, {SQL_INVENTORY_CONDITION}, {SQL_INVENTORY_STATTRACK}, {SQL_INVENTORY_USERNAME})
        VALUES('{item.type}', '{item.name}', '{item.condition}', {item.stattrack}, '{item.username}');
'''
        self.sql_inventory.execute(query)
        self.sql_connection.commit()
        

    def display_table_columns(self):
        query = f"PRAGMA TABLE_INFO('{SQL_INVENTORY_TABLE_NAME}');"
        buffer = self.sql_inventory.execute(query).fetchall()
        print(buffer)

    def display_whole_inventory(self):
        query = f"SELECT * FROM {SQL_INVENTORY_TABLE_NAME}"
        buffer = self.sql_inventory.execute(query).fetchall()
        print(buffer)


    def import_from_google_sheets(self):
        pass
