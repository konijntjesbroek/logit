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

def get_wx_data(lat, lon):
    key = os.environ['OWX']
    url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&lat={lat}&lon={lon}&units=imperial'
    src = urllib.request.urlopen(url)
    soup = bs(src, 'lxml')
    return json.loads(soup.text)

class Tablet_info():
    def __init__(self, location):
        self.lat = round(location[1]['latitude'], 4)
        self.lon = round(location[1]['longitude'], 4)
        
class Journal_Header():
    def __init__(self, table):
        self.lat = table['coord']['lat'] 
        self.lon = table['coord']['lon']
        self.date = dt.fromtimestamp(table['dt']).strftime('%A, %B %d, %Y @%H:%M')
        self.temp = int(round(table['main']['temp'], 0))
        self.e_temp = int(round(table['main']['feels_like'], 0))
        self.hi = table['main']['temp_max']
        self.lo = table['main']['temp_min']
        self.rise = dt.fromtimestamp(table['sys']['sunrise']).strftime('%H:%M')
        self.set = dt.fromtimestamp(table['sys']['sunset']).strftime('%H:%M')
    
    def get_loc(self):
        friendly_coords = ''
        if self.lat >= 0:
            friendly_coords += str(self.lat) + '° N, '
        else:
            friendly_coords += str(-self.lat) + '° S, '
        if self.lon >= 0:
            friendly_coords += str(self.lon) + '° E'
        else:
            friendly_coords += str(-self.lon) + '° W'
        return friendly_coords


def main():
    raw_loc =  tablet.location()
    ti = Tablet_info(raw_loc)
    wx_table =  get_wx_data(ti.lat, ti.lon)
    jh=Journal_Header(wx_table)

    print(f'{jh.date} @{jh.get_loc()}')
    print(f'  sunedges: {jh.rise}/{jh.set}')
    print(f'  current temp/feels like: {jh.temp}/{jh.e_temp}')
    print(f'  hi/lo: {jh.hi}/{jh.lo}')

if __name__== '__main__':
    main()
