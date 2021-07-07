#!/usr/bin/env python3

# Hacked together by matt <at> faraday.at
# This script requires an immersun hardware unit, with internet bridge
# and an account setup at live.myimmersun.com
# it also requires the t-rex miner to be up and running (but can be paused)
# I suggest you cron this script

import requests
from datetime import datetime
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup

####### CHANGE THESE #######
username = "my@email.com"
password = "password"
trexIP = 192.168.0.3
############################


url = 'http://live.myimmersun.com'
page = requests.get(url, auth=HTTPDigestAuth(username, password))
soup = BeautifulSoup(page.text, 'html.parser')

import_power = soup.find(class_='container')
import_power_item = import_power.find_all('p')
import_value = import_power_item[0].contents[0]
production_value = import_power_item[1].contents[0]
consumption_value = import_power_item[2].contents[0]

if "Hot" not in import_power_item[3].contents[0]:
     divert_value = import_power_item[3].contents[0]
else:
     divert_value = 0
pproduction = int(str(production_value).rstrip('W'))
pconsumption = int(str(consumption_value).rstrip('W'))
pfree = pproduction - pconsumption

if (pfree > 150):
   response = requests.get("http://10.0.0.30:4067/control?pause=false")
else:
   response = requests.get("http://10.0.0.30:4067/control?pause=true")
