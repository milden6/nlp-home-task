import numpy as np
import naive_bayes
import common_utils

# result_list
result_list = []

# Train data
path_train = './spam_train.csv'
sms_words, class_lables = common_utils.read_sms(path_train)
vocabulary_list = common_utils.create_vocabulary_list(sms_words)
train_marked_words = common_utils.set_of_words_list_to_vector(vocabulary_list, sms_words)
train_marked_words = np.array(train_marked_words)
p_words_spamicity, p_words_healthy, p_spam = naive_bayes.training(train_marked_words, class_lables)

# Classify test data
path = './spam_data.csv'
sms_words, class_lables = common_utils.read_sms(path)
sms_list = open(path, "r").readlines()

for i in range(len(sms_words)):
    smsType = naive_bayes.classify(vocabulary_list, p_words_spamicity,
                                p_words_healthy, p_spam, sms_words[i])
    if smsType == 0:
        row = "ham\t" + (sms_list[i].split(',')[1])
        result_list.append(row)
    else:
        row = "spam\t" + (sms_list[i].split(',')[1])
        result_list.append(row)

common_utils.write_file("result", result_list)