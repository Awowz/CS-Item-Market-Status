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
    
    def add_item_and_history(self, item:Item):
        self.add_item(item)
        self.add_history_to_item(item)

    def add_item(self, item:Item):
        if self.__does_inventory_entry_exist(item):
            return
        query = f'''INSERT INTO {SQL_INVENTORY_TABLE_NAME}({SQL_INVENTORY_ITEM_TYPE}, {SQL_INVENTORY_ITEM_NAME}, {SQL_INVENTORY_CONDITION}, {SQL_INVENTORY_STATTRACK}, {SQL_INVENTORY_USERNAME})
        VALUES('{item.type}', '{item.name}', '{item.get_condition_str()}', {item.stattrack}, '{item.username}');
'''
        self.sql_inventory.execute(query)
        self.sql_connection.commit()
        

    def add_history_to_item(self, item:Item):
        item_id = self.__get_inventory_id(item)
        for x in range(item.quantity):
            query = f'''INSERT INTO {SQL_PURCHASE_HISTORY_TABLE_NAME}({SQL_PURCHASE_HISTORY_PRICE}, {SQL_PURCHASE_HISTORY_DATE}, {SQL_PURCHASE_HISTORY_FOREIGN_INVENTORY_ID})
            VALUES('{item.bought_price}', '{item.date}', '{item_id}');
            '''
            self.sql_inventory.execute(query)
            self.sql_connection.commit()

    def __does_inventory_entry_exist(self, item):
        try:
            self.__get_inventory_id(item)
            return True
        except Exception as e:
            print(e)
        return False

    def display_table_columns(self):
        query = f"PRAGMA TABLE_INFO('{SQL_INVENTORY_TABLE_NAME}');"
        buffer = self.sql_inventory.execute(query).fetchall()
        print(buffer)

    def __convert_inv_and_history_to_item(self, inv, hist_price, quantity = 1):    
        temp = Item(inv[1], inv[2], hist_price, quantity, inv[3], inv[4], inv[5])
        return temp
    
    def __convert_list_of_inv_to_item(self, raw_item_lst) -> list[Item]:
        buffer_items = []
        for x in raw_item_lst:
            raw_history_prices = self.__search_history_from_item_id(x[0])
            history_prices = [temp_item for t in raw_history_prices for temp_item in t]
            counted_history_price = dict((i, history_prices.count(i)) for i in history_prices)
            for y in counted_history_price.keys():
                temp = self.__convert_inv_and_history_to_item(x, y, counted_history_price[y])
                buffer_items.append(temp)
        return buffer_items


    def get_whole_inventory(self):
        query = f"SELECT * FROM {SQL_INVENTORY_TABLE_NAME}"
        buffer = self.sql_inventory.execute(query).fetchall()
        buff_list = []
        for x in buffer:
            buff_list.append(Item(x[1], x[2], 999999, self.__get_total_count_of_item(x[0]), x[3], x[4], x[5]))
        return buff_list

    def display_whole_history(self):
        query = f"SELECT * FROM {SQL_PURCHASE_HISTORY_TABLE_NAME}"
        buffer = self.sql_inventory.execute(query).fetchall()
        print(buffer)

    def display_item_history(self, item:Item):
        item_id = self.__get_inventory_id(item)
        query = f"SELECT * FROM {SQL_PURCHASE_HISTORY_TABLE_NAME} WHERE {SQL_PURCHASE_HISTORY_FOREIGN_INVENTORY_ID} == '{item_id}'"
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
    
    def __search_history_from_item_id(self, id):
        query = f'''SELECT {SQL_PURCHASE_HISTORY_PRICE} FROM {SQL_PURCHASE_HISTORY_TABLE_NAME}
        WHERE {SQL_PURCHASE_HISTORY_FOREIGN_INVENTORY_ID} == '{id}'
        '''
        buffer = self.sql_inventory.execute(query).fetchall()
        return buffer
    
    def __search_history_id_from_item_id(self, id):
        query = f'''SELECT {SQL_PURCHASE_HISTORY_ID}, {SQL_PURCHASE_HISTORY_PRICE} FROM {SQL_PURCHASE_HISTORY_TABLE_NAME}
        WHERE {SQL_PURCHASE_HISTORY_FOREIGN_INVENTORY_ID} == '{id}'
        '''
        buffer = self.sql_inventory.execute(query).fetchall()
        return buffer
    
    def get_usernames_in_inventory(self) -> list[str]:
        query = f'''SELECT {SQL_INVENTORY_USERNAME} FROM {SQL_INVENTORY_TABLE_NAME} GROUP BY {SQL_INVENTORY_USERNAME}'''
        buffer = self.sql_inventory.execute(query).fetchall()
        list_of_users = []
        for x in range(len(buffer)):
            list_of_users.append(buffer[x][0].upper())
        return list_of_users
    
    def get_users_inventory(self, username:str):
        query = f"SELECT * FROM {SQL_INVENTORY_TABLE_NAME} WHERE {SQL_INVENTORY_USERNAME} == '{username}'"
        raw_items_list = self.sql_inventory.execute(query).fetchall()
        buffer = self.__convert_list_of_inv_to_item(raw_items_list)
        return buffer
    
    def get_numb_of_item_related_history(self, item:Item):
        #sum total of history entries that are related to item id
        pass

    def get_total_spent(self, item:Item):
        #get sum of all entries related to item ID
        pass

    def get_raw_item_from_id(self, item_id):
        query = f"SELECT * FROM {SQL_INVENTORY_TABLE_NAME} WHERE {SQL_INVENTORY_INDEX} == '{item_id}'"
        raw_item = self.sql_inventory.execute(query).fetchall()
        return raw_item

    def import_from_google_sheets(self):
        ##scrape from a provided link all of the entries. add them to the DB,
        pass

    def get_accurate_items_history_from_item(self, item:Item):
        item_id = self.__get_inventory_id(item)
        raw_item = self.get_raw_item_from_id(item_id)
        return self.__convert_list_of_inv_to_item(raw_item)

    def __get_total_count_of_item(self, id):
        hist = self.__search_history_from_item_id(id)
        return len(hist)

    
    def get_history_price_of_item(self, item:Item):
        item_id = self.__get_inventory_id(item)
        output = self.__search_history_from_item_id(item_id)
        return output
    
    def __remove_history_from_id(self, history_id):
        query = f"DELETE FROM {SQL_PURCHASE_HISTORY_TABLE_NAME} WHERE {SQL_PURCHASE_HISTORY_ID} == '{history_id}'"
        self.sql_inventory.execute(query).fetchall()
        self.sql_connection.commit()

    def __delete_item_from_inventory(self, id):
        pass


    def remove_item(self, item:Item, quantity = 1):
        item_id = self.__get_inventory_id(item)
        raw_history = self.__search_history_id_from_item_id(item_id)
        count = 0
        for x in raw_history:
            if x[1] == item.bought_price:
                count += 1
                self.__remove_history_from_id(x[0])
            if count == quantity:
                break
        raw_history = self.__search_history_id_from_item_id(item_id)
        if len(raw_history) == 0:
            self.__delete_item_from_inventory(item_id)
        return



