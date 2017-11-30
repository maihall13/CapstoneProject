import Geocoding
import Weather
import PixLab
import ThreadGenius
import Pinterest
import Instagram
import Jacket
import AlchemyOutlook
#Get location - will need validation on webpage
location = input("Enter Location")

#Get coordinates
latlon = Geocoding.Geocoding().getLocation(location)
lat = str(latlon["lat"])
long = str(latlon["lng"])

#Get weather based on coordinates
weather = Weather.Weather()
weather.getAllInfo(lat,long)
print(weather.getCurrent())
print(weather.getDescription())
print(weather.getHigh())
print(weather.getLow())
print(weather.getHumidity())
print(weather.getWind())

alchemy = AlchemyOutlook.Alchemy(location)
print(alchemy.runAlchemy())

