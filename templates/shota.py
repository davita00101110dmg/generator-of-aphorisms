import requests
from bs4 import BeautifulSoup
import random

url = 'https://sites.google.com/site/mygeolingua/aporizmebi-vepkhistqaosnidan'
r = requests.get(url)
c = r.text


def quotes():
    sia = []
    soup = BeautifulSoup(c, 'html.parser')
    quotes = soup.find('tbody')
    all_quotes = quotes.find_all('li')
    for each in all_quotes:
        quote = each.find('p').text
        sia.append(quote)
    return sia[random.randint(0, 64)]
