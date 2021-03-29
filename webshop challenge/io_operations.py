#!./venv/bin/python

import sqlite3
import pandas as pd

def readCSV(filename):
  return pd.read_csv(filename)

def writeCSV(filename, df):
  try:
    df.to_csv(filename)
    print(f'{filename} is saved successfully')
  except:
    print(f'Failed to save {filename}')

def getDataFrame(records, namedTuple):
  return pd.DataFrame.from_records(records, columns=namedTuple._fields)

def readSqlQuery(query):
  dbConnection = sqlite3.connect("WebShop.db")

  with dbConnection:
    df = pd.read_sql_query(query, dbConnection)

  return df