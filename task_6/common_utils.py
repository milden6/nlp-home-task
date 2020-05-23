from operator import itemgetter  # for sort
import re
import numpy as np
import os


# normalize a vector to be a probablistic representation
def normalize(vector):
    s = sum(vector)
    assert (abs(s) != 0.0)  # the sum must not be 0

    for i in range(len(vector)):
        assert (vector[i] >= 0)  # element must be >= 0
        vector[i] = vector[i] * 1.0 / s


#  print topic-word distribution to file and list top n most probable words for each topic
def print_topic_word_distribution(topic_word_prob, vocabulary, number_of_topics, topn, filepath):
    V = len(vocabulary)  # size of vocabulary
    assert (topn < V)
    f = open(filepath, "w")
    for k in range(number_of_topics):
        word_prob = topic_word_prob[k, :]
        word_index_prob = []
        for i in range(V):
            word_index_prob.append([i, word_prob[i]])
        word_index_prob = sorted(word_index_prob, key=itemgetter(1), reverse=True)  # sort by word count
        f.write("Topic #" + str(k) + ":\n")
        for i in range(topn):
            index = word_index_prob[i][0]
            f.write(vocabulary[index] + " ")
        f.write("\n")

    f.close()


# print document-topic distribution to file and list top n most probable topics for each document
def print_document_topic_distribution(document_topic_prob, documents, number_of_topics, topn, filepath):
    assert (topn <= number_of_topics)
    f = open(filepath, "w")
    D = len(documents)  # number of documents
    for d in range(D):
        topic_prob = document_topic_prob[d, :]
        topic_index_prob = []
        for i in range(number_of_topics):
            topic_index_prob.append([i, topic_prob[i]])
        topic_index_prob = sorted(topic_index_prob, key=itemgetter(1), reverse=True)
        f.write("Document #" + str(d) + ":\n")
        for i in range(topn):
            index = topic_index_prob[i][0]
            f.write("topic" + str(index) + " ")
        f.write("\n")

    f.close()


# construct a list of unique words in the corpus.
def build_vocabulary(documents):
    discrete_set = set()
    for document in documents:
        for word in document:
            discrete_set.add(word)
    vocabulary = list(discrete_set)
    return vocabulary


# split file into an ordered list of words.
def split(stop_words_set, filepath):
    words_list = []
    file = open(filepath)
    try:
        lines = [line for line in file]
    finally:
        file.close()

    for line in lines:
        words = line.split(' ')
        for word in words:
            clean_word = _clean_word(word)
            if clean_word and (clean_word not in stop_words_set) and (len(clean_word) > 1):  # omit stop words
                words_list.append(clean_word)
    return words_list, lines


# preprocessing
def _clean_word(word):
    punctuation = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*']
    carriage_returns = ['\n', '\r\n']

    word = word.lower()
    for punc in punctuation + carriage_returns:
        word = word.replace(punc, '').strip("'")
    return word if re.match("^[a-z']+$", word) else None


def read_consistent_wordsim(path, matrix_keys):
    wordsim_lines = open(path).readlines()
    wordsim_consistent = []

    for words_line in wordsim_lines:
        words_list = words_line.split('\t')
        del words_list[2]
        if words_list[0] in matrix_keys and words_list[1] in matrix_keys:
            wordsim_consistent.append(words_list)
    return wordsim_consistent

#  measure of similarity between two non-zero vectors by cos
def cosine_similarity(a, b):
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cosine = dot / (norma * normb)
    return cosine

# measure of similarity between two non-zero vectors by scalar
def scalar(a, b):
    length = min(a.shape[0], b.shape[0])
    scalar = 0
    for i in range(0, length):
        scalar = scalar + a[i]*b[i]
    return scalar

def write_file(filename, data):
    write = open(filename, "w")
    str = '\n'

    str = str.join(data)

    write.write(str)
    write.close()


def get_texts_list(path):
    texts_list = []

    for file in os.walk(path):
        file[2].sort(key=lambda f: int(re.sub('\D', '', f)))
        for f in file[2]:
            text = open(path + f, "r").read()
            texts_list.append(text)

    return texts_list


def get_sentences(text):
    pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    return pattern.findall(text)


def get_sentences_list(texts_list):
    sentences_list = []

    for text in texts_list:
        sentences_list.extend(get_sentences(text))

    return sentences_list

# split file into an ordered list of words.
def words_splitter(stop_words_set, sentences):
    words_list = []

    for sentence in sentences:
        words = sentence.split(' ')
        for word in words:
            clean_word = _clean_word(word)
            if clean_word and (clean_word not in stop_words_set) and (len(clean_word) > 1):  # omit stop words
                words_list.append(clean_word)
    return words_list