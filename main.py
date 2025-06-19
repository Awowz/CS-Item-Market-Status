from inventory_lsit import *
from steam_market_scraper import *
import os
#nnext implement REMOVE_ITEM_SELECT logic
#TODO calculate value gained from each itme, total value gained nad percentage increase for each entrie (1.00 spent 1.50 market value ->50% gain)
#TODO when editing entry if already exisitning, then just add its history to existin item hirstory
#TODO pull from db all into an item array, then get prices for each of them. dont throw away this data, keep it pooled so that if more request are sent in the same session its not spamming server
#TODO error catch when user doesnt provide an interger int(users_inpute)
class System_State(Enum):
    MAIN_MENU = 0
    ADD_ITEM_OVERVIEW = 1
    INVENTORY_ITEM_OVERVIEW = 2
    VIEW_BUFFER_OUTPUT = 3
    DISPLAY_USERS_INTO_INVENTORY = 4
    DISPLAY_PRICE_OPTIONS = 5
    VIEW_BUFFER_INTO_ITEM_SPECIFIC_VALUE = 6
    VIEW_BUFFER_INTO_VIEW_PLAYERS = 7
    VIEW_BUFFER_WHOLE_INVENTORY = 8
    REMOVE_ITEM_PROFILE_SELECT = 9
    REMOVE_ITEM_SELECT = 10
    REMOVE_ITEM_QUATITY = 11

class App_Container():
    def __init__(self):
        self.error = ""
        self.inventory = Inventory_List()
        self.buffer_output = ""
        self.scraper = Steam_Market_Scraper()
        self.buffer_input = None

    
        

def display(current_state, users_input, app_container):
    if app_container.error != "":
        print(f"{TEXT_WARNING}ERROR MSG:{app_container.error}{TEXT_ENDC}")
    match current_state:

        case System_State.MAIN_MENU:
            print('''Options
1. Add / Import / Export items to inventory.
2. Inventory Item Overview
3. Profits''')
            
        case System_State.ADD_ITEM_OVERVIEW:
            print('''Options
1. Google sheets
2. Add item manually
3. Edit Item
4. Remove Item''')
            
        case System_State.INVENTORY_ITEM_OVERVIEW:
            print('''Options
1. Get all items
2. Get items from user
3. Get Purchase history from item''')

        case System_State.VIEW_BUFFER_OUTPUT:
            print(app_container.buffer_output)
        case System_State.REMOVE_ITEM_SELECT:
            buff = ""
            for x in range(len(app_container.buffer_output)):
                buff += f"{x}: {app_container.buffer_output[x]} {app_container.buffer_output[x].bought_price}\n"
            print(buff)
        case System_State.DISPLAY_USERS_INTO_INVENTORY:
            print(display_user_profiles(app_container))
        case System_State.REMOVE_ITEM_PROFILE_SELECT:
            print(display_user_profiles(app_container))
        case System_State.VIEW_BUFFER_INTO_VIEW_PLAYERS:
            print(display_user_profiles(app_container))

        case System_State.DISPLAY_PRICE_OPTIONS:
            print('''Options
1. Display all profits
2. Display User Profits
3. Display Specific Item Profit''')
            
        case System_State.VIEW_BUFFER_INTO_ITEM_SPECIFIC_VALUE:
            inv = app_container.inventory.get_whole_inventory()
            buffer = ""
            for x in range(len(inv)):
                buffer += f"{x}: {inv[x]}\n"
            print(buffer)

        case System_State.VIEW_BUFFER_WHOLE_INVENTORY:
            items = app_container.inventory.get_whole_inventory()
            buffer = ""
            for x in items:
                buffer += f"{x}\n"
            print(buffer)

        case System_State.REMOVE_ITEM_QUATITY:
            print(f"Enter quantity to remove of {app_container.buffer_output}")


        case _:
            raise Exception("unkown state condition raised")
    print('q to quit    |   x back to main menu' )
        


