import Geocoding
import Weather
import PixLab
import ThreadGenius
import Pinterest
import Instagram
import Jacket


class Alchemy():
    def __init__(self, location, option):
        self.option = str(option).lower()
        # Get location - will need validation on webpage
        # Get coordinates
        self.location = location
        latlon = Geocoding.Geocoding().getLocation(location)
        lat = str(latlon["lat"])
        long = str(latlon["lng"])

        self.instaList = []

        # Get pictures from location (AKA Instagram)
        insta = Instagram.Instagram()
        if location == "chicago, il" or location =="chicago,il":
            while len(self.instaList) < 3:
                location = "millennium park,chicago"
                latlong = {'lat': 41.8825524, 'lng': -87.62255139999999}
                url = insta.getURL(latlong, location)
                images = insta.getImages(url)
                images = list(set(images))
                self.instaList = images

                location = "navy pier,chicago"
                latlong = {'lat': 41.89161379999999, 'lng': -87.60789869999999}
                url = insta.getURL(latlong, location)
                set2 = insta.getImages(url)
                set2 = list(set(set2))

                for picture in set2:
                    self.instaList.append(picture)

                latlong = {'lat': 41.8871481, 'lng': -87.63278319999999}
                location = "chicago riverwalk, chicago"
                url = insta.getURL(latlong, location)
                set3 = insta.getImages(url)
                set3 = list(set(set3))

                for picture3 in set3:
                    self.instaList.append(picture3)
        elif location == "minneapolis, mn" or location =="minneapolis,mn":
            location = "minnehaha park,minneapolis"
            latlong = {'lat': 44.9153307, 'lng': -93.21100059999999}
            url = insta.getURL(latlong, location)
            images = insta.getImages(url)
            images = list(set(images))
            self.instaList = images

            location = "uptown,minneapolis"
            latlong = {'lat': 44.9489637, 'lng': -93.29986889999999}
            url = insta.getURL(latlong, location)
            set2 = insta.getImages(url)
            set2 = list(set(set2))

            for picture in set2:
                self.instaList.append(picture)

            latlong = {'lat': 44.9695478, 'lng': -93.2897804}
            location = "minneapolis sculpture garden, minneapolis"
            url = insta.getURL(latlong, location)
            set3 = insta.getImages(url)
            set3 = list(set(set3))

            for picture3 in set3:
                self.instaList.append(picture3)

        else:
            while len(self.instaList) < 3:
                url = insta.getURL(latlon, location)
                self.instaList = insta.getImages(url)

        self.count = 0


    def runAlchemy(self):
        pictures = self.getPictures()
        return pictures

    def getPictures(self):
        imagelist = self.instaList
        print(imagelist)
        # From list determine if face - returns list of images with faces
        self.detect = PixLab.PixLab()

        img_clothes = self.detect.getImages(imagelist)
        self.count = self.detect.getCount()
        self.detect.clearCount()

        # For each image get a list of keywords to search
        details = ThreadGenius.TGenius()
        clothing_details = details.getDetails(img_clothes)
        print(clothing_details)

        # For each of the keywords search Pinterest and get results of outfit ideas
        pins = Pinterest.Pinterest()

        final_list = (pins.getAllImages((clothing_details), self.option))
        # remove special keywords for validation
        if self.option == "men":
            remove_words = ["hunt", "women", "woman", "gifts", "girl", "birthday", "girls", "cute",
                            "wedding", "handbag", "bags", "handbags", "country", "fedoras", "fedora", "beadwork",
                            "necklace",
                            "jewelry", "bag",
                            "https://i.pinimg.com/236x/45/84/78/4584782ae4da98d5a43924682bb534dc.jpg", "cookie",
                            "cookies", "gingerbread", "captain"]
            final_list = set(final_list) - {i for e in remove_words for i in final_list if e in i}
        elif self.option == "women":
            remove_words = ["hunt", "men", "man", "boy", "gifts", "father", "girl", "birthday", "dad",
                            "wedding", "handbag", "bags", "handbags", "country", "fedoras", "fedora", "beadwork",
                            "necklace",
                            "jewelry", "bag",
                            "https://i.pinimg.com/236x/45/84/78/4584782ae4da98d5a43924682bb534dc.jpg"]
            final_list = set(final_list) - {i for e in remove_words for i in final_list if e in i}
        final_list = list(final_list)

        try:
            jacket = Jacket.Jacket()
            if jacket.jacketWorthy(self.location):
                refine_list = ["crop", "bikini", "swim", "summer"]
                final_list = set(final_list) - {i for e in refine_list for i in final_list if e in i}
                final_list = list(final_list)
            else:
                refine_list = ["jacket", "winter", "sweater"]
                final_list = set(final_list) - {i for e in refine_list for i in final_list if e in i}
                final_list = list(final_list)
        except Exception as e:
            print("jacket error")
            print(e)

        final_list = list(set(final_list))
        pictures = []
        for i in final_list:
            pictures.append([i])
        composite_list = [final_list[x:x + 5] for x in range(0, len(final_list), 5)]

        print(composite_list)
        return composite_list



    def updatedInstaList(self):
        # For future use if pictures are too little
        self.instaList = self.instaList[self.count:]
        return self.instaList

#al = Alchemy("chicago, il", "women")
#print(al.getPictures())

#jacket = Jacket.Jacket()
#answer = jacket.jacketWorthy("chicago,il")
#print(answer)

#pics = ['https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24838396_799299326916706_8798709533464592384_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25009308_1477007359079029_7696313053465280512_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24331830_143893656264376_8386001062225510400_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24331870_155537815201586_8085452951797104640_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25006955_1929008030759906_6663727238183124992_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25009569_1695509310467412_7686529710670479360_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25014538_2091827191050000_3275648656170024960_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24845505_194973874394921_4514085601045118976_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24331767_1522897707758925_5166220202475520000_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25006815_1920797804836949_764215324957474816_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25010896_131250784232222_3031526168219090944_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25006761_501523263564883_9148000261367660544_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25012235_172273743364504_4431772651601526784_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25008593_170832833658623_1736397441743192064_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25008864_1794366583908299_7778942928545644544_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25005169_133097530699137_5518126247634272256_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25013738_325558167923730_5362566191485288448_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24332267_136344883666122_826199726037663744_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25006272_2095623347335253_276601872456876032_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25013137_127154821399375_3294428851643351040_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25009795_540603769620585_7515873441476509696_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24838636_152378848726105_6375370358064676864_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25009185_158078051469273_6765380352346161152_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25005337_334217803727545_37009239268392960_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24274783_924564811040028_5111099227853815808_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24327546_539616509730189_6883325780701478912_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24177959_190358504860346_4673882217229844480_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24125470_133408877372520_6042752207873376256_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24274153_957539794384765_6282312027511717888_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/25008262_133203827322256_1846168598146449408_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24254406_135893530445463_7282588839640563712_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24327979_121705691948946_5790630420643053568_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24253980_148612309101109_2780749229738426368_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24274619_1978693652390076_2046052613710938112_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24274732_518920901796287_1927576997412732928_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24274221_148115995909676_5891056054627729408_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24177738_375116012947531_4773757051723579392_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24838298_1318615971600385_5645234198441623552_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24274170_171097250298413_8754009747230818304_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24177582_325219921288133_645884663805509632_n.jpg', 'https://scontent-ort2-1.cdninstagram.com/t51.2885-15/e35/24175051_893697220805208_5806279524828053504_n.jpg']

#for p in pics:
#    print(p.)