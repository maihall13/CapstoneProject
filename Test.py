from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
url = "https://www.pinterest.com/search/pins/?q=outfit&rs=typed&term_meta[]=outfit%7Ctyped"
soup = BeautifulSoup(urlopen(url).read(), 'html.parser')

images = []
#print(soup.prettify())
for link in soup.find_all('a'):
    #print(link)
    title_start = str(link).find("title")
    title_end = str(link).find("img")

    print(str(link)[title_start+7:title_end-3])
    redirect_start = str(link).find("href")
    redirect_end = str(link).find("style")
    print(str(link)[redirect_start+6:redirect_end-1])

    image_start = str(link).find("src")
    image_end = str(link).find("srcset")
    print(str(link)[image_start+5:image_end-1])
    try:
        images.append(str(link)[image_start+5:image_end-1])
    except:
        break
    print("\n")

#print(images)
"""