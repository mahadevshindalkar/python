#!./venv/bin/python

from io_operations import readCSV, writeCSV
from get_region import Region

def region(postcode):
  region, country = Region().getRegion(postcode)

  if region == 'Channel Islands':
    return 'South West'
  elif region == 'Isle of Man':
    return 'North West'
  elif region == '' and country == 'England':
    return 'West Midlands'
  else:
    return region

customers = readCSV('PersonData.csv')

customers['warehouse'] = customers['postcode'].apply(region)

writeCSV('PersonData.csv', customers.set_index('CustomerID'))
