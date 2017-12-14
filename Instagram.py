import json
import re
import urllib
import webbrowser
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import requests
import facebook
from urllib.parse import urlencode, urlparse, urldefrag
import warnings
import datetime
import ast
#import Clarifai
import http

import _codecs as codecs
url = "https://www.facebook.com/v2.11/dialog/oauth?client_id=338987829901432&display=popup&response=token&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token"
#webbrowser.open(url)
#print(urlparse(url))
#print(urldefrag(url))

#with requests.Session() as s:
#    response = s.post(url,allow_redirects=True)
#response = urlopen(url, allow_redirects=True)
#    print(response.status_code)
import FaceDetect

class Facebook():
    def __init__(self):
        # Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
        warnings.filterwarnings('ignore', category=DeprecationWarning)

        # Parameters of your app and the id of the profile you want to mess with.
        FACEBOOK_APP_ID = '338987829901432'
        FACEBOOK_APP_SECRET = 'e9276abe424bb88d70df507307a7e66d'



        # Trying to get an access token. Very awkward.
        oauth_args = dict(client_id=FACEBOOK_APP_ID,
                          client_secret=FACEBOOK_APP_SECRET,
                          grant_type='client_credentials')
        oauth_curl_cmd = ['curl', 'https://graph.facebook.com/oauth/access_token?' + urlencode(oauth_args)]


        oauth_response = ast.literal_eval(requests.get(oauth_curl_cmd[1]).text)

        oauth_access_token = oauth_response['access_token']

        self.facebook_graph = facebook.GraphAPI(oauth_access_token)




    def getPlaceID(self, latlong, location):
        try:
            #for 3.4
            #lat = str(latlon["lat"])
            #long = str(latlon["lng"])
            #latlon = lat + "," + long
            #fb_response = self.facebook_graph.access_token
            #token = "EAAE0TsEvOHgBAP3Lf8BF8JeRjs8XfLZAZAszlTcgUfv9ObOhX3ZAS1gAjnieFNSnqZCVivFAe8uRjIy8ygTPZAPtJf7TxfA2Y1GNceuTZAUvApWvSFLFTjIJkmlT0oAeUsUUVnqxZBUQlqWCVbVSyi9AjZA5FAZB4zRxk9dYkYllHvCrPDbqJMqiVgHFqVRzLPmEZD"
            #response = requests.get("https://graph.facebook.com/v2.11/search?"+ "q=" + location + "&type=place&center=" + "41.8781136,-87.6297982" + "&access_token=" + token)
            #re= response.json()
            #data = (re['data'][0])
            #placeid = data['id']


            #for 3.6
            fb_response = self.facebook_graph.search(type="place", center=latlong, q=location)
            data = fb_response['data'][0]
            placeid = data['id']

            return (placeid)
        except facebook.GraphAPIError as e:
            return ('Something went wrong:', e.type, e.message)


