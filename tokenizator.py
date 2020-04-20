import re
import string


def get_words(text):
    text = str(re.sub('[' + string.punctuation + ']', string.whitespace, text).split())
    return str(re.sub(r'[^A-Za-z,]', ',', text))


def get_sentences(text):
    pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    return pattern.findall(text)
