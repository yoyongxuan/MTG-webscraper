from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re

url = 'https://www.greyogregames.com/search?q=*cultivate*'

page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
result = soup.find_all("div",class_="product Norm")
for product in result:
    for card in product.find_all("div", class_= "addNow single"):
        onclick = card['onclick']
        addToCart = onclick[10:-1].split(',')
        name = addToCart[1]
        print(name)

        price = int(re.sub(r'[^0-9]', '', card.p.get_text()))
        print(price)

        print('\n\n')
    



