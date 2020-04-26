import math


def compute_tf(word_dict, word_list):
    tf_dict = {}

    for word, count in word_dict.items():
        tf_dict[word] = count / float(len(word_list))
    return tf_dict


def compute_idf(doc_list):
    idf_dict = dict.fromkeys(doc_list[0].keys(), 0)
    for doc in doc_list:
        for word, val in doc.items():
            if val > 0:
                if word in idf_dict:
                    idf_dict[word] += 1
                if word not in idf_dict:
                    idf_dict[word] = 1

    for word, val in idf_dict.items():
        idf_dict[word] = math.log10(len(doc_list) / float(val))

    return idf_dict


def compute_tf_idf(tfBow, idfs):
    tf_idf = {}
    for word, val in tfBow.items():
        tf_idf[word] = val * idfs[word]
    return tf_idf