import requests

#Geocoding used to get latitude and longtitude of a location

class Geocoding():
    def __init__(self):
        #Will need to obtain key from txt file

        #file = open("geocodingkey.txt", "r")
        #key = file.readline()
        #file.close()
        #self.key = key
        self.key = "AIzaSyCg2F23yo3rQs_Etb3YqH-tX6kQmCZUMpI"

    def getLocation(self, address):
        #creates appropriate string format if space

        address=address.replace(" ", "+")
        #Uses Json to get query
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address +"&key=" + self.key)
        resp_json_payload = response.json()

        print(resp_json_payload['results'][0]['geometry']['location'])
        return(resp_json_payload['results'][0]['geometry']['location'])


#try:
#    print(Geocoding().getLocation("minneapolis sculpture garden, minneapolis"))
#except Exception as e:
#    print(e)