class Instagram():
    def __init__(self):
        self.fb = Facebook()

    #Get coordinates
    def getURL(self, latlon, location):

        lat = str(latlon["lat"])
        long = str(latlon["lng"])

        latlong = lat + "," + long

        placeid = self.fb.getPlaceID(latlong, location)
        instaURL = "https://www.instagram.com/explore/locations/" + placeid + "/"
        #print(instaURL)
        return instaURL



    def getImages(self, url):
        soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
        test = (soup.findAll("script", type="text/javascript"))



        script = []
        for i in test[2]:
            script = i

        window_sharedData = (script[len("window._sharedData = "):])
        #print(window_sharedData)


        #keywords = window_sharedData.split("caption")


        #keywords = window_sharedData.split("is_video")
        keywords = window_sharedData.split("owner")
        keywords = keywords[1:]

        images = []
        for k in keywords:
            #print(k)
            #print("\n")

            #check if image is of a video
            video_start = int(k.find("is_video")) + 11
            video_end = int(k.find("code")) - 3
            is_video = (k[video_start:video_end])

            if is_video == "true":
                #print("this is a video")
                break
            else:
                #print(k)
                if "caption" in k:
                    caption_start = int(k.find("caption")) + 11
                    caption_end = int(k.find("comments")) - 4
                    caption = str((k[caption_start:caption_end]))
                    print(caption)
                else:
                    caption = "no caption"
                    print(caption)

                #get date
                date_start = int(k.find("date") + 7)
                date_end = int(k.find("display_src") - 3)
                date = self.convertTime(k[date_start:date_end])
                print("date: " + date)

                if "display_src" in k:
                    # print("true")
                    image = k.split("display_src")
                    final_img = self.findJpg(image[1])
                    images.append(final_img)
                    #print(final_img)

            print("\n")
        #new_list = []
        #x = FaceDetect.FacePlusPlus()
        #for i in images:
        #    if x.isFace(i) == True:
        #        new_list.append(i)

        return images

    #Converts Unix time stamp from instagram
    def convertTime(self, timestamp):
        return(datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %I:%M:%p'))

    def findJpg(self, stringWithJpg):
        final_img = stringWithJpg
        start = final_img.find("http")
        end = final_img.find("jpg")
        image = (final_img[start:end + 3])
        return image

#testing
#location = "millennium park,chicago"
#latlong = {'lat': 41.8825524, 'lng': -87.62255139999999}
#x = Instagram()

#url = x.getURL(latlong, location)
#print(url)
#images = x.getImages(url)
#images = list(set(images))
#print(images)
#print("\n")

#detect = Clarifai.Clarifai()
#print(detect.detectFact(images))

#test_caption = ['The', 'weather', 'these', 'days', 'is', 'like', 'spring', '\\ud83d', '\\udc97', '\\ud83d', '\\udc97', '\\ud83d', '\\udc97Thanks', 'for', 'every', 'single', 'follower', 'of', '@ruby_thecorgi.', 'I', 'woof', 'you!\\nBandana', 'from:', '@courtneyahndesign\\n.\\n.\\n.\\n.', '\\u2764', '\\ud83d', '\\udc3eCORGI', 'DOG', 'are', 'my', 'entire', 'life', '\\ud83d', '\\udc3e', '\\u2764\\n', '\\ud83d', '\\udeab', '\\u2714', '\\ufe0f', 'Follow:', '@corgidog_gemma', '\\ud83c', '\\udf1f', '\\u21c7', '\\u21c7', '\\u21c7', 'For', 'Fun', '\\u2714', '\\ufe0f', '\\ud83d', '\\udcf7', '\\ud83d', '\\udc4c\\n', '\\ud83d', '\\udeab', '\\u2714', '\\ufe0f', 'Follow:', '@corgidog.team_rose', '\\ud83c', '\\udf1f', '\\u2b05', '\\u2b05', '\\u2b05', 'For', 'More', 'Fun', '\\u2714', '\\ufe0f', '\\ud83d', '\\udcf7', '\\ud83d', '\\udc4c\\nTag', '@corgibabyhouse', 'a', 'friend', 'who', 'needs', 'to', 'see', 'this!\\n', '\\ud83d', '\\udeab', '\\u2714', '\\ufe0f', '\\ufe0f', 'FOLLOW', 'my', 'partners:', '\\ud83d', '\\udc3e', '\\u2764', '\\ud83d', '\\udc66', '\\ud83d', '\\udc69', '\\u2764', '\\ud83d', '\\udc3e\\n@corgibabyhouse', '\\ud83c', '\\udf1f\\n@horsesspecies.club', '\\ud83c', '\\udf1f\\n@dachshund.dog.club', '\\ud83c', '\\udf1f\\n@boxerlovedog', '\\ud83c', '\\udf1f\\n@boxerdog.club', '\\ud83c', '\\udf1f\\n!!Thank', 'you', 'so', 'much', '\\ud83d', '\\udc95', '\\ud83d', '\\udc9e', '\\ud83d', '\\udc95', '!!\\n@ruby_thecorgi', '@clubfrenchbulldog.team', '@pugs.dogclub', '\\ud83d', '\\udc95', '\\ud83d', '\\udc95', '\\ud83d', '\\udc95\\n#corgi', '#corgination', '#corgisofinstagram', '#corgilove', '#corgicommunity', '#corgistagram', '#welshcorgi#corgipuppy#corgigram#corgiplanet#corgiaddict#corgistagrams#dogdailystyle', '#corgilove', '#corgi', '#corgis#corgipuppy', '#corgilover', '#corgistagram#welshcorgi', '#puppylove#dog', '#dogs#doglover', '#dogs_of_instagram#cute#corgisofinstagram', '#love#dogoftheday', '#cutedog']
#caption = x.getImages("https://www.instagram.com/explore/locations/108659242498155/")
#print(caption)


#html = urllib.request.Request("https://www.instagram.com/explore/locations/108659242498155/")
#html_page = urllib.request.urlopen(html).read()
#print(re.findall("<script text/javascript", html_page))