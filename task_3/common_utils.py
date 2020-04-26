import tokenizator
import os

# create dict from text with key and value(word count)
def create_dict(text):
    words_dict = {}

    words_list = tokenizator.get_words(text)

    for word in words_list:
        if word in words_dict:
            word_count = words_dict.get(word)
            words_dict[word] = word_count + 1
        if word not in words_dict:
            words_dict[word] = 1

    return words_dict


# read all texts into list
def get_texts_list(path):
    texts_list = []

    for file in os.walk(path):
        for f in file[2]:
            text = open(path + f, "r").read().lower()
            texts_list.append(text)

    return texts_list

def write_file(filename, data):
    write = open(filename, "w")
    str = '\n'

    str = str.join(data)

    write.write(str)
    write.close()