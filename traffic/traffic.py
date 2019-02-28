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

def help(data):
    unwanted = ['\r', '\n', '\xa0']
    for i in unwanted:
        data = data.replace(i, ' ')

    count = 0
    for i in data:
        if i.isalnum() == True:
            data = data[count:]
            break
        else:
            count += 1
    return data

def clean_desc(data):
    return help(help(data)[::-1])[::-1]

clean_desc(desc)

# Now, putting all data in a dataframe
for i in range(len(soup.find_all('li', "item clr"))):
    data = {'location':soup.find_all('li', "item clr")[i].find_all('span', 'location_name')[0].text,
    'timestamp':soup.find_all('li', "item clr")[i].find_all('span', 'timestamp')[0].text,
    'description':clean_desc(soup.find_all('li', "item clr")[i].find_all('span', 'description')[0].text)}
    if len(df) == 0:
        df = pd.DataFrame([data])
    else:
        df = df.append(pd.DataFrame([data]))

df.index = range(len(df))
