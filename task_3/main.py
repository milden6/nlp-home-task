import tf_idf
import common_utils
import tokenizator
from collections import Counter

folder_path = "./Files/"
stop_words = []  # stop words list
dicts_list = []  # list of dict
tfs_list = []  # TF - list

google_blog_dict = {} # 1 - 10 Google blog
games_dict = {} # 11 - 20 Games reviews
news_dict = {} # 21 - 30 News from CNN

google_blog_list = [] # 1 - 10 Google blog
games_list = [] # 11 - 20 Games reviews
news_list = [] # 21 - 30 News from CNN

# compute TF for all text and append into list
# prepare list of dict for IDF computation
for text in common_utils.get_texts_list(folder_path):
    tfs_list.append(tf_idf.compute_tf(common_utils.create_dict(text), tokenizator.get_words(text)))
    dicts_list.append(common_utils.create_dict(text))

# compute IDF
result_of_idf = tf_idf.compute_idf(dicts_list)
counter = 1

for tf in tfs_list:
    # compute TF-IDF
    result_of_tf_idf = tf_idf.compute_tf_idf(tf, result_of_idf)

    # sort result of TF-IDF
    sorted_tf_idf = dict(sorted(result_of_tf_idf.items(), key=lambda key: key[1], reverse=True))

    # collect stop words
    for key, val in sorted_tf_idf.items():
        if val < 0.00008:
            stop_words.append(key)

    # collect thematic dicts by 10 text
    if counter <= 10:
        google_blog_dict.update(sorted_tf_idf)
    if counter > 10 and counter <= 20:
        games_dict.update(sorted_tf_idf)
    if counter > 20 and counter <= 30:
        news_dict.update(sorted_tf_idf)

    counter += 1

# sort thematic dicts
sorted_google_blog_dict = dict(sorted(google_blog_dict.items(), key=lambda key: key[1], reverse=True))
sorted_games_dict = dict(sorted(games_dict.items(), key=lambda key: key[1], reverse=True))
sorted_news_dict = dict(sorted(news_dict.items(), key=lambda key: key[1], reverse=True))

# prepare counter for getting common words
counter_google_blog_dict = Counter(sorted_google_blog_dict)
counter_games_dict = Counter(sorted_games_dict)
counter_news_dict = Counter(sorted_news_dict)

# get most commons words with high TF-IDF
common_words_google_blog_dict = counter_google_blog_dict.most_common(30)
common_words_games_dict = counter_games_dict.most_common(30)
common_words_news_dict = counter_news_dict.most_common(30)

for word in common_words_google_blog_dict:
    google_blog_list.append(word[0])

for word in common_words_games_dict:
    games_list.append(word[0])

for word in common_words_news_dict:
    news_list.append(word[0])

# delete duplicates and sort
stop_words = tokenizator.unique_words(stop_words)
stop_words.sort()

google_blog_list = tokenizator.unique_words(google_blog_list)
google_blog_list.sort()

games_list = tokenizator.unique_words(games_list)
games_list.sort()

news_list = tokenizator.unique_words(news_list)
news_list.sort()

# write files
common_utils.write_file("stop_words.txt", stop_words)

common_utils.write_file("google_blog_dict.txt", google_blog_list)
common_utils.write_file("games_dict.txt", games_list)
common_utils.write_file("news_dict.txt", news_list)