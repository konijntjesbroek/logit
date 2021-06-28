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
    lat = round(lat, 4)
    lon = round(lon, 4)
    key = os.environ['OWX']
    url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&lat={lat}&lon={lon}&units=imperial'
    src = urllib.request.urlopen(url)
    soup = bs(src, 'lxml')
    return json.loads(soup.text)

def reverse_geo(lat, lon):
    key = os.environ['GEO_ID']
    url = f'https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&lang=en&limit=1&apiKey={key}'
    src = urllib.request.urlopen(url)
    soup = bs(src, 'lxml')
    response = json.loads(soup.text)['features'][0]['properties']
    return f"{response['suburb']}, {response['city']}, {response['state_code']}"

class Tablet_info():
    def __init__(self, location):
        self.lat = location[1]['latitude']
        self.lon = location[1]['longitude']
        
class Journal_Header():
    def __init__(self, table, location):
        self.lat = location.lat
        self.lon = location.lon
        self.date = dt.fromtimestamp(table['dt']).strftime('%A, %B %d, %Y; %H:%M')
        self.temp = int(round(table['main']['temp'], 0))
        self.e_temp = int(round(table['main']['feels_like'], 0))
        self.hi = table['main']['temp_max']
        self.lo = table['main']['temp_min']
        self.rise = dt.fromtimestamp(table['sys']['sunrise']).strftime('%H:%M')
        self.set = dt.fromtimestamp(table['sys']['sunset']).strftime('%H:%M')
    
    def get_loc(self):
        friendly_coords = ''
        if self.lat >= 0:
            friendly_coords += str(round(self.lat, 4)) + '° N, '
        else:
            friendly_coords += str(round(-self.lat, 4)) + '° S, '
        if self.lon >= 0:
            friendly_coords += str(round(self.lon, 4)) + '° E'
        else:
            friendly_coords += str(round(-self.lon, 4)) + '° W'
        return friendly_coords


def main():
    raw_loc =  tablet.location()
    ti = Tablet_info(raw_loc)
    wx_table =  get_wx_data(ti.lat, ti.lon)
    jh=Journal_Header(wx_table, ti)
    g_tag = reverse_geo(ti.lat, ti.lon)
    sep_line = 10 * '-'
    print(f'{jh.date}\n@{g_tag}')
    print(f' ({jh.get_loc()})')
    print(sep_line) 
    print(f'    sunedges: {jh.rise} | {jh.set}')
    print(f'    current temp: {jh.temp}')
    print(f'    effective temp: {jh.e_temp}')
    print(f'    hi: {jh.hi}\tlo: {jh.lo}')
    print(sep_line)

if __name__== '__main__':
    main()
