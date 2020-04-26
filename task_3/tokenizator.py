import re


def get_words(text):
    return re.findall(r'\b\S+\b', text)


def get_sentences(text):
    pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    return pattern.findall(text)


def unique_words(list):
    list_uniq = []
    for word in list:
        if word not in list_uniq:
            list_uniq.append(word)
    return list_uniq
