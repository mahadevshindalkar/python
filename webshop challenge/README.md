# WebShop

## Problem Statements

### TASK 1

WEBSHOP Ltd. has 12 warehouses: one for each region of England and one for each of the other three countries in the UK. The list of warehouses is as follows:

East Midlands
East of England
London
North East
North West
Northern Ireland
Scotland
South East
South West
Wales
West Midlands
Yorkshire and The Humber

A customer's purchases are always delivered from the warehouse in the region in which they live. We know our customers' postcodes, but we don't yet know what regions they live in!

Use the free and open source postcode lookup API that is documented at https://postcodes.io/ to find which country and region the customers live in.

Modify the file "PersonData.csv" with a new column, "warehouse", with the name of the Warehouse region.

N.B. Channel Islands residents should get deliveries from the South West warehouse; Isle of Man resident from North West. England residents without a region should get deliveries from West Midlands.

### TASK 2

Orders are coming in! We need to make a system to dispatch them from the warehouses. Management have decided to simply wait until twenty items have been ordered from a particular warehouse, and then dispatch them together with a courier (this is not the most efficient system possible). It's OK if the last order added to a delivery takes the number of items over twenty; we don't want to split up orders.

Order data is stored in the SQLite database WebShop.db (you can connect to this with the sqlite3 module, documented here: https://docs.python.org/2/library/sqlite3.html ).

There are two tables, "Orders" and "OrderItems".

The "Orders" table has three columns: 'OrderID' (an integer primary key), 'CustomerID' (an integer which can be used to link to the data in 'PersonData.csv'), and 'Timestamp' (a timestamp indicating the datetime of the order).

The 'OrderItems' table has two columns: 'OrderID' (for linking to the first table) and 'ItemID' (an integer defining an item). There is one row for each item in each order. There may be multiple rows with identical data (except the hidden ROWID) if a customer ordered an item more than once in the same order.

You should create a process to work out which items should be dispatched together from which warehouse, and at what time.

You should output a CSV file called 'Dispatch.csv' with the following columns:

'DispatchID' - An integer you create.
'Warehouse' - The name of the regional warehouse.
'ItemID' - As in the OrderItems table.
'OrderID' - As in the Orders and OrderItems tables.
'CustomerID' - As in the Orders table.
'Postcode'
'DispatchTimestamp' - This should be the timestamp of the last order added to the the delivery.

There should be one row per item for each dispatch.

### TASK 3

Our stock pickers in the warehouses have raised a big problem - we have been selling items that are out of stock!

We need to change the dispatch system so that it only fills orders when all items are in stock. The remaining orders should be filled when items come back in stock.

Initial stock levels for all the warehouses are given in the JSON file "inventory.json". If no value is given for an item, it is not in stock at that warehouse.

The stock replenishment deliveries are listed in the "deliveries" directory; there is one .json file for each delivery. The files indicate which warehouse the delivery is for, as well as the date, time, and contents of the delivery.

For this task you should output another CSV file called 'Dispatch2.csv'. It should have the same columns as 'Dispatch.csv' plus one additional column, "StockCount" which is an integer that indicates how many instances of that item are in stock after being picked for delivery.

## Install dependencies

### For python3

```
pip3 install -r requirements.txt
```

## Solution

### For task - 1

```
python3 update_person_data.py
```

### For task - 2

```
python3 dispatch_system.py
```

## Pandas documents

See [Pandas reference] (https://pandas.pydata.org/pandas-docs/stable/reference/index.html)
