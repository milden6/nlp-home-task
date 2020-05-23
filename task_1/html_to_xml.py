from bs4 import BeautifulSoup
from urllib.request import urlopen
from XmlConverterAPI import Structure, Converter
import re

list = []
url = 'https://lifehacker.ru/5-trendov-prilozhenij/'

rs = urlopen(url)
root = BeautifulSoup(rs, 'html.parser')

pattern = '<.*?>'

regex = re.compile(r'{}'.format(pattern))

#title
title = root.find_all('title')
title = regex.sub('', str(title))

list.append(Structure(name=Converter.BLOCK, value="tag title"))
list.append(Structure(name=Converter.TEXT, value=title))

#h3
for h3 in root.find_all('h3'):
    h3 = regex.sub('', str(h3))

    list.append(Structure(name=Converter.BLOCK, value="tag h3"))
    list.append(Structure(name=Converter.TEXT, value=h3))
#p
for p in root.find_all('p'):
    p = regex.sub('', str(p))

    list.append(Structure(name=Converter.BLOCK, value="tag p"))
    list.append(Structure(name=Converter.TEXT, value=p))

Converter.createXML(list, "FromHtml_XML.xml")