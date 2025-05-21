from inventory_lsit import *
from curses import wrapper
import curses

class System_State(Enum):
    MAIN_MENU = 0

def display(stdscr, current_state):
    match current_state:
        case System_State.MAIN_MENU:
            stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
            stdscr.refresh()
        case _:
            raise Exception("unkown state condition raised, exiting")
        
    stdscr.refresh()


def reaction(current_state, users_input):
    pass

def main(stdscr):
    inventory = Inventory_List()
    current_state = System_State.MAIN_MENU
    users_input = ""

    while True:
        stdscr.clear()
        display(stdscr,current_state)
        stdscr.getkey()
        reaction(current_state, users_input)


wrapper(main)

