import common_utils
import word_matrix
import numpy as np

# wordsim path
path_wordsim = './wordsim353_sim_rel/wordsim_similarity_goldstandard.txt'
data = []

# read texts into list
texts_list = common_utils.get_texts_list('./Files/')

# get sentences list from texts list
sentences_list = common_utils.get_sentences_list(texts_list)

# build co-occurrence matrix
co_occurrence_matrix = word_matrix.co_occurrence(sentences_list)

# PPMI
ppmi = word_matrix.ppmi(co_occurrence_matrix)

# words dict
matrix_keys_list = co_occurrence_matrix.keys()

# it's mean that my words included in wordsim353
consistent_wordsim = common_utils.read_consistent_wordsim(path_wordsim, matrix_keys_list)

# get vector 1 and vector 2 for each word and comp.
# cosine similarity
for item in consistent_wordsim:
    vector1 = ppmi.get(item[0]).values
    vector2 = ppmi.get(item[1]).values
    vec1 = np.array([vector1])
    vec2 = np.array([vector2])
    vec1 = vec1[~np.isnan(vec1)]
    vec2 = vec2[~np.isnan(vec2)]
    number = word_matrix.cosine_similarity(vec1, vec2)
    data.append('{}\t{}\t{}'.format(item[0], item[1], number))

#  write to file
common_utils.write_file('my_words', data)
