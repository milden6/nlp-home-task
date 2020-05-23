from docx2python import docx2python
from XmlConverterAPI import Structure, Converter
import re

file = docx2python('Files/ForDocx.docx')
list = []

pattern = '\[|\]|\''
regex = re.compile(r'{}'.format(pattern))

doc = str(file.document).split("',")

for line in doc:
    line = regex.sub('', line)

    if '.' not in line and (line.count(' ')) <= 9:
        list.append(Structure(name=Converter.BLOCK, value=line))
    else:
        list.append(Structure(name=Converter.TEXT, value=line))

Converter.createXML(list, "FromDocx_XML.xml")