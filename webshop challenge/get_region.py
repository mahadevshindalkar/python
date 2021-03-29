#!./venv/bin/python

import json
import requests

import postcodes_io_api


class Region(object):

  @staticmethod
  def getRegion(postcode):
    apiURL = f'https://api.postcodes.io/postcodes/{postcode}'

    response = requests.get(apiURL)

    if response.status_code == 200:
        payload = json.loads(response.content.decode('utf-8'))
        region = payload['result']['region']
        country = payload['result']['country']
        return region, country
    else:
        return '', ''
