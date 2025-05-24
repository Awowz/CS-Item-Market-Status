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
            if users_input == '1':
                pass
            elif users_input == '2':
                create_item()
                return System_State.ADD_ITEM_OVERVIEW

        case _:
            raise Exception("unkown state contition raised in reaction")
        
    return current_state

def clear():
    os.system('clr' if os.name == 'nt' else 'clear')

def create_item():
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
        except:
            pass
    print("please enter the price that you bought the item at ex: 42.93 , 0.03")
    while True:
        try:
            user_price = input()
            user_price = float(user_price)
            if user_price <= 0.009:
                raise Exception("invalid input")
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
    global inventory
    inventory.add_item_and_history(generated_item)


def main():
    current_state = System_State.MAIN_MENU
    users_input = ""
    clear()
    while True:
        display(current_state, users_input)
        users_input = input()
        current_state = reaction(current_state, users_input)
        clear()

inventory = Inventory_List()
main()

'''
inventory = Inventory_List()

item = Item("Ak-47", "Python Skin", 6.79, quanity=2, condition=Condition.BATTLE_SCARRED, username="tester1")

inventory.add_item_and_history(item)

inventory.display_whole_inventory()
inventory.display_whole_history()
'''