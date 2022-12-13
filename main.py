from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib

url = 'https://www.greyogregames.com/search?q=*rhystic+study*'

page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
result = soup.find_all(class_="buyWrapper")
print(result)

pattern = '<div class="buyWrapper">'


