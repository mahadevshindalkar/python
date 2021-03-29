#!./venv/bin/python

import collections
import dateutil.parser
import datetime
import pandas as pd

from io_operations import readSqlQuery, readCSV, getDataFrame, writeCSV

DispatchOrder = collections.namedtuple('DispatchOrder', 'Warehouse OrderID CustomerID Postcode DispatchTimestamp')

perWarehouse = {
  'East Midlands': {'itemsCount': 0, 'orders': []},
  'East of England': {'itemsCount': 0, 'orders': []},
  'London': {'itemsCount': 0, 'orders': []},
  'North East': {'itemsCount': 0, 'orders': []},
  'North West': {'itemsCount': 0, 'orders': []},
  'Northern Ireland': {'itemsCount': 0, 'orders': []},
  'Scotland': {'itemsCount': 0, 'orders': []},
  'South East': {'itemsCount': 0, 'orders': []},
  'South West': {'itemsCount': 0, 'orders': []},
  'Wales': {'itemsCount': 0, 'orders': []},
  'West Midlands': {'itemsCount': 0, 'orders': []},
  'Yorkshire and The Humber': {'itemsCount': 0, 'orders': []}
}

def getMaxTimestamp(orders):
  """
  Get the dispatchtimestamp - last order timestamp
  :params orders: collection of orders havinf 20 or more items together
  :return maxDateTime: dispatch timestamp
  """
  maxDateTime = None
  
  for order in orders:
    if maxDateTime is None or dateutil.parser.parse(order[3]) > dateutil.parser.parse(maxDateTime): maxDateTime = order[3]

  return maxDateTime
    
# Order by Timestamp to FIFO
orders = readSqlQuery('SELECT * FROM Orders')

# Get items per order
itemsPerOrder = readSqlQuery('SELECT OrderID, COUNT(ItemID) as ItemsPerOrderID FROM OrderItems GROUP BY OrderID')

# Get order items
orderItems = readSqlQuery('SELECT * FROM OrderItems')

# Get all customer data
customers = readCSV('PersonData.csv')

# Have all orders with client details - to get warehouse and postcode
ordersWithCustomerDetails = orders.join(customers.set_index('CustomerID'), on='CustomerID')

orderWithCustomerAndItemsPerOrder = ordersWithCustomerDetails.join(itemsPerOrder.set_index('OrderID'), on='OrderID')

dispatch = []

for row in orderWithCustomerAndItemsPerOrder.sort_values(by=['Timestamp']).itertuples(index=False):
  if not pd.isnull(row.warehouse):
    warehouseOrder = perWarehouse[row.warehouse]

    warehouseOrder['itemsCount'] +=  row.ItemsPerOrderID
    warehouseOrder['orders'].append([row.OrderID, row.CustomerID, row.postcode, row.Timestamp])

    # For 20 or more item dispatch from a respective warehouse
    if warehouseOrder['itemsCount'] > 19:
      dispatchTime = getMaxTimestamp(warehouseOrder['orders'])

      for order in warehouseOrder['orders']:
        dispatch.append(
          DispatchOrder(
            Warehouse=row.warehouse,
            OrderID=order[0],
            CustomerID=order[1],
            Postcode=order[2],
            DispatchTimestamp=dispatchTime
          )
        )
      
      # Reset warehouse orders
      warehouseOrder['itemsCount'] = 0
      warehouseOrder['orders'] = []

orderCollections = getDataFrame(dispatch, DispatchOrder)

ordersToDispatchPerWarehouse = orderCollections.join(orderItems.set_index('OrderID'), on='OrderID')

ordersToDispatchPerWarehouse.index = [x for x in range(1, len(ordersToDispatchPerWarehouse.values) + 1)]
ordersToDispatchPerWarehouse.index.name = 'DispatchID'

writeCSV('Dispatch.csv', ordersToDispatchPerWarehouse[['Warehouse', 'ItemID', 'OrderID', 'CustomerID', 'Postcode', 'DispatchTimestamp']])