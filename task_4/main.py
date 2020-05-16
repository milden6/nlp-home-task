import common_utils
import word_matrix
import numpy as np

# wordsim path
path_wordsim = './wordsim353_sim_rel/wordsim_similarity_goldstandard.txt'
data_ppmi_cos = []
data_ppmi_scalar = []
data_lsa_cos = []
data_lsa_scalar = []

# read texts into list
texts_list = common_utils.get_texts_list('./Files/')

# get sentences list from texts list
sentences_list = common_utils.get_sentences_list(texts_list)

# build co-occurrence matrix
co_occurrence_matrix = word_matrix.co_occurrence(sentences_list)

# # PPMI
ppmi = word_matrix.ppmi(co_occurrence_matrix)
#
# # LSA
lsa = word_matrix.lsa(co_occurrence_matrix)

# words dict
matrix_keys_list = co_occurrence_matrix.keys()

# it's mean that my words included in wordsim353
consistent_wordsim = common_utils.read_consistent_wordsim(path_wordsim, matrix_keys_list)

# get vector 1 and vector 2 for each word and comp.
# cosine similarity
for item in consistent_wordsim:
    ppmi_vector1 = ppmi.get(item[0]).values
    ppmi_vector2 = ppmi.get(item[1]).values
    ppmi_vec1 = np.array([ppmi_vector1])
    ppmi_vec2 = np.array([ppmi_vector2])
    ppmi_vec1 = ppmi_vec1[~np.isnan(ppmi_vec1)]
    ppmi_vec2 = ppmi_vec2[~np.isnan(ppmi_vec2)]
    ppmi_number_cos = word_matrix.cosine_similarity(ppmi_vec1, ppmi_vec2)
    ppmi_number_scalar = word_matrix.scalar(ppmi_vec1, ppmi_vec2)

    lsa_vector1 = lsa.get(item[0]).values
    lsa_vector2 = lsa.get(item[1]).values
    lsa_vec1 = np.array([lsa_vector1])
    lsa_vec2 = np.array([lsa_vector2])
    lsa_vec1 = lsa_vec1[~np.isnan(lsa_vec1)]
    lsa_vec2 = lsa_vec2[~np.isnan(lsa_vec2)]
    lsa_number_cos = word_matrix.cosine_similarity(lsa_vec1, lsa_vec2)
    lsa_number_scalar = word_matrix.scalar(lsa_vec1, lsa_vec2)

    # PPMI model
    data_ppmi_cos.append('{}\t{}\t{}'.format(item[0], item[1], ppmi_number_cos))
    data_ppmi_scalar.append('{}\t{}\t{}'.format(item[0], item[1], ppmi_number_scalar))

    # LSA model
    data_lsa_cos.append('{}\t{}\t{}'.format(item[0], item[1], lsa_number_cos))
    data_lsa_scalar.append('{}\t{}\t{}'.format(item[0], item[1], lsa_number_scalar))

#  write to file
common_utils.write_file('data_ppmi_cos', data_ppmi_cos)
common_utils.write_file('data_ppmi_scalar', data_ppmi_scalar)
common_utils.write_file('data_lsa_cos', data_lsa_cos)
common_utils.write_file('data_lsa_scalar', data_lsa_scalar)
