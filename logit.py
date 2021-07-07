#!/usr/bin/python3
'''
logit
created by: Arlo Gittings
created on: 2021-06-27
last modified: 2021-07-06
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

class Journal_Header():
    def __init__(self, location):
        '''
        Journal Header
            expects:
                location: gps object holding the location of the current device
            attributes:
                lat:    float; device latitude
                lon:    float; device longitude
                table:  json object; the table of weather details retrieved from openweathermap.org
                temp:   int;regional temp
                e_temp: int; the effective temp including heat index or windchill
                hi:     float; expected high for the day
                lo:     float; expected low temperature
                rise;   datetime; expected time of sunrise
                set:    datetime; expected time of sunset
                g_tag:  str; The suburb, city, state/province as returned from geoapify.com
            methods:
                get_wx_data:    return json of weather data from openweathermap.org API
                reverse_geo:    return a formatted string of the suburb, city, state/province from geoapify.com
                get_loc:        return a human friendly version of latitude and longitude from raw lat/lon
                build_header:   return a formatted header for journal entries 
        '''
        self.lat = location[1]['latitude']
        self.lon = location[1]['longitude']
        self.table = self.get_wx_data()
        self.date = dt.fromtimestamp(self.table['dt']).strftime('%A, %B %d, %Y; %H:%M')
        self.temp = int(round(self.table['main']['temp'], 0))
        self.e_temp = int(round(self.table['main']['feels_like'], 0))
        self.hi = self.table['main']['temp_max']
        self.lo = self.table['main']['temp_min']
        self.rise = dt.fromtimestamp(self.table['sys']['sunrise']).strftime('%H:%M')
        self.set = dt.fromtimestamp(self.table['sys']['sunset']).strftime('%H:%M')
        self.g_tag = self.reverse_geo()

    def get_wx_data(self):
        '''
        get_wx_data:
            expects:
                self
            uses:
                lat:    float; latitude rounded to 4 sigfigs 
                lon:    float: longitude rounded to 4 sigfigs
                ^^^ These are mandated by the API
                units:  str; imperial or metric 
                key:    str: API key as provided by openweathermap.org this is
                        This is loaded as an environmental variable and pulled
                        in by the os module. Be Careful With Your Keys!
                url:    fstr: formatted API call with variable substitution
            returns:
                json object containing the data as provided by
        '''
        lat = round(self.lat, 4)
        lon = round(self.lon, 4)
        units = 'imperial'
        key = os.environ['OWX']
        url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&lat={lat}&lon={lon}&units={units}'
        src = urllib.request.urlopen(url)
        soup = bs(src, 'lxml')
        return json.loads(soup.text)


    def reverse_geo(self):
        '''
        reverse_geo:
            expects:
                self
            uses:
                key:    str; API key provided by geoapify.com. Pulled in by os 
                        module.
                url:    fstr; formatted API call with variable substitution
            returns:
                fstring containing the suburb, city, and state code provided by
                the API call
        '''
        key = os.environ['GEO_ID']
        url = f'https://api.geoapify.com/v1/geocode/reverse?lat={self.lat}&lon={self.lon}&lang=en&limit=1&apiKey={key}'
        src = urllib.request.urlopen(url)
        soup = bs(src, 'lxml')
        response = json.loads(soup.text)['features'][0]['properties']
        return f"{response['suburb']}, {response['city']}, {response['state_code']}"
       
    def get_loc(self):
        '''
        get_loc:
            - GPS coordinates indicate that latitude is south of the equator 
            and longitude is west of the prime meridian
            expects:
                self
            returns:
                friendly_coords: str; latitude and longitude as read by humans
        '''
        friendly_coords = ''
        friendly_coords += str(round(self.lat, 4)) + '° N, ' if self.lat >= 0 else str(round(-self.lat, 4)) + '° S, '
        friendly_coords += str(round(self.lon, 4)) + '° E' if self.lon >= 0 else  str(round(-self.lon, 4)) + '° W'
        return friendly_coords
    
    def build_header(self):
        '''
        build_header:
            expects:
                self
            returns:
                result: fstr; a multiline string formatted to present the data
                        contained in Journal_header objects in a compact,
                        useful way. This is where you modify the layout of all
                        the things.
        '''
        sep_line = 79 * '-' + '\n'
        result =  f'{self.date}\n@{self.g_tag}\n'
        result += f' ({self.get_loc()})\n'
        result += sep_line 
        result += f'    sunedges: {self.rise} | {self.set}\n'
        result += f'    current temp: {self.temp}\n'
        result += f'    effective temp: {self.e_temp}\n'
        result += f'    hi: {self.hi}\tlo: {self.lo}\n'
        result += sep_line + '\n' + sep_line[:79]
        return result


def main():
    jh=Journal_Header(tablet.location())

    print(jh.build_header())

if __name__== '__main__':
    main()
