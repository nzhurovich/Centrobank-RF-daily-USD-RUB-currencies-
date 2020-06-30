import pandas as pd
import lxml
import requests
from bs4 import BeautifulSoup
import codecs
import datetime


def today():
    dt = datetime.datetime.today()
    year = dt.year
    month = dt.month
    day = dt.day
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)

    return str(day), str(month), str(year)


date = today()

url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/04/2011&date_req2={}/{}/{}&VAL_NM_RQ=R01235'.format(
    date[0], date[1], date[2])

response = requests.get(url)
with open('feed.xml', 'wb') as file:
    file.write(response.content)

soup = BeautifulSoup(codecs.open('feed.xml', "r", "utf_8_sig").read(), 'lxml')

values = []
for s in soup.find_all('record'):
    values.append(s.find('value').get_text())

dates = []
for s in soup.find_all('record'):
    tmp = str(s)
    dates.append(tmp[14:24])

data = pd.DataFrame()
data['date'] = dates
data['USD'] = values

data.to_excel('USD_RUB_CBRF.xls')
