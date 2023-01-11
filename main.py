from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re
import csv
import json

def write_to_file(filename,nestedlist):
    with open(filename,'w',newline='') as f:
        csv_writer = csv.writer(f)
        for listing in nestedlist:
            csv_writer.writerow(listing)
            print(listing)

#url = 'https://www.greyogregames.com/search?q=*rhystic+study*'
#url = 'https://www.greyogregames.com/search?q=*kogla*'
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
            condition_foil,price = card.p.get_text().split('-')
            price = int(re.sub(r'[^0-9]', '', price))
            quantity = card["onclick"].split(',')[-2]
            if 'Foil' in condition_foil:
                foil = True
                condition = condition_foil.replace('Foil','').strip()
            else:
                foil = False
                condition = condition_foil.strip()
            
            
            # print("Card")
            # print(card.prettify())
            # print([name,set,condition,foil,price,quantity])
            # print(foil)
            # print("\n\n")
            
            cardlist.append([name,set,condition,foil,price,quantity])
            
            
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


# greyogregames_cardlist = greyogregames_scraper(url)
# write_to_file("greyogregames_cardlist.csv",greyogregames_cardlist)
# print(greyogregames_cardlist)

# url = "https://cardscitadel.com/search?q=*cultivate*"
# cardcitadel_cardlist = greyogregames_scraper(url)
# print(cardcitadel_cardlist)
# write_to_file("cardcitadel_cardlist.csv",cardcitadel_cardlist)

def manapro_scrape_page(url):
    print(url)
    cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    product_list = soup.find("ul",id="main-collection-product-grid").find_all("script")
    for product in product_list:
        script = product.get_text()
        script = script.split('\n')
        script = script[2].strip("product = ,",)
        products = json.loads(script)
        variants = products["variants"]
        for variant in variants:
            #print(variant)
            name = variant['name']
            sku = variant['sku']
            price = variant['price']
            cardlist.append([name,sku,price])
        
    
        

#         name_set = product.find('p',class_="productTitle").get_text()
#         set = re.findall('\[(.*?)\]', name_set)[0].strip()
#         name = re.sub('\[(.*?)\]','', name_set).strip()

#         # print("Product")
#         # print(product.prettify())
#         # print("\n\n")
        

#         available_cards = product.find("div", class_= "hoverMask").find_all("div",class_="addNow single")
#         for card in available_cards:
#             quality_foil,price = card.p.get_text().split('-')
#             price = int(re.sub(r'[^0-9]', '', price))
#             quantity = card["onclick"].split(',')[-2]
#             if 'Foil' in quality_foil:
#                 foil = True
#                 quality = quality_foil.replace('Foil','').strip()
#             else:
#                 foil = False
#                 quality = quality_foil.strip()
            
            
#             # print("Card")
#             # print(card.prettify())
#             # print([name,set,quality,foil,price,quantity])
#             # print(foil)
#             # print("\n\n")
            
#             cardlist.append([name,set,quality,foil,price,quantity])
            
            
#         if len(available_cards) == 0:
#             cardlist.append([name,None,None,None,"Sold Out",0])
            
            
    next_page = soup.find("div",class_="pag_next").find_all("a")
    if len(next_page) > 0:
        next_page_url = 'https://sg-manapro.com/' + next_page[0]['href']
    else:
        next_page_url = None      
#         # print(name)
#         # print(price)
#         # print('\n\n')
    return cardlist,next_page_url


def manapro_scraper(url):
    manapro_cardlist = []
    while url != None:
        cardlist,url = manapro_scrape_page(url)
        manapro_cardlist.extend(cardlist)

    return manapro_cardlist

# url = 'https://sg-manapro.com/collections/jumpstart-2022'
# manapro_cardlist = manapro_scraper(url)
# write_to_file('manapro_cardlist.csv',manapro_cardlist)



def gameshaven_scrape_page(url):
    print(url)
    cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find_all("div",class_="productCard__card")
    for product in product_list:
        
        productCard_lower = product.find('div',class_="productCard__lower")
        name = productCard_lower.find('p',class_="productCard__title").get_text().strip()
        set = productCard_lower.find('p',class_="productCard__setName").get_text()

        # print("Product")
        # print(product.prettify())
        # print("\n\n")
        # print(set)
        # print(name)
        
        available_cards = productCard_lower.find("ul", class_= "productChip__grid").find_all("li")
        for card in available_cards:
            if card['data-variantavailable'] == 'true':
                quantity = card['data-variantqty']
                price = card['data-variantprice']
                condition_foil = card['data-varianttitle']
                
                if 'Foil' in condition_foil:
                    foil = True
                    condition = condition_foil.replace('Foil','').strip()
                else:
                    foil = False
                    condition = condition_foil.strip()
                    
                cardlist.append([name,set,condition,foil,price,quantity])
            
    #         # print("Card")
    #         # print(card.prettify())
    #         # print([name,set,quality,foil,price,quantity])
    #         # print(foil)
    #         # print("\n\n")
            
            
            
    pagination = soup.find("ol",class_="pagination")
    next_page = pagination.find_all("li")[-1]
    if next_page.has_attr('class'):
        next_page_url = None
    else:
        next_page_url = 'https://www.gameshaventcg.com/' + next_page.a['href']
    return cardlist,next_page_url

def gameshaven_scraper(url):
    gameshaven_cardlist = []
    while url != None:
        cardlist,url = gameshaven_scrape_page(url)
        gameshaven_cardlist.extend(cardlist)

    return gameshaven_cardlist
    
url = 'https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A'
#url = "https://www.gameshaventcg.com/search?page=1&q=%2A%2A"
gameshaven_cardlist = gameshaven_scraper(url)
print(gameshaven_cardlist)
write_to_file('gameshaven_cardlist.csv',gameshaven_cardlist)