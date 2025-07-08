from inventory_lsit import *
from steam_market_scraper import *
import os
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
    EDIT_ITEM_PROFILE_SELECT = 12
    EDIT_ITEM_SELECT = 13
    EDIT_ITEM_OPTIONS = 14
    VIEW_BUFFER_LIST_OF_ITEMS = 15

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
1. Add / Remove / Edit Items
2. Inventory Item Overview
3. Profits''')
            
        case System_State.ADD_ITEM_OVERVIEW:
            print('''Options
1. Add item manually
2. Edit Item
3. Remove Item''')
            
        case System_State.INVENTORY_ITEM_OVERVIEW:
            print('''Options
1. Get all items
2. Get items from user''')

        case System_State.VIEW_BUFFER_OUTPUT:
            print(app_container.buffer_output)

        case System_State.REMOVE_ITEM_SELECT:
            print("Please Select an item to remove:")
            print(display_items_from_buffer(app_container))
        case System_State.EDIT_ITEM_SELECT:
            print("Please Select an item to edit:")
            print(display_items_from_buffer(app_container))
        case System_State.VIEW_BUFFER_LIST_OF_ITEMS:
            print(display_items_from_buffer(app_container))

        case System_State.DISPLAY_USERS_INTO_INVENTORY:
            print("Please select a profile:")
            print(display_user_profiles(app_container))
        case System_State.REMOVE_ITEM_PROFILE_SELECT:
            print("Please select a profile that contains the item you want to remove:")
            print(display_user_profiles(app_container))
        case System_State.VIEW_BUFFER_INTO_VIEW_PLAYERS:
            print("Please select a profile:")
            print(display_user_profiles(app_container))
        case System_State.EDIT_ITEM_PROFILE_SELECT:
            print("Please select a profile that contains the item you want to edit:")
            print(display_user_profiles(app_container))

        case System_State.DISPLAY_PRICE_OPTIONS:
            print('''Options
1. Display all profits
2. Display User Profits
3. Display Specific Item Profit''')
            
        case System_State.EDIT_ITEM_OPTIONS:
            print(f'''Options for {app_container.buffer_input} {app_container.buffer_input.bought_price}
1. Edit Item Type
2. Edit Item Name
3. Edit Stattrack Bool
4. Edit Item Condition
5. Edit Item's Owner''')
            
        case System_State.VIEW_BUFFER_INTO_ITEM_SPECIFIC_VALUE:
            app_container.buffer_output = app_container.inventory.get_whole_inventory()
            buffer = display_items_no_value_from_buffer(app_container)
            print("Please Select an item:")
            print(buffer)

        case System_State.VIEW_BUFFER_WHOLE_INVENTORY:
            app_container.buffer_output = app_container.inventory.get_whole_inventory()
            buffer = display_items_no_value_from_buffer(app_container)
            print("Current items in inventory:")
            print(buffer)

        case System_State.REMOVE_ITEM_QUATITY:
            print(f"Please enter the quantity you want to remove of item:\n{TEXT_BOLD}{app_container.buffer_output}{TEXT_ENDC}")


        case _:
            raise Exception("unkown state condition raised")
    print('q to quit    |   x back to main menu' )
        


