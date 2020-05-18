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


# metrics
def quality_control(path, test_count):

    sms_words, class_lables = common_utils.read_sms(path)

    true_positive_spam = 0.0
    true_negative_spam = 0.0
    false_positive_spam = 0.0
    false_negative_spam = 0.0

    true_positive_ham = 0.0
    true_negative_ham = 0.0
    false_positive_ham = 0.0
    false_negative_ham = 0.0

    test_words = []
    test_words_type = []

    for i in range(test_count):
        test_words_type.append(class_lables[i])
        test_words.append(sms_words[i])

    vocabulary_list = common_utils.create_vocabulary_list(sms_words)
    train_marked_words = common_utils.set_of_words_list_to_vector(vocabulary_list, sms_words)
    # Convert to array vector
    train_marked_words = np.array(train_marked_words)
    p_words_spamicity, p_words_healthy, p_spam = training(train_marked_words, class_lables)

    for i in range(test_count):
        sms_type = classify(vocabulary_list, p_words_spamicity,
                            p_words_healthy, p_spam, test_words[i])
        if (sms_type == 1) and (test_words_type[i] == 1):
            true_positive_spam += 1
        if (sms_type == 0) and (test_words_type[i] == 0):
            true_negative_spam += 1
        if (sms_type == 1) and (test_words_type[i] == 0):
            false_positive_spam += 1
        if (sms_type == 0) and (test_words_type[i] == 1):
            false_negative_spam += 1

        if (sms_type == 0) and (test_words_type[i] == 0):
            true_positive_ham += 1
        if (sms_type == 1) and (test_words_type[i] == 1):
            true_negative_ham += 1
        if (sms_type == 0) and (test_words_type[i] == 1):
            false_positive_ham += 1
        if (sms_type == 1) and (test_words_type[i] == 0):
            false_negative_ham += 1

    precision_spam = true_positive_spam / (true_positive_spam + false_positive_spam)
    recall_spam = true_positive_spam / (true_positive_spam + false_negative_spam)
    f_score_spam = 2 * ((precision_spam * recall_spam) / (precision_spam + recall_spam))

    precision_ham = true_positive_ham / (true_positive_ham + false_positive_ham)
    recall_ham = true_positive_ham / (true_positive_ham + false_negative_ham)
    f_score_ham = 2 * ((precision_ham * recall_ham) / (precision_ham + recall_ham))

    print(precision_spam, recall_spam, f_score_spam)
    print(precision_ham, recall_ham, f_score_ham)

    return 'Precision(spam): {}. Recall(spam): {}. F-score(spam): {}.\n Precision(ham): {}. '\
           'Recall(ham): {}. F-score(ham): {}.'.format(precision_spam, recall_spam, f_score_spam,
                                                       precision_ham, recall_ham, f_score_ham)
