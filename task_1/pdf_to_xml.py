from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from XmlConverterAPI import Converter, Structure

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

text = convert_pdf_to_txt('Files/FromPdf.pdf')

text = text.replace("","")

list = []

for line in text.split("\n"):
    #if line == '':
     #   break
    if '.' not in line and (line.count(' ')) <= 4:
        list.append(Structure(name=Converter.BLOCK, value=line))
    else:
        list.append(Structure(name=Converter.TEXT, value=line))

Converter.createXML(list, 'FromPdf_XML.xml')