def reaction(current_state, users_input, app_container):
    if users_input.lower() == 'q':
        app_container.inventory.close()
        exit()
    elif users_input.lower() == 'x':
        return System_State.MAIN_MENU
    
    match current_state:

        case System_State.MAIN_MENU:
            if users_input == '1':
                return System_State.ADD_ITEM_OVERVIEW
            elif users_input == '2':
                return System_State.INVENTORY_ITEM_OVERVIEW
            elif users_input == '3':
                return System_State.DISPLAY_PRICE_OPTIONS

        case System_State.ADD_ITEM_OVERVIEW:
            if users_input == '1':
                app_container.buffer_output = None
                create_item(app_container)
                if app_container.buffer_output == None:
                    return System_State.ADD_ITEM_OVERVIEW
                return System_State.VIEW_BUFFER_OUTPUT
            elif users_input == '2':
                return System_State.EDIT_ITEM_PROFILE_SELECT
            elif users_input == '3':
                return System_State.REMOVE_ITEM_PROFILE_SELECT
            
        case System_State.INVENTORY_ITEM_OVERVIEW:
            if users_input =='1':
                return System_State.VIEW_BUFFER_WHOLE_INVENTORY
            elif users_input == '2':
                return System_State.DISPLAY_USERS_INTO_INVENTORY

        case System_State.VIEW_BUFFER_OUTPUT:
            pass
        case System_State.VIEW_BUFFER_WHOLE_INVENTORY:
            pass
        case System_State.VIEW_BUFFER_LIST_OF_ITEMS:
            pass

        case System_State.DISPLAY_USERS_INTO_INVENTORY:
            
            input_int = int(users_input)
            user_list = app_container.inventory.get_usernames_in_inventory()
            if input_int >= 0 and input_int < len(user_list):
                app_container.buffer_output = app_container.inventory.get_users_inventory(user_list[input_int])
                return System_State.VIEW_BUFFER_LIST_OF_ITEMS
        
        case System_State.DISPLAY_PRICE_OPTIONS:
            if users_input == '1':
                item_list = app_container.inventory.get_whole_inventory()
                app_container.buffer_output = get_str_item_value_output(app_container, item_list)
                return System_State.VIEW_BUFFER_OUTPUT
            elif users_input == '2':
                return System_State.VIEW_BUFFER_INTO_VIEW_PLAYERS
            elif users_input == '3':
                return System_State.VIEW_BUFFER_INTO_ITEM_SPECIFIC_VALUE
            
        case System_State.EDIT_ITEM_OPTIONS:
            if users_input == '1':
                new_item_type = user_input_item_type()
                new_item = app_container.inventory.set_item_type(app_container.buffer_input, new_item_type)
                app_container.buffer_input = new_item
                return System_State.EDIT_ITEM_OPTIONS
            elif users_input == '2':
                new_name = user_input_item_name()
                new_item = app_container.inventory.set_item_name(app_container.buffer_input, new_name)
                app_container.buffer_input = new_item
                return System_State.EDIT_ITEM_OPTIONS
            elif users_input == '3':
                is_stattrack = user_input_item_statrack()
                new_item = app_container.inventory.set_item_stattrack(app_container.buffer_input, is_stattrack)
                app_container.buffer_input = new_item
                return System_State.EDIT_ITEM_OPTIONS
            elif users_input == '4':
                new_item_condition = user_input_item_condition()
                condition_str = Item.get_condition_str_from_cond(new_item_condition)
                new_item = app_container.inventory.set_item_condition(app_container.buffer_input, condition_str)
                app_container.buffer_input = new_item
                return System_State.EDIT_ITEM_OPTIONS
            elif users_input == '5':
                new_item_owner = user_input_item_user()
                new_item = app_container.inventory.set_item_owner(app_container.buffer_input, new_item_owner)
                app_container.buffer_input = new_item
                return System_State.EDIT_ITEM_OPTIONS
            elif users_input == '6':
                pass
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
            selection = profile_select(app_container, users_input, System_State.REMOVE_ITEM_SELECT)
            if selection != None:
                return selection
        case System_State.EDIT_ITEM_PROFILE_SELECT:
            selection = profile_select(app_container, users_input, System_State.EDIT_ITEM_SELECT)
            if selection != None:
                return selection

        case System_State.REMOVE_ITEM_SELECT:
            selection = item_select_from_buffer(app_container, users_input, System_State.REMOVE_ITEM_QUATITY)
            if selection != None:
                return selection
        case System_State.EDIT_ITEM_SELECT:
            selection = item_select_from_buffer(app_container, users_input, System_State.EDIT_ITEM_OPTIONS)
            if selection != None:
                return selection

        case System_State.REMOVE_ITEM_QUATITY:
            try:
                input_int = int(users_input)
                if input_int >= 1 and input_int <= app_container.buffer_input.quantity:
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

