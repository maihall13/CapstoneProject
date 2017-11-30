import Geocoding
import Weather
import PixLab
import ThreadGenius
import Pinterest
import Instagram
import Jacket

class Alchemy():
    def __init__(self, location):
        # Get location - will need validation on webpage
        # Get coordinates
        self.location = location
        latlon = Geocoding.Geocoding().getLocation(location)
        lat = str(latlon["lat"])
        long = str(latlon["lng"])

        # Get pictures from location (AKA Instagram)
        test_list = Instagram.Instagram()
        url = test_list.getURL(latlon, location)
        self.instaList = test_list.getImages(url)
        self.count = 0

    def runAlchemy(self):
        pictures = self.getPictures(self.updatedInstaList())
        return pictures

    def getPictures(self, image_list):
        # From list determine if face - returns list of images with faces
        self.detect = PixLab.PixLab()

        img_clothes = self.detect.getImages(image_list)
        self.count = self.detect.getCount()
        self.detect.clearCount()

        # For each image get a list of keywords to search
        details = ThreadGenius.TGenius()
        clothing_details = details.getDetails(img_clothes)

        # For each of the keywords search Pinterest and get results of outfit ideas
        pins = Pinterest.Pinterest()
        final_list = (pins.getAllImages((clothing_details)))

        # remove special keywords for validation
        remove_words = ["hunt", "men", "man", "boy", "gifts", "father", "girl", "birthday", "dad", "wedding"]
        final_list = set(final_list) - {i for e in remove_words for i in final_list if e in i}
        final_list = list(final_list)

        jacket = Jacket.Jacket()
        if jacket.jacketWorthy(self.location):
            refine_list = ["crop", "bikini", "swim", "summer"]
            final_list = set(final_list) - {i for e in refine_list for i in final_list if e in i}
            final_list = list(final_list)
        else:
            refine_list = ["jacket", "winter", "sweater"]
            final_list = set(final_list) - {i for e in refine_list for i in final_list if e in i}
            final_list = list(final_list)

        final_list = list(set(final_list))
        return (final_list)


    def updatedInstaList(self):
        # For future use if pictures are too little
        self.instaList = self.instaList[self.count:]
        return self.instaList