from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re
import csv



#url = 'https://www.greyogregames.com/search?q=*rhystic+study*'
url = 'https://www.greyogregames.com/search?q=*cultivate*'
#url = 'https://www.greyogregames.com/collections/mtg-singles-all-products'


def greyogregames_scraper(url):
    print(url)
    greyogregames_cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find_all("div",class_="product Norm")
    for product in product_list:
        # print("Product")
        # print(product)
        # print("\n\n")

        available_cards = product.find_all("div", class_= "addNow single")
        for card in available_cards:
            # print("Card")
            # print(card)
            # print("\n\n")
            onclick = card['onclick']
            addToCart = onclick[10:-1].split(',')
            name = addToCart[1]
            price = int(re.sub(r'[^0-9]', '', card.p.get_text()))
            greyogregames_cardlist.append([name,price])
            
        if len(available_cards) == 0:
            name = product.find(class_="productTitle").get_text().strip()
            greyogregames_cardlist.append([name,"Sold Out"])
            
            
    
            
    
            

    next_page = soup.find_all("a",class_="pagination-item pagination-next")
    if len(next_page) > 0:
        next_page_url = 'https://www.greyogregames.com' + next_page[0]['href']
        greyogregames_cardlist.extend(greyogregames_scraper(next_page_url))
        
        # print(name)
        # print(price)
        # print('\n\n')
    return greyogregames_cardlist


greyogregames_cardlist = greyogregames_scraper(url)

def write_to_file(filename,nestedlist):
    with open(filename,'w') as f:
        csv_writer = csv.writer(f)
        for listing in nestedlist:
            csv_writer.writerow(listing)

write_to_file("greyogregames_cardlist.csv",greyogregames_cardlist)
print(greyogregames_cardlist)


