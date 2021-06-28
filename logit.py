#!/usr/bin/python3
'''
logit
created by: Arlo Gittings
created on: 2021-06-27
last modified: 2021-06-27
description:
    Python tool to build a log entry
'''
import os
import json
from termux import API as tablet
import urllib.request
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

raw_loc =  tablet.location()
loc_table = raw_loc[1]
lat = round(raw_loc[1]['latitude'], 4)
lon = round(loc_table['longitude'], 4)
key = os.environ['OWX']
url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&lat={lat}&lon={lon}&units=imperial'
src = urllib.request.urlopen(url)
soup = bs(src, 'lxml')
wx_table = json.loads(soup.text)

print(dt.fromtimestamp(wx_table['dt']).strftime('%A, %B %d, %Y\n%H:%M'))

fields = {'Location: ': 'coord', 'Conditions: ': 'main'}
for field in fields:
    print(field)
    segment = fields[field]
    for item  in  wx_table[segment]:
        print(f'\t{item}: {wx_table[segment][item]}')
    print()

print(f'Sunrise: {dt.fromtimestamp(wx_table["sys"]["sunrise"]).strftime("%H:%M")}\nSunset:  {dt.fromtimestamp(wx_table["sys"]["sunset"]).strftime("%H:%M")}')
