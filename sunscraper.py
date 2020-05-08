#!/usr/bin/env python3

# Hacked together by matt <at> faraday.at 
# This script requires an immersun hardware unit, with internet bridge
# and an account setup at live.myimmersun.com 

import requests
from datetime import datetime
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient


timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

### Update these ###
username = "my@email.com"
password = "passwordgoeshere"
dbhost = '192.168.0.2'
dbport = '8086'
dbname = 'immersun'
pvname = "my solar farm" 
pvloc  = "London"
###

url = 'http://live.myimmersun.com'
page = requests.get(url, auth=HTTPDigestAuth(username, password))
soup = BeautifulSoup(page.text, 'html.parser')

import_power = soup.find(class_='container')
import_power_item = import_power.find_all('p')

client = InfluxDBClient(dbhost, dbport)

import_value = import_power_item[0].contents[0]
production_value = import_power_item[1].contents[0]
consumption_value = import_power_item[2].contents[0]

if "Hot" not in import_power_item[3].contents[0]:
     divert_value = import_power_item[3].contents[0]
 else:
     divert_value = 0

json_body = [
        {
            "measurement": "immersun_stats",
            "tags": {
                "host": pvname,
                "region": pvloc
            },
            "time": timestamp,
            "fields": {
                "Import": int(str(import_value).rstrip('W')),
                "Production": int(str(production_value).rstrip('W')),
                "Consumption": int(str(consumption_value).rstrip('W')),
                "Divert": int(str(divert_value).rstrip('W'))
            }
        }
    ]
client.create_database(dbname)
client.write_points(json_body, time_precision='ms',protocol='json',database=dbname)
