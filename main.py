from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re



#url = 'https://www.greyogregames.com/search?q=*rhystic+study*'

url = 'https://www.greyogregames.com/collections/mtg-singles-all-products'


def greyogregames_scraper(url,nextpage=False):
    greyogregames_cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find_all("div",class_="product Norm")
    for product in product_list:
        for card in product.find_all("div", class_= "addNow single"):
            onclick = card['onclick']
            addToCart = onclick[10:-1].split(',')
            name = addToCart[1]
            
    
            price = int(re.sub(r'[^0-9]', '', card.p.get_text()))
    
            greyogregames_cardlist.append([name,price])

    if not nextpage:
        pagination = soup.find_all("div", id="pagination")
        if len(pagination) > 0:
            print(True)

        # print(name)
        # print(price)
        # print('\n\n')
    return greyogregames_cardlist
    
print(greyogregames_scraper(url))


