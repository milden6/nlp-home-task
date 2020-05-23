from nltk.tokenize import word_tokenize
import warnings
import gensim
from gensim.models import Word2Vec
import common_utils

warnings.filterwarnings(action='ignore')
path_wordsim = './wordsim353_sim_rel/wordsim_similarity_goldstandard.txt'

stop_words_set = set()
data_skip_gram_sim = []
data_cbow_sim = []

# read texts into list
texts_list = common_utils.get_texts_list('./Files/')

# get sentences list from texts list
sentences_list = common_utils.get_sentences_list(texts_list)

# load stop words list from file
stopwordsfile = open("stopwords.txt", "r")
for word in stopwordsfile:  # a stop word in each line
    word = word.replace("\n", '')
    word = word.replace("\r\n", '')
    stop_words_set.add(word)

words = common_utils.words_splitter(stop_words_set, sentences_list)

discrete_set = set()
for word in words:
    discrete_set.add(word)
vocabulary = list(discrete_set)

data = []

# iterate through each sentence
for sentence in sentences_list:
    temp = []

    # tokenize the sentence into words
    for j in word_tokenize(sentence):
        temp.append(j.lower())

    data.append(temp)

# create cbow model
cbow_model = gensim.models.Word2Vec(data, min_count=1, size=100, window=5)

# create skip gram model
skip_gram_model = gensim.models.Word2Vec(data, min_count=1, size=100, window=5, sg=1)

consistent_wordsim = common_utils.read_consistent_wordsim(path_wordsim, vocabulary)

for item in consistent_wordsim:
    cbow_sim = cbow_model.similarity(item[0], item[1])
    skip_gram_sim = skip_gram_model.similarity(item[0], item[1])

    data_cbow_sim.append('{}\t{}\t{}'.format(item[0], item[1], cbow_sim))
    data_skip_gram_sim.append('{}\t{}\t{}'.format(item[0], item[1], skip_gram_sim ))

common_utils.write_file('data_cbow_sim', data_cbow_sim)
common_utils.write_file('data_skip_gram_sim', data_skip_gram_sim)