def reaction(current_state, users_input, app_container):
    if users_input == 'q':
        exit()
    elif users_input == 'x':
        return System_State.MAIN_MENU
    
    match current_state:

        case System_State.MAIN_MENU:
            if users_input == '1':
                print("sss")
                return System_State.ADD_ITEM_OVERVIEW
            elif users_input == '2':
                return System_State.INVENTORY_ITEM_OVERVIEW
            elif users_input == '3':
                return System_State.DISPLAY_PRICE_OPTIONS

        case System_State.ADD_ITEM_OVERVIEW:
            if users_input == '1':
                pass
            elif users_input == '2':
                create_item(app_container)
                return System_State.ADD_ITEM_OVERVIEW
            elif users_input == '3':
                pass
            elif users_input == '4':
                return System_State.REMOVE_ITEM_PROFILE_SELECT
            
        case System_State.INVENTORY_ITEM_OVERVIEW:
            if users_input =='1':
                return System_State.VIEW_BUFFER_WHOLE_INVENTORY
            elif users_input == '2':
                return System_State.DISPLAY_USERS_INTO_INVENTORY
            elif users_input == '3':
                pass

        case System_State.VIEW_BUFFER_OUTPUT:
            pass
        case System_State.VIEW_BUFFER_WHOLE_INVENTORY:
            pass

        case System_State.DISPLAY_USERS_INTO_INVENTORY:
            
            input_int = int(users_input)
            user_list = app_container.inventory.get_usernames_in_inventory()
            if input_int >= 0 and input_int < len(user_list):
                app_container.buffer_output = app_container.inventory.get_users_inventory(user_list[input_int])
                return System_State.VIEW_BUFFER_OUTPUT
        
        case System_State.DISPLAY_PRICE_OPTIONS:
            if users_input == '1':
                pass
            elif users_input == '2':
                return System_State.VIEW_BUFFER_INTO_VIEW_PLAYERS
            elif users_input == '3':
                return System_State.VIEW_BUFFER_INTO_ITEM_SPECIFIC_VALUE
            
        case System_State.VIEW_BUFFER_INTO_ITEM_SPECIFIC_VALUE:
            try:
                input_int = int(users_input)
                item_list = app_container.inventory.get_whole_inventory()
                if input_int >= 0 and input_int < len(item_list):
                    app_container.buffer_output = get_str_item_value_output(app_container, [item_list[input_int]])
                    return System_State.VIEW_BUFFER_OUTPUT
            except ValueError as e:
                app_container.error = "Invalid input, please try again"
            except Exception as e:
                app_container.error = e

        case System_State.VIEW_BUFFER_INTO_VIEW_PLAYERS:
            try:
                input_int = int(users_input)
                user_list = app_container.inventory.get_usernames_in_inventory()
                if input_int >= 0 and input_int < len(user_list):
                    items_from_user = app_container.inventory.get_users_inventory(user_list[input_int])
                    app_container.buffer_output = get_str_item_value_output(app_container, items_from_user)
                    return System_State.VIEW_BUFFER_OUTPUT
            except ValueError as e:
                app_container.error = "Invalid input, please try again"
            except Exception as e:
                app_container.error = e

        case System_State.REMOVE_ITEM_PROFILE_SELECT:
            app_container.buffer_input = None
            try:
                input_int = int(users_input)
                user_list = app_container.inventory.get_usernames_in_inventory()
                if input_int >= 0 and input_int < len(user_list):
                    app_container.buffer_output = app_container.inventory.get_users_inventory(user_list[input_int])
                    app_container.buffer_input = app_container.buffer_output
                    return System_State.REMOVE_ITEM_SELECT
            except ValueError as e:
                app_container.error = "Invalid input, please try again"
            except Exception as e:
                app_container.error = e

        case System_State.REMOVE_ITEM_SELECT:
            try:
                input_int = int(users_input)
                user_list = app_container.buffer_input
                if input_int >= 0 and input_int < len(user_list):
                    app_container.buffer_output = user_list[input_int]
                    app_container.buffer_input = user_list[input_int]
                    return System_State.REMOVE_ITEM_QUATITY
            except ValueError as e:
                app_container.error = "Invalid input, please try again"
            except Exception as e:
                app_container.error = e

        case System_State.REMOVE_ITEM_QUATITY:
            try:
                input_int = int(users_input)
                if input_int >= 1 and input_int < app_container.buffer_input.quantity:
                    app_container.inventory.remove_item(app_container.buffer_input, input_int)
                    return System_State.MAIN_MENU
            except ValueError as e:
                app_container.error = "Invalid input, please try again"
            except Exception as e:
                app_container.error = e

        case _:
            raise Exception("unkown state contition raised in reaction")
        
    return current_state

