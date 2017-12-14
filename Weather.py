import datetime
import json
import urllib.request
import pytemperature


#Using OpenWeatherMap API
#Free 60 calls a minute

class Weather():
    def __init__(self):
        #file = open("weatherkey.txt", "r")
        #key = file.readline()
        #file.close()
        #self.key = key

        self.key = "256b72cf5d99fffedb833cc657964aad"

    def time_converter(self, time):
        converted_time = datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%I:%M %p')
        self.converted_time = converted_time


    def getAllInfo(self, la, lo):
        # lat={lat}&lon={lon}
        key = self.key
        full_api_url = "http://api.openweathermap.org/data/2.5/weather?lat=" + la + "&lon=" + lo + "&APPID=" + key
        #print(full_api_url)

        url = urllib.request.urlopen(full_api_url)
        output = url.read().decode('utf-8')
        raw_api_dict = json.loads(output)
        url.close()
        print(raw_api_dict)
        self.m_symbol = '\xb0' + 'F'

        self.data = dict(
            city=raw_api_dict.get('name'),
            country=raw_api_dict.get('sys').get('country'),
            temp=raw_api_dict.get('main').get('temp'),
            temp_max=raw_api_dict.get('main').get('temp_max'),
            temp_min=raw_api_dict.get('main').get('temp_min'),
            humidity=raw_api_dict.get('main').get('humidity'),
            pressure=raw_api_dict.get('main').get('pressure'),
            sky=raw_api_dict['weather'][0]['description'],
            icon=raw_api_dict['weather'][0]['icon'],
            sunrise=self.time_converter(raw_api_dict.get('sys').get('sunrise')),
            sunset=self.time_converter(raw_api_dict.get('sys').get('sunset')),
            wind=raw_api_dict.get('wind').get('speed'),
            wind_deg=raw_api_dict.get('deg'),
            dt=self.time_converter(raw_api_dict.get('dt')),
            cloudiness=raw_api_dict.get('clouds').get('all')
        )
        return self.data
    def getIcon(self):
        icon = self.data['icon']
        icon = "http://openweathermap.org/img/w/" + icon + ".png"
        return icon

    def getWind(self):
        wind = self.data['wind']
        wind = str(int(round(wind*2.2369))) + " mph"
        return wind

    def getHumidity(self):
        hum = str(self.data['humidity']) + "%"
        return hum

    def getCurrent(self):
        current = self.data['temp']
        current = str(pytemperature.k2f(current))  + self.m_symbol
        return current

    def getDescription(self):
        desc =  self.data['sky']
        return desc

    def getHigh(self):
        high = self.data['temp_max']
        high = str(pytemperature.k2f(high)) + self.m_symbol
        return high


    def getLow(self):
        low = self.data['temp_min']
        low = str(pytemperature.k2f(low)) + self.m_symbol
        return low

#weather = Weather()
#weather.getAllInfo("37.3860517", "-122.0838511" )
#print(weather.getDescription())
#print(weather.getIcon())
"""
if __name__ == '__main__':
    try:
        weather = Weather()
        weather.getAllInfo("37.3860517", "-122.0838511" )
        print(weather.getCurrent())
        print(weather.getHigh())
        print(weather.getLow())
        print(weather.getDescription())
        print(weather.getHumidity())
        print(weather.getWind())


    except IOError:
        print('no internet')

"""



