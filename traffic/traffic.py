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
name = soup.find_all('li', "item clr")[1].find_all('span', 'location_name')[0].text # Name
ts = soup.find_all('li', "item clr")[1].find_all('span', 'timestamp')[0].text # TimeStamp
desc = soup.find_all('li', "item clr")[0].find_all('span', 'description')[0].text # Description

# The name as it is seems clean, the timestamp too.. Our focus is on the description!
unwanted = ['\r', '\n', '\xa0']
for i in unwanted:
    desc = desc.replace(i, ' ')

count_pos = 0
for i in desc:
    if i.isalnum() == True:
        desc = desc[count_pos:]
        break
    else:
        count_pos += 1

count_pos = 0
desc = desc[::-1]
for i in desc:
    if i.isalnum() == True:
        desc = desc[count_pos:]
        break
    else:
        count_pos += 1

desc = desc[::-1]



desc
