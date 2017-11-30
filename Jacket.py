#check if its sweather worthy
from bs4 import BeautifulSoup
from urllib.request import urlopen

class Jacket:
    def jacketWorthy(self, place):
        place = place.replace(",","-")
        url = "https://doineedajacket.com/weather/" + place
        soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
        verdict = soup.find("h1").getText()
        if verdict == "Yes":
            return True
        else:
            return False


#jacket = Jacket()
#location = "chicago,il"

#if jacket.jacketWorthy(location):
#    print("true")
#else:
#    print("false")