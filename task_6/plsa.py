import common_utils
import numpy as np

def plsa(number_of_topics, max_iter, documents):

    # get vocabulary and number of documents.
    vocabulary = common_utils.build_vocabulary(documents)
    number_of_documents = len(documents)
    vocabulary_size = len(vocabulary)

    # build term-doc matrix
    term_doc_matrix = np.zeros([number_of_documents, vocabulary_size], dtype=np.int)
    for d_index, doc in enumerate(documents):
        term_count = np.zeros(vocabulary_size, dtype=np.int)
        for word in doc:
            if word in vocabulary:
                w_index = vocabulary.index(word)
                term_count[w_index] = term_count[w_index] + 1
        term_doc_matrix[d_index] = term_count

    # create the counter arrays.
    document_topic_prob = np.zeros([number_of_documents, number_of_topics], dtype=np.float)  # P(z | d)
    topic_word_prob = np.zeros([number_of_topics, len(vocabulary)], dtype=np.float)  # P(w | z)
    topic_prob = np.zeros([number_of_documents, len(vocabulary), number_of_topics],
                               dtype=np.float)  # P(z | d, w)

    # randomly assign values
    document_topic_prob = np.random.random(size=(number_of_documents, number_of_topics))
    for d_index in range(len(documents)):
        common_utils.normalize(document_topic_prob[d_index])  # normalize for each document
    topic_word_prob = np.random.random(size=(number_of_topics, len(vocabulary)))
    for z in range(number_of_topics):
        common_utils.normalize(topic_word_prob[z])  # normalize for each topic

    # run the EM algorithm
    for iteration in range(max_iter):
        for d_index, document in enumerate(documents):
            for w_index in range(vocabulary_size):
                prob = document_topic_prob[d_index, :] * topic_word_prob[:, w_index]
                common_utils.normalize(prob)
                topic_prob[d_index][w_index] = prob
        # update P(w | z)
        for z in range(number_of_topics):
            for w_index in range(vocabulary_size):
                s = 0
                for d_index in range(len(documents)):
                    count = term_doc_matrix[d_index][w_index]
                    s = s + count * topic_prob[d_index, w_index, z]
                topic_word_prob[z][w_index] = s
            common_utils.normalize(topic_word_prob[z])

        # update P(z | d)
        for d_index in range(len(documents)):
            for z in range(number_of_topics):
                s = 0
                for w_index in range(vocabulary_size):
                    count = term_doc_matrix[d_index][w_index]
                    s = s + count * topic_prob[d_index, w_index, z]
                document_topic_prob[d_index][z] = s
            common_utils.normalize(document_topic_prob[d_index])

    return topic_word_prob, document_topic_prob
