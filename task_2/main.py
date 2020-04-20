import numpy as np
import matplotlib.pyplot as plot
import scipy.cluster.hierarchy as hier
import compare_strings
import tokenizator

# get word list
word_list = list(dict.fromkeys(tokenizator.get_words( open("./text.txt", "r").read()).lower().split(',')))

# remove empty field from list
for word in word_list:
    if word == '':
        word_list.remove(word)

# fill by zero
hamming_matrix = np.zeros((len(word_list), len(word_list)))
levenshtein_matrix = np.zeros((len(word_list), len(word_list)))
jaro_matrix = np.zeros((len(word_list), len(word_list)))

# compare string
for i in range(0, len(word_list)):
     for j in range(0, len(word_list)):
         hamming_matrix[i, j] = compare_strings.hammingDistance(word_list[i], word_list[j])
         levenshtein_matrix[i, j] = compare_strings.levenshteinDistance(word_list[i], word_list[j])
         jaro_matrix[i, j] = compare_strings.jaroDistance(word_list[i], word_list[j])

# figure size
plot.figure(figsize=(10, 8), dpi=300)

# Hamming
plot.title("Hamming")
linkage = hier.linkage(hamming_matrix, 'complete', 'correlation')
dendrogram = hier.dendrogram(linkage, 30, None, None, True, 'top', labels=word_list)
plot.savefig('hamming_distance.png')

# Levenshtein
plot.title("Levenshtein")
linkage = hier.linkage(levenshtein_matrix, 'complete', 'correlation')
dendrogram = hier.dendrogram(linkage, 30, None, None, True, 'top', labels=word_list)
plot.savefig('levenshtein_distance.png')

# Jaro
plot.title("Jaro")
linkage = hier.linkage(jaro_matrix, 'complete', 'correlation')
dendrogram = hier.dendrogram(linkage, 30, None, None, True, 'top', labels=word_list)
plot.savefig('jaro_distance.png')
