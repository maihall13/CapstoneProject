import requests
import json
#takes about 23 seconds for each photo


#PixLab API
# Detect all human faces present in a given image via 'facedetect' and extract each one of them via 'crop'.
# Target image: Feel free to change to whatever image holding as many human faces you want
#Paid 150K Media Anayis Calls/Month
#Unlimited Media Processing Calls

class PixLab():

    def __init__(self):
        self.counter = 0
        #file = open("pixlabkey.txt", "r")
        #key = file.readline()
        #file.close()
        #self.key = key
        self.key = "c85e690af325004980fef50d15f7e1cc"

    def getImages(self, image_list):
        self.new_image_list = []

        for image in image_list:
            if len(self.new_image_list) >= 5:
                break
            else:
                self.isFace(image)
            self.counter = self.counter + 1

        return self.new_image_list

    def getCount(self):
        return self.counter

    def clearCount(self):
        self.counter = 0

    def isFace(self, image):
        req = requests.get('https://api.pixlab.io/facedetect', params={
            'img': image,
            'key': self.key,
        })
        reply = req.json()
        error = reply['status']
        list_len = reply['faces']

        if error != 200:
            return False
        else:
            if len(list_len) == 0:
                print(False)
                return False
            else:
                print(True)
                self.new_image_list.append(image)
                #print(len(self.new_image_list))
                return True

#Test
#try:
#    detect = PixLab()
#    detect.isFace('https://scontent-lga3-1.cdninstagram.com/t51.2885-15/s750x750/sh0.08/e35/23668209_2425341327691298_6197593084633546752_n.jpg')
#except Exception as e:
#    print(e)
#detect.isFace('https://scontent-lga3-1.cdninstagram.com/t51.2885-15/e35/23823358_238134726720341_8311411688045805568_n.jpg')
#detect.isFace('https://scontent-lga3-1.cdninstagram.com/t51.2885-15/e35/23734920_1789845404642131_827001600726794240_n.jpg')