def display_items_from_buffer(app_container):
    buff = ""
    for x in range(len(app_container.buffer_output)):
        buff += f"{x}: {TEXT_BOLD}{app_container.buffer_output[x].construct_string()}{TEXT_ENDC} {app_container.buffer_output[x].username} - {app_container.buffer_output[x].bought_price}\n"
    if buff == "":
        return f"{TEXT_WARNING}Your Inventory is currently empty. Please add an item before continuing.{TEXT_ENDC}"
    return buff

def display_items_no_value_from_buffer(app_container):
    buff = ""
    for x in range(len(app_container.buffer_output)):
        buff += f"{x}: {TEXT_BOLD}{app_container.buffer_output[x].construct_string()}{TEXT_ENDC} {app_container.buffer_output[x].username}\n"
    if buff == "":
        return f"{TEXT_WARNING}Your Inventory is currently empty. Please add an item before continuing.{TEXT_ENDC}"
    return buff

def display_user_profiles(app_container):
    all_users = app_container.inventory.get_usernames_in_inventory()
    buffer = ""
    for x in range(len(all_users)):
        buffer += f"{x}. {TEXT_BOLD}{all_users[x]}{TEXT_ENDC}\n"
    if buffer == "":
        return f'{TEXT_WARNING}There are currently no profiles. Please add an item before continuing. {TEXT_ENDC}'
    return buffer

def profile_select(app_container, users_input, return_type):
    app_container.buffer_input = None
    try:
        input_int = int(users_input)
        user_list = app_container.inventory.get_usernames_in_inventory()
        if input_int >= 0 and input_int < len(user_list):
            app_container.buffer_output = app_container.inventory.get_users_inventory(user_list[input_int])
            app_container.buffer_input = app_container.buffer_output
            return return_type
    except ValueError as e:
        app_container.error = "Invalid input, please try again"
    except Exception as e:
            app_container.error = e

def item_select_from_buffer(app_container, users_input, return_state):
    try:
        input_int = int(users_input)
        user_list = app_container.buffer_input
        if input_int >= 0 and input_int < len(user_list):
            app_container.buffer_output = user_list[input_int]
            app_container.buffer_input = user_list[input_int]
            return return_state
    except ValueError as e:
        app_container.error = "Invalid input, please try again"
    except Exception as e:
        app_container.error = e

def user_input_item_type():
    print("Enter an item type  |  Ex: AK47, CASE, STICKER, MP7, M249, MUSIC KIT.....")
    user_type = input()
    return user_type.upper()

def user_input_item_name():
    print("Enter the item name  |  Ex: FOREST DDPAT, OPERATION BRAVO, SLATE, PRINTSTREAM.....")
    user_item_name = input()
    return user_item_name.title()

def user_input_item_statrack():
    print("Is the item stattrack?")
    user_stattrack = None
    while True:
        print("Enter either y/n:")
        temp = input().upper()
        if temp == "Y":
            user_stattrack = True
            break
        elif temp == "N":
            user_stattrack = False
            break
    return user_stattrack

def user_input_item_condition():
    print("Enter the condition of the item (if applicable)")
    print("1. NONE\n2. BATTLE SCARRED\n3. WELL_WORN\n4. FIELD_TESTED\n5. MINIMAL_WEAR\n6. FACTORY_NEW")
    user_condition = None
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
    return user_condition

def user_input_item_user():
    print("Please enter a profile name  |  Ex: Ant, Sticker Collection....")
    while True:
        user_name = input()
        if user_name != "":
            return user_name
        print("Profile name cannot be left blank")

