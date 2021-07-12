#!/usr/bin/env python3

# Hacked together by matt <at> faraday.at
# This script requires an immersun hardware unit, with internet bridge
# and an account setup at live.myimmersun.com
# it also requires the t-rex miner to be up and running (but can be paused)
# I suggest you cron this script

import urllib3
import requests
from datetime import datetime
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup

### Change these ###

username = "my@email.com"
password = "mypassword"
trexIP = "192.168.0.2"
trexPort = "4067"
url = 'http://live.myimmersun.com'


## The amount of power your graphics card/computer uses to mine with, in watts
miningpower = 350
###


##Scrape the immersun website
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


# Check current status of t-rex miner

http = urllib3.PoolManager()
minerStatusUrl = "http://"+trexIP+":"+trexPort+"/summary"
response = http.request('GET', minerStatusUrl)
minerStatus = response.data.decode('utf-8')

if "\"paused\":true" in minerStatus:
  mining = False
if "\"paused\":false" in minerStatus:
  mining = True


###DEBUGGING
#print("Mining = ", mining)
#print("Production: ", pproduction)
#print("Consumption: ", pconsumption)
#print("Surplus: ",pfree)
############


if (pfree > miningpower and mining == False):
#   print("Enough energy free to mine, starting miner")
   response = requests.get("http://"+trexIP+":"+trexPort+"/control?pause=false")
#   print(response)

if (mining == True and pconsumption > pproduction):
#   print("Insufficient free power to mine, pausing miner")
   response = requests.get("http://"+trexIP+":"+trexPort+"/control?pause=true")
#   print(response)
