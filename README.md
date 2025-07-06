# 📦 Counter Strike Item Market Status 📦

This project retrieves the current market value of your skins from your Counter Strike inventory and the retrieve the profits of your current assets.

In this application:
* Users will manualy input their items and the amount it was purchased for into a database.
* The application will scrap the current steam market for each items current market value.
* The application will return a list of items that display a sub total of profit from each item and the current value of your inventory.
* all items are saved into a local database for future investment check in.

--------------
![Table Sample](/Assets/profit_table.png "Table Sample")

--------------
## Why?

My Friends and I often like to make questionable financial invenstments, and one thing we like to invenst in is: Counter Strike skins. this application allows us to easily track how much our inventory value has accumulated without having to go item by item and manualy do the calculations.

## 📱 Features

- 💵 Get the current value of all your CS assets
- 🔧 Supports multiple currencies
- 🔗 Scraps the Steam market for the most current value of an item
- 🔧 Items are stored in a local DB that can be added, removed, and modified.
- 🔗 Create profiles to sort your item collection, or add your friend to the list.

![Profile Sample](/Assets/User_table.png "Profile Sample")

## 🛠️ Installation and Dependencies

This Applicaitons requires
* Python 3
* BeautifulSoup4
* requests

```bash
# Clone the repository
git clone https://github.com/Awowz/CS-Item-Market-Status.git

# Navigate into the directory
cd CS-Item-Market-Status

# Install Dependencies
pip install -r requirements.txt
```
Application is now ready to run with ```python3 main.py```

--------------

## 📋 Usage

This application should be straight forward to use.

after opening the app with ```python3 main.py``` you can start by adding items to your inventory
- navigate to 'Add / Remove / Edit Items'
- Then navigate to 'Add item manually'
- youll be prompted with a seriies of questions. youll need to provide what type of item it is, the name of the item, if the item has a condition, a price, quantity and an optional profile name.

After adding whatever amount of items you desire, you can go back to the main menu by typing 'x' and enter.

Now that you have items in your inventory, you can check their live value
- navigate to 'Profits'
- Select your desired option of displaying all items, profile items, or single item
- a table will be generated, be sure to stretch out your console window if its warped.


## 🛠️ Modifications

* currency can be changed from USD to anyother currency. change ```COUNTRY_VALUE``` and ```CURRENCY_VALUE``` to the correct correspoding values that allign with steam api guidlines. USD = 1, EUR = 3 ...