def clear():
    os.system('clr' if os.name == 'nt' else 'clear')

def display_user_profiles(app_container):
    all_users = app_container.inventory.get_usernames_in_inventory()
    buffer = ""
    for x in range(len(all_users)):
        buffer += f"{x}. {all_users[x]}\n"
    return buffer


def create_item(app_container):
    clear()
    print("Enter item type, for example: AK47, CASE, STICKER.....")
    user_type = input()
    print("Enter item name, for example: FOREST DDPAT, OPERATION BRAVO.....")
    user_item_name = input()
    print("is item stattrack?")
    while True:
        print("Enter either y/n:")
        temp = input().upper()
        if temp == "Y":
            user_stattrack = True
            break
        elif temp == "N":
            user_stattrack = False
            break
    print("enter the condition of the item (if applicable)")
    print("1. NONE\n2. BATTLE SCARRED\n3. WELL_WORN\n4. FIELD_TESTED\n5. MINIMAL_WEAR\n6. FACTORY_NEW")
    while True:
        print("please enter a number 1 thru 6")
        temp = input()
        try:
            temp = int(temp)
            match temp:
                case 1:
                    user_condition = Condition.NULL
                    break
                case 2:
                    user_condition = Condition.BATTLE_SCARRED
                    break
                case 3: 
                    user_condition = Condition.WELL_WORN
                    break
                case 4: 
                    user_condition = Condition.FIELD_TESTED
                    break
                case 5:
                    user_condition = Condition.MINIMAL_WEAR
                    break
                case 6:
                    user_condition = Condition.FACTORY_NEW
                    break
        except:
            pass
    print("please enter the price that you bought the item at ex: 42.93 , 0.03")
    while True:
        try:
            user_price = input()
            user_price = float(user_price)
            break
        except:
            print("invalid input, please try again")
    print("please enter the quantity of items you have bought ex: 1")
    while True:
        try:
            user_quantity = input()
            user_quantity = int(user_quantity)
            if user_quantity <= 0:
                raise Exception("zero or less than")
            break
        except:
            print("invalid input, please try again")
    print("please enter the owners name, can leave blank")
    user_name = input()
    if user_name == "":
        user_name = None
    generated_item = Item(user_type, user_item_name, user_price, user_quantity, user_condition, user_stattrack, user_name)
    app_container.inventory.add_item_and_history(generated_item)

def get_str_item_value_output(app_container, items: list[Item]):
    buffer = ""
    total_spent = 0
    total_gained = 0
    for item in items:
        item_with_history = app_container.inventory.get_accurate_items_history_from_item(item)
        item_value = app_container.scraper.get_item_value(item)
        for single_item in item_with_history:
            total_spent += single_item.bought_price * single_item.quantity
            single_item.set_market_value(item_value.market_value)
            total_gained += single_item.market_value * single_item.quantity
            buffer += f"{TEXT_UNDERLINE}{single_item.construct_string()}{TEXT_ENDC}\n---------------------------------\nCurrent Market Value: {single_item.market_value}\nBought {single_item.quantity} at {single_item.bought_price} Each\nSpent: {single_item.get_total_spent()}\nProfit: {single_item.get_total_profit()}\n\n"
        buffer += f"---------------------------------\n{TEXT_BOLD}Total Spent: {total_spent}\nTotal Market Value: {total_gained}\nTotal Profit: {total_gained - total_spent}{TEXT_ENDC}\n" 
    return buffer

def main():
    current_state = System_State.MAIN_MENU
    users_input = ""
    app_container = App_Container()
    clear()
    while True:
        display(current_state, users_input, app_container)
        users_input = input()
        app_container.error = ""
        current_state = reaction(current_state, users_input, app_container)
        clear()


main()
