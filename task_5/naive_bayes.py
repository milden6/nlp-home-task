import numpy as np
import common_utils
import random


# Train model
def training(train_marked_words, train_category):
    num_train_doc = len(train_marked_words)
    num_words = len(train_marked_words[0])

    pSpam = sum(train_category) / float(num_train_doc)

    # Count the number of occurrences of words in S and H in the corpus
    words_in_spam_num = np.ones(num_words)
    words_in_health_num = np.ones(num_words)
    spam_words_num = 2.0
    health_words_num = 2.0
    for i in range(0, num_train_doc):
        if train_category[i] == 1:  # if it spam
            words_in_spam_num += train_marked_words[i]
            spam_words_num += sum(train_marked_words[i])
        else:
            words_in_health_num += train_marked_words[i]
            health_words_num += sum(train_marked_words[i])

    p_words_spamicity = np.log(words_in_spam_num / spam_words_num)
    p_words_healthy = np.log(words_in_health_num / health_words_num)

    return p_words_spamicity, p_words_healthy, pSpam


#  Compute probability
def classify(vocabulary_list, p_words_spamicity, p_words_healthy, p_spam, test_words):
    test_words_count = common_utils.set_of_words_to_vector(vocabulary_list, test_words)
    test_words_marked_array = np.array(test_words_count)

    p1 = sum(test_words_marked_array * p_words_spamicity) + np.log(p_spam)
    p0 = sum(test_words_marked_array * p_words_healthy) + np.log(1 - p_spam)
    if p1 > p0:
        return 1
    else:
        return 0


# classification error rate
def quality_control(path, test_count):

    sms_words, class_lables = common_utils.read_sms(path)

    # cross-validation
    test_words = []
    test_words_type = []

    for i in range(test_count):
        random_index = int(random.uniform(0, len(sms_words)))
        test_words_type.append(class_lables[random_index])
        test_words.append(sms_words[random_index])
        del (sms_words[random_index])
        del (class_lables[random_index])

    vocabulary_list = common_utils.create_vocabulary_list(sms_words)
    train_marked_words = common_utils.set_of_words_list_to_vector(vocabulary_list, sms_words)
    # Convert to array vector
    train_marked_words = np.array(train_marked_words)
    p_words_spamicity, p_words_healthy, p_spam = training(train_marked_words, class_lables)

    error_count = 0.0
    for i in range(test_count):
        sms_type = classify(vocabulary_list, p_words_spamicity,
                            p_words_healthy, p_spam, test_words[i])
        if sms_type != test_words_type[i]:
            error_count += 1

    return 'Number of errors: {} Error rate: {}%'.format(error_count, ((error_count / test_count) * 100))
