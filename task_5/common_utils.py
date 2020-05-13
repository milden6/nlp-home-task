import re


#  SMS preprocessing, deleting blank lines and lower case unification
def text_preprocessing(text):
    reg_ex = re.compile(r'[^a-zA-Z]|\d')  # only words
    words = reg_ex.split(text)
    # Remove empty strings and to lower case
    words = [word.lower() for word in words if len(word) > 0]
    return words


#  Read sms
def read_sms(path):
    f = open(path)

    class_category = []  # Метка категории, 1 означает мусорное SMS, 0 означает обычное SMS
    sms_words = []

    for line in f.readlines():
        linedatas = line.strip().split(',')
        if linedatas[0] == 'ham':
            class_category.append(0)
        elif linedatas[0] == 'spam':
            class_category.append(1)

        words = text_preprocessing(linedatas[1])
        sms_words.append(words)
    return sms_words, class_category


#  Make corpus
def create_vocabulary_list(sms_words):
    vocabulary_set = set([])
    for words in sms_words:
        vocabulary_set = vocabulary_set | set(words)
    vocabulary_list = list(vocabulary_set)
    return vocabulary_list

#  Mark word if it in vocabulary list
def set_of_words_to_vector(vocabulary_list, sms_words):
    vocab_marked = [0] * len(vocabulary_list)
    for sms_word in sms_words:
        if sms_word in vocabulary_list:
            vocab_marked[vocabulary_list.index(sms_word)] += 1
    return vocab_marked


#  Mark word list
def set_of_words_list_to_vector(vocabulary_list, sms_words_list):

    vocab_marked_list = []
    for i in range(len(sms_words_list)):
        vocab_marked = set_of_words_to_vector(vocabulary_list, sms_words_list[i])
        vocab_marked_list.append(vocab_marked)
    return vocab_marked_list

# Write file
def write_file(filename, data):
    write = open(filename, "w")
    str = '\n'

    str = str.join(data)

    write.write(str)
    write.close()
