from inventory_lsit import *
import os

class System_State(Enum):
    MAIN_MENU = 0
    ADD_ITEM_OVERVIEW = 1
    INVENTORY_ITEM_OVERVIEW = 2

def display(current_state, users_input):
    match current_state:

        case System_State.MAIN_MENU:
            print('''Options
1. Add / Import / Export items to inventory.
2. Inventory Item Overview
3. Profits''')
            
        case System_State.ADD_ITEM_OVERVIEW:
            print('''Options
1. Google sheets
2. Add item manually''')
            
        case System_State.INVENTORY_ITEM_OVERVIEW:
            print('''Options
1. Get all items
2. Get items from user
3. Get Purchase history from item''')


        case _:
            raise Exception("unkown state condition raised")
    print('q to quit    |   x back to main menu' )
        



def reaction(current_state, users_input):
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
                pass

        case System_State.ADD_ITEM_OVERVIEW:
            pass

        case _:
            raise Exception("unkown state contition raised in reaction")
        
    return current_state

def clear():
    os.system('clr' if os.name == 'nt' else 'clear')

def main():
    inventory = Inventory_List()
    current_state = System_State.MAIN_MENU
    users_input = ""
    clear()
    while True:
        display(current_state, users_input)
        users_input = input()
        current_state = reaction(current_state, users_input)
        clear()


main()

'''
inventory = Inventory_List()

item = Item("Ak-47", "Python Skin", 6.79, quanity=2, condition=Condition.BATTLE_SCARRED, username="tester1")

inventory.add_item_and_history(item)

inventory.display_whole_inventory()
inventory.display_whole_history()
'''