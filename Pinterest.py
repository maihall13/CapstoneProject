from bs4 import BeautifulSoup
import webbrowser
from urllib.request import urlopen
app_secret = "d3a22eeb4aefa8b56239332a1361442b8297e9435915b55194f4f83704c30526"
app_id = "4934510159606072512"


class Pinterest():
    def createURL(self, searchphrase, option):
        keywords = searchphrase.split()
        url = "https://www.pinterest.com/search/pins/?q=winter%20"

        for index in range(len(keywords)):
            url = url  + keywords[index] + str("%20")

            if option == "women":
                url = url + "women&rs=typed%term_meta[]=winter%7Ctyped"

                for index in range(len(keywords)):
                    url = url  + "&term_meta[]=" + keywords[index] + str("%7Ctyped")

                url = url + "&term_meta[]=womens%7Ctyped"
                return (url)
            elif option == "men":
                url = url + "men&rs=typed%term_meta[]=winter%7Ctyped"

                for index in range(len(keywords)):
                    url = url + "&term_meta[]=" + keywords[index] + str("%7Ctyped")

                url = url + "&term_meta[]=men%7Ctyped"
                return (url)




    def getImage(self, searchphrase, option):
        url = self.createURL(searchphrase, option)
        soup = BeautifulSoup(urlopen(url, timeout=15).read(), 'html.parser')
        images = []
        for link in soup.find_all('a'):
            for l in soup.find_all('img'):
                images.append(l.get("src"))
        return (images[:5])

    def getAllImages(self, details_list, option):
        all_pics = []
        for keywords in details_list:
            images = self.getImageList(keywords, option)
            for i in images:
                all_pics.append(i)

        return list(set(all_pics))

    def getImageList(self, keywords, option):
        set_one = keywords[0]
        set_two = keywords[1]
        set_three = keywords[2]

        images = []
        for key in set_one:
            img = self.getImage(key, option)
            if not img:
                break
            else:
                for i in img:
                    images.append(i)

        if not images:
            for key in set_two:
                img = self.getImage(key, option)
                if not img:
                    break
                else:
                    for i in img:
                        images.append(i)

        return images


#pins = Pinterest()
#search_word = ['color blocked beanie long sleeved grey', 'mink cardigan', 'leather sleeved cardigan','dark green cardigan', 'sequin varsity sweatshirt',  'cold shoulder silver sweatshirt']
#search_word = ['color blocked beanie long sleeved color grey']

#search_word = [[['beaded peruvian hat vneckline rust ', 'beaded bomber hat vneckline rust ', 'beaded bucket hat vneckline rust '], ['beaded bucket hat ', 'beaded peruvian hat ', 'beaded bomber hat '], ['vneckline bomber hat ', 'vneckline peruvian hat ', 'vneckline bucket hat ']], [['long sleeved silver ', 'bell sleeves beige '], [''], ['bell sleeves ', 'long sleeved ']], [['color blocked cardigan turtleneck purple ', 'burberry house check design aviator sunglasses shawl collar purple '], ['color blocked cardigan ', 'burberry house check design aviator sunglasses '], ['turtleneck cardigan ', 'shawl collar aviator sunglasses ']], [['camouflage bucket hat amethyst blue ', 'camouflage peruvian hat blue topaz yellow ', 'camouflage beanie blue topaz yellow '], ['camouflage beanie ', 'camouflage peruvian hat ', 'camouflage bucket hat '], ['blue topaz peruvian hat ', 'amethyst bucket hat ', 'blue topaz beanie ']], [['buffalo plaid plaid shirt long sleeved red '], ['buffalo plaid plaid shirt '], ['long sleeved plaid shirt ']]]
#print(pins.getAllImages(search_word, "women"))


"""
et_one = []
# first tier
for key0 in keywords[0]:
    img0 = self.getImage(key0)
    if not img0:
        break
    else:
        set_one.append(img0)

# second tier
set_two = []
if not set_one:
    for key1 in keywords[1]:
        img1 = self.getImage(key1)
        # print(img)
        if not img1:
            break
        else:
            set_two.append(img1)

# third tier
set_three = []
if not set_two:
    for key2 in keywords[2]:
        img2 = self.getImage(key2)
        if not img2:
            break
        else:
"""