from item import *
import sqlite3
from constants import *

class Inventory_List:
    def __init__(self):
        self.sql_connection = sqlite3.connect(SQL_FILE_NAME)
        self.sql_inventory = self.sql_connection.cursor()
        self.create_table()

    def create_table(self):
        self.__create_inventory_table()
        self.__create_history_table()
        
    def __create_inventory_table(self):
        query = f"SELECT name FROM sqlite_master WHERE type='table' and name='{SQL_INVENTORY_TABLE_NAME}';"
        listOfTables = self.sql_inventory.execute(query).fetchall()
        if listOfTables != []:
            print("Existing inventory detected")
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

    def __create_history_table(self):
        query = f"SELECT name FROM sqlite_master WHERE type='table' and name='{SQL_PURCHASE_HISTORY_TABLE_NAME}';"
        list_of_tables = self.sql_inventory.execute(query).fetchall()
        if list_of_tables != []:
            print("Existing history detected")
            return
        query = f'''CREATE TABLE {SQL_PURCHASE_HISTORY_TABLE_NAME}(
        {SQL_PURCHASE_HISTORY_ID} {SQL_PURCHASE_HISTORY_ID_VAR} PRIMARY KEY,
        {SQL_PURCHASE_HISTORY_PRICE} {SQL_PURCHASE_HISTORY_PRICE_VAR},
        {SQL_PURCHASE_HISTORY_DATE} {SQL_PURCHASE_HISTORY_DATE_VAR},
        {SQL_PURCHASE_HISTORY_FOREIGN_INVENTORY_ID} {SQL_INVENTORY_INDEX_VAR},
        FOREIGN KEY ({SQL_PURCHASE_HISTORY_FOREIGN_INVENTORY_ID})
        REFERENCES {SQL_INVENTORY_TABLE_NAME}({SQL_INVENTORY_INDEX})
        );'''
        self.sql_inventory.execute(query).fetchall()
        
    def add_item(self, item:Item):
        query = f'''INSERT INTO {SQL_INVENTORY_TABLE_NAME}({SQL_INVENTORY_ITEM_TYPE}, {SQL_INVENTORY_ITEM_NAME}, {SQL_INVENTORY_CONDITION}, {SQL_INVENTORY_STATTRACK}, {SQL_INVENTORY_USERNAME})
        VALUES('{item.type}', '{item.name}', '{item.get_condition_str()}', {item.stattrack}, '{item.username}');
'''
        self.sql_inventory.execute(query)
        self.sql_connection.commit()
        
        self.add_history_to_item(item)

    def add_history_to_item(self, item:Item):
        item_id = self.__get_inventory_id(item)
        for x in range(item.quantity):
            query = f'''INSERT INTO {SQL_PURCHASE_HISTORY_TABLE_NAME}({SQL_PURCHASE_HISTORY_PRICE}, {SQL_PURCHASE_HISTORY_DATE}, {SQL_PURCHASE_HISTORY_FOREIGN_INVENTORY_ID})
            VALUES('{item.bought_price}', '{item.date}', '{item_id}');
            '''
            self.sql_inventory.execute(query)
            self.sql_connection.commit()

    def __does_inventory_entry_exist(self, item):
        ##check if item is already in inventory table return true if true. alse otherwise
        #add this to add_item to avoid duplicate entries, still follow through with history entiry
        pass

    def display_table_columns(self):
        query = f"PRAGMA TABLE_INFO('{SQL_INVENTORY_TABLE_NAME}');"
        buffer = self.sql_inventory.execute(query).fetchall()
        print(buffer)

    def display_whole_inventory(self):
        query = f"SELECT * FROM {SQL_INVENTORY_TABLE_NAME}"
        buffer = self.sql_inventory.execute(query).fetchall()
        print(buffer)

    def display_whole_history(self):
        query = f"SELECT * FROM {SQL_PURCHASE_HISTORY_TABLE_NAME}"
        buffer = self.sql_inventory.execute(query).fetchall()
        print(buffer)

    def __get_inventory_id(self, item:Item):
        query = f'''SELECT {SQL_INVENTORY_INDEX} FROM {SQL_INVENTORY_TABLE_NAME}
        WHERE {SQL_INVENTORY_USERNAME} == '{item.username}' AND 
        {SQL_INVENTORY_ITEM_TYPE} == '{item.type}' AND
        {SQL_INVENTORY_ITEM_NAME} == '{item.name}' AND
        {SQL_INVENTORY_CONDITION} == '{item.get_condition_str()}' AND
        {SQL_INVENTORY_STATTRACK} == {item.stattrack};'''
        buffer = self.sql_inventory.execute(query).fetchall()
        if buffer == []:
            raise Exception("item currently does not exist in inventory.db")
        return buffer[0][0]

    def import_from_google_sheets(self):
        ##scrape from a provided link all of the entries. add them to the DB,
        pass
