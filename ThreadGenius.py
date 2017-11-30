from threadgenius import ThreadGenius
from threadgenius.types import ImageUrlInput

#Thread Genius API used to recognize clothing keywords from a picture
#Free 10,000 monthly predictions
#Unlimited search

class TGenius():
    def __init__(self):
        file = open("threadgeniuskey.txt", "r")
        key = file.readline()
        file.close()
        self.key = key

    def getDetails(self, image_list):
        keywords=[]
        for image in image_list:
            tg = ThreadGenius(api_key=self.key)
            image = ImageUrlInput(image)
            response = tg.tag_image(image=image)

            prediction = response.get('response').get("prediction")

            self.details = []
            for k, v in prediction.items():
                if k == "data":
                    for k, v in v.items():
                        self.details = v

            keys = (self.createOutfit(self.details))
            keywords.append(keys)

        return keywords


    def createOutfit(self, imageDetails):
        pattern = []
        shape = []
        detail = []
        color = []


        for dets in imageDetails:
            for k, v in dets.items():
                if v=='pattern':
                    pattern.append(dets["name"])
                if v == "shape":
                    shape.append(dets["name"])
                if v == "detail":
                    if "sleeved" in dets["name"]:
                        word = dets["name"]
                        start = word.find("sleeved")
                        first = word[:start]
                        last = word[start:]
                        word = first + " " + last
                        detail.append(word)
                    else:
                        detail.append(dets["name"])
                if v == "color":
                    if "color" in dets["name"]:
                        start = dets["name"].find("color")
                        word = dets["name"][start + 6:]
                        color.append(word)
                    else:
                        color.append(dets["name"])


        while len(color) > len(shape) or len(color) > len(detail):
            if len(color) == len(shape) or len(color) == len(detail):
                break
            else:
                color = color[:-1]
        while len(pattern) > len(shape) or len(pattern) > len(detail):
            pattern = pattern[:-1]

        list1 = pattern, shape, detail, color

        #print("\n")

        outfits = []
        outfit_key1 = []
        for p in range(0, self.longest(list1)):
            outfit = self.findItem(pattern, p) + self.findItem(shape, p) + self.findItem(detail, p) + self.findItem(color, p)
            outfit_key1.append(outfit)

        outfits.append(list(set(outfit_key1)))
        #print(outfits)


        #print("\n")

        outfit_key2 = []
        for p in range(0, self.longest(list1)):
            outfit = self.findItem(pattern, p) + self.findItem(shape, p)
            outfit_key2.append(outfit)
            #print(outfit)

        outfits.append(list(set(outfit_key2))
)
        #print(outfits)

        #print("\n")

        outfit_key3 = []
        for p in range(0, self.longest(list1)):
            outfit = self.findItem(detail, p) + self.findItem(shape, p)
            outfit_key3.append(outfit)
        outfits.append(list(set(outfit_key3)))

        return outfits

    def longest(self, allLists):
        longest_list = max(len(elem) for elem in allLists)
        return (longest_list)

    def findItem(self, list, index):
        try:
            if index < len(list)-1:
                word = list[index]
                return word + " "
            else:
                while index > (len(list)-1):
                    index = index-1
                word = list[index]
                return word + " "

        except:
            return ""



#TEST
#detect = TGenius()
#detect.getDetails("https://instagram.ffcm1-2.fna.fbcdn.net/t51.2885-15/s640x640/sh0.08/e35/23594699_162123951058864_7638702604129665024_n.jpg")
#print(detect.getDetails(["https://scontent-lga3-1.cdninstagram.com/t51.2885-15/e35/23734920_1789845404642131_827001600726794240_n.jpg"]))