def create_item(app_container):
    clear()
    user_type = user_input_item_type()
    user_item_name = user_input_item_name()
    user_stattrack = user_input_item_statrack()
    user_condition = user_input_item_condition()
    print("Please enter the price that you bought the item at  |  Ex: 1.99, 42.93 , 0.03.....")
    while True:
        try:
            user_price = input()
            user_price = float(user_price)
            break
        except:
            print("invalid input, please try again")
    print("Please enter the quantity of items you have bought  |  ex: 1, 2, 37.....")
    while True:
        try:
            user_quantity = input()
            user_quantity = int(user_quantity)
            if user_quantity <= 0:
                raise Exception("zero or less than")
            break
        except:
            print("invalid input, please try again")
    user_name = user_input_item_user()
    generated_item = Item(user_type, user_item_name, user_price, user_quantity, user_condition, user_stattrack, user_name)
    app_container.inventory.add_item_and_history(generated_item)
    print("Would you like to see the profit for this item now?")
    while True:
        print("Enter either y/n:")
        temp = input().upper()
        if temp == "Y":
            app_container.buffer_output = get_str_item_value_output(app_container, [generated_item])
            break
        elif temp == "N":
            break

def get_str_item_value_output(app_container, items: list[Item]):
    items_visited = []
    buffer = ""
    absolute_gained = 0
    absolute_spent = 0
    buffer += f"{TEXT_WARNING}Please be sure to stretch your terminal to prevent the table from wrapping\n{TEXT_ENDC}Items labeld with ** are items that could not be found in the market\nlikely due to spelling and have been replaced with the next closes result\n"
    buffer += f"| {'Item':<28} | {'Market Val':>10} | {'Qty':>3} | {'Bought at':>9} | {'Spent':>9} | {'Profit':>9} |\n"
    buffer += "-" * 86 + "\n"
    for item in items:
        if item.construct_string() in items_visited:
            continue
        else:
            items_visited.append(item.construct_string())
        total_spent = 0
        total_gained = 0
        item_with_history = app_container.inventory.get_accurate_items_history_from_item(item)
        item_value = app_container.scraper.get_item_value(item)
        for single_item in item_with_history:
            total_spent += single_item.bought_price * single_item.quantity
            single_item.set_market_value(item_value.market_value)
            total_gained += single_item.market_value * single_item.quantity
            text_value_color = profit_color(single_item.get_total_profit())
            identifyed_item_name = identify_item_inaccuracy(single_item.construct_string(), item_value.construct_string())
            buffer += f"| {trunc_name(identifyed_item_name, 28):<28} | {single_item.market_value:<10} | {single_item.quantity:<3d} | {single_item.bought_price:<9} | {single_item.get_total_spent():>9.4f} | {text_value_color}{single_item.get_total_profit():>9.4f}{TEXT_ENDC} |\n"
        #buffer += f"---------------------------------\n{TEXT_BOLD}Sub Total Spent: {total_spent}\nSub Total Market Value: {total_gained}\nSub Total Profit: {total_gained - total_spent}{TEXT_ENDC}\n\n" 
        absolute_spent += total_spent
        absolute_gained += total_gained
    profit = absolute_gained - absolute_spent
    text_value_color = profit_color(profit)
    buffer += f"\n\n{TEXT_BOLD}Total Market Value:  {absolute_gained:.4f}\n{"Total Spent:":<20} {absolute_spent:.4f}\n{"Total Profit:":<20} {text_value_color}{profit:.4f}{TEXT_ENDC}\n\n" 
    return buffer

def identify_item_inaccuracy(orgin_name:str, new_name:str):
    if orgin_name.lower() == new_name.lower():
        return orgin_name
    return f"**{new_name}"

def trunc_name(name, max_length):
    return name if len(name) <= max_length else name[:max_length - 3] + "..."

def profit_color(profit):
    if profit <= 0.00001 and profit >= -0.00001:
        return TEXT_WARNING
    elif profit > 0:
        return TEXT_OKGREEN
    return TEXT_FAIL

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