import re
import os
import string


def get_sentences(text):
    pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    return pattern.findall(text)


def get_texts_list(path):
    texts_list = []

    for file in os.walk(path):
        file[2].sort(key=lambda f: int(re.sub('\D', '', f)))
        for f in file[2]:
            text = open(path + f, "r").read()
            texts_list.append(text)

    return texts_list


def get_sentences_list(texts_list):
    sentences_list = []

    for text in texts_list:
        sentences_list.extend(get_sentences(text))

    return sentences_list

#  text preprocessing
def sentence_preprocessing(text):
    text = text.lower()  # to lower
    text = re.sub(r'\d+', '', text)  # remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    text = text.replace('\n', ' ')  # remove new line
    text = text.replace('\t', ' ')  # remove tabulation
    text = text.replace('“', '')
    text = text.replace('•', '')
    text = text.replace('’', '')
    text = text.replace('—', '')
    text = text.replace('≥', '')
    text = ' '.join(text.split())  # leave only one space
    return text

#  this function return list of wordsim words that in my word list
def read_consistent_wordsim(path, matrix_keys):
    wordsim_lines = open(path).readlines()
    wordsim_consistent = []

    for words_line in wordsim_lines:
        words_list = words_line.split('\t')
        del words_list[2]
        if words_list[0] in matrix_keys and words_list[1] in matrix_keys:
            wordsim_consistent.append(words_list)
    return wordsim_consistent

def write_file(filename, data):
    write = open(filename, "w")
    str = '\n'

    str = str.join(data)

    write.write(str)
    write.close()