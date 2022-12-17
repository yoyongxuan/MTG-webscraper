from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re
import csv

def write_to_file(filename,nestedlist):
    with open(filename,'w',newline='') as f:
        csv_writer = csv.writer(f)
        for listing in nestedlist:
            csv_writer.writerow(listing)
            print(listing)

#url = 'https://www.greyogregames.com/search?q=*rhystic+study*'
url = 'https://www.greyogregames.com/search?q=*cultivate*'
#url = 'https://www.greyogregames.com/collections/mtg-singles-all-products'

def greyogregames_scrape_page(url):
    print(url)
    cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find_all("div",class_="product Norm")
    for product in product_list:
        

        name_set = product.find('p',class_="productTitle").get_text()
        set = re.findall('\[(.*?)\]', name_set)[0].strip()
        name = re.sub('\[(.*?)\]','', name_set).strip()

        # print("Product")
        # print(product.prettify())
        # print("\n\n")
        

        available_cards = product.find("div", class_= "hoverMask").find_all("div",class_="addNow single")
        for card in available_cards:
            quality_foil,price = card.p.get_text().split('-')
            price = int(re.sub(r'[^0-9]', '', price))
            quantity = card["onclick"].split(',')[-2]
            if 'Foil' in quality_foil:
                foil = True
                quality = quality_foil.replace('Foil','').strip()
            else:
                foil = False
                quality = quality_foil
            
            
            print("Card")
            print(card.prettify())
            print([name,set,quality,foil,price,quantity])
            print(foil)
            print("\n\n")
            
            cardlist.append([name,set,quality,foil,price,quantity])
            
            
        if len(available_cards) == 0:
            cardlist.append([name,None,None,None,"Sold Out",0])
            
            
    next_page = soup.find_all("a",class_="pagination-item pagination-next")
    if len(next_page) > 0:
        next_page_url = 'https://www.greyogregames.com' + next_page[0]['href']
    else:
        next_page_url = None      
        # print(name)
        # print(price)
        # print('\n\n')
    return cardlist,next_page_url


def greyogregames_scraper(url):
    greyogregames_cardlist = []
    while url != None:
        cardlist,url = greyogregames_scrape_page(url)
        greyogregames_cardlist.extend(cardlist)

    return greyogregames_cardlist


greyogregames_cardlist = greyogregames_scraper(url)
write_to_file("greyogregames_cardlist.csv",greyogregames_cardlist)
print(greyogregames_cardlist)

# url = "https://cardscitadel.com/search?q=*cultivate*"
# cardcitadel_cardlist = greyogregames_scraper(url)
# print(cardcitadel_cardlist)
# write_to_file("cardcitadel_cardlist.csv",cardcitadel_cardlist)


