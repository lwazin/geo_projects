# Importing packages
import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests

# Processing webpage for BeautifulSoup
request = requests.get('https://m.news24.com/Traffic/Gauteng')
page = request.content
soup = bs4(page)
