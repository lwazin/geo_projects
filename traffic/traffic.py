# Importing packages
import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests

# Processing webpage for BeautifulSoup
request = requests.get('https://m.news24.com/Traffic/Gauteng')
page = request.content
soup = bs4(page)

# Finding value within the web page
# The value we are interested in is placed within list objects, of class 'item clr'
len(soup.find_all('li', "item clr"))
# The page returns a list of 10 items.. This is traffic data

# Let's look at the data provided by a single item within this list:
soup.find_all('li', "item clr")[0].find_all('span', 'location_name')[0].text # Name
soup.find_all('li', "item clr")[0].find_all('span', 'timestamp')[0].text # TimeStamp
soup.find_all('li', "item clr")[0].find_all('span', 'description')[0].text # Description

# These values, being a sample of the crude data values we can mine.. Clearly we need to clean it up a bit!
