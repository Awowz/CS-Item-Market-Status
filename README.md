# 📦 Counter Strike Item Market Status 📦

This project retrieves the current market value of your skins from your Counter Strike inventory and the retrieve the profits of your current assets.

In this application:
* Users will input their items and the amount it was purchased for into a database.
* The application will scrap the current steam market for each items current market value.
* The application will return a list of items that display a sub total of profit from each item and the current value of your inventory.

--------------
![Table Sample](/Assets/profit_table.png "Table Sample")

## 📱 Features

- 💵 Get the current value of all your CS assets
- 🔧 Supports multiple currencies
- 🔗 Scraps the Steam market for the most current value of an item
- 🔧 Items are stored in a local DB that can be added, removed, and modified.
- 🔗 Create profiles to sort your item collection, or add your friend to the list.

## 🛠️ Installation and Dependencies

This Applicaitons requires
* Python 3
* BeautifulSoup4
* Regex

```bash
# Clone the repository
git clone https://github.com/Awowz/CS-Item-Market-Status.git

# Navigate into the directory
cd CS-Item-Market-Status
TODO
```
📋 Usage

This application should be straight forward to use.

after opening the app with ```python3 main.py``` you can start by adding items to your inventory
- navigate to 'Add / Remove / Edit Items'
- Then navigate to 'Add item manually'
- youll be prompted with a seriies of questions. youll need to provide what type of item it is, the name of the item, if the item has a condition, a price, quantity and an optional profile.
