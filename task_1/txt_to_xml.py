from XmlConverterAPI import Converter, Structure

file = open("Files/ForText", "r")

list = []

for line in file.readlines():
    if line.__contains__(":"):
        line = line.replace(' ', '_')
        line = line.replace(':', '')
        line = line.replace('\n', '')
        list.append(Structure(name=Converter.BLOCK, value=line))
    if line.__contains__("-"):
             line = line.replace(' ', '')
             line = line.replace('-', '')
             line = line.replace('\n', '')
             list.append(Structure(name=Converter.TEXT, value=line))

Converter.createXML(list, "FromText_XML.xml")