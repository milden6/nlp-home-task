import os
import glob
import common_utils
import plsa
import pandas as pd
import numpy as np

stop_words_set = set()

# load stop words list from file
stopwordsfile = open("stopwords.txt", "r")
for word in stopwordsfile:  # a stop word in each line
    word = word.replace("\n", '')
    word = word.replace("\r\n", '')
    stop_words_set.add(word)

# iterate over the files in the directory.
document_paths = ['./Files/']
documents = []
for document_path in document_paths:
    for document_file in glob.glob(os.path.join(document_path, '*.txt')):
        words, lines = common_utils.split(stop_words_set, document_file)  # tokenize
        documents.append(words)

vocabulary = common_utils.build_vocabulary(documents)

number_of_topics = 3
max_iterations = 1

topic_word_prob, document_topic_prob = plsa.plsa(number_of_topics, max_iterations, documents)

common_utils.print_topic_word_distribution(topic_word_prob, vocabulary,
                                           number_of_topics, 3, "./topic-word.txt")
common_utils.print_document_topic_distribution(document_topic_prob, documents,
                                               number_of_topics, 3, "./document-topic.txt")

path_wordsim = './wordsim353_sim_rel/wordsim_similarity_goldstandard.txt'
data_cos = []
data_scalar = []

plsa_matrix = pd.DataFrame(data=topic_word_prob, columns=vocabulary)

consistent_wordsim = common_utils.read_consistent_wordsim(path_wordsim, vocabulary)

for item in consistent_wordsim:
    vector1 = plsa_matrix.get(item[0]).values
    vector2 = plsa_matrix.get(item[1]).values
    vec1 = np.array([vector1])
    vec2 = np.array([vector1])
    vec1 = vec1[~np.isnan(vec1)]
    vec2 = vec2[~np.isnan(vec2)]
    number_cos = common_utils.cosine_similarity(vec1, vec2)
    number_scalar = common_utils.scalar(vec1, vec2)

    # PLSA model
    data_cos.append('{}\t{}\t{}'.format(item[0], item[1], number_cos))
    data_scalar.append('{}\t{}\t{}'.format(item[0], item[1], number_scalar))

#  write to file
common_utils.write_file('data_plsa_cos', data_cos)
common_utils.write_file('data_plsa_scalar', data_scalar)

