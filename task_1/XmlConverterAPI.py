from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

class Converter:

    BLOCK = "block"
    TEXT = "text"

    def createXML(list, write_path):
        root = Element("doc")

        for line in list:
            #Block
            if line.name == Converter.BLOCK:
                appt = Element("block", name = line.value)
                root.append(appt)
            #Text
            if line.name == Converter.TEXT:
                begin = SubElement(appt, "text")
                begin.text = line.value

        rough_string = ElementTree.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ")

        with open(write_path, "w") as fh:
            fh.writelines(pretty_str)

class Structure:
    def __init__(self, name, value):
        self.name = name
        self.value = value