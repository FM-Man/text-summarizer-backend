from functools import lru_cache
import nltk
import re
from nltk.tokenize import RegexpTokenizer
from gensim.models import KeyedVectors
import pickle
import os
from sklearn.cluster import SpectralClustering
from math import ceil, exp
from collections import defaultdict
import numpy

nltk.download('punkt')

"""================================== step 1 =======================================
This part preprocesses the  input document. The preprocessing involves at first
tokenizing the input document and then removing the stop words. the tokenization is
done using the 'custom_tokenizer' function and stop word removal using the 
'stopword_removal' function.
================================================================================="""


def preprocessor(text):
    sentence_dividers = ['।', '|', '!', '\n', '?', ":"]
    sentences = custom_tokenizer(text, sentence_dividers)  # each sentences as intact and in a list

    word_dividers = [' ', ',', '.', ';', '"', "'", '`', '(', ')', '[', ']', '-', '‘', '’‌', '%', '/', '\\']
    words = []
    for sentence in sentences:
        words.append(custom_tokenizer(sentence, word_dividers))  # each word as a separate token now

    preprocessed_word_list = stopword_removal(words)

    # the returning variables are two list.
    # sentences = [sent1, sent2, sent3, ...]
    # preprocessed_word_list = [[word11, word12, ...], [word21, word22, ...], ...]
    return sentences, preprocessed_word_list


def custom_tokenizer(text, dividers):
    # idk what this regex part is doing. got it from stack overflow.
    divider_pattern = '|'.join(map(re.escape, dividers))
    tokenizer = RegexpTokenizer(f'[^{divider_pattern}]+|[{divider_pattern}]')
    tokens = tokenizer.tokenize(text)

    # removes the divider tokens and also strips them
    processed_tokens = []
    for token in tokens:
        if token.strip() and token not in dividers:
            processed_tokens.append(token.strip())

    return processed_tokens


def stopword_removal(sentences):
    stop_words = open("datasets\\stopwords.txt", "r", encoding="utf8").readlines()
    for stop_word in stop_words:
        stop_words.append(stop_word.split('\n')[0])

    preprocessed_word_list = []
    for sentence in sentences:
        preprocessed_word_list.append([word for word in sentence if word not in stop_words])

    return preprocessed_word_list


"""====================================step 2=======================================
Now the vector field consisting of over 1.4M bengali words are read. This function 
is cached to save time in future. 'pydic.dic' is a python dictionary written in
binary to save time reading. 'read_vectors_from_object_file' is used to read from
this file. 'cc.bn.300.vec' is a plain text file. 'read_vectors_from_plaintext' is 
used to read from here.
================================================================================="""


@lru_cache(maxsize=1)
def read_vector():
    if not os.path.exists('datasets\\pydic.dic'):
        if not os.path.exists('datasets\\cc.bn.300.vec'):
            print('dataset doesnot exist.'
                  'download from https://drive.google.com/file/d/1qSjqzygv8_T7LC_S21nCvv_x_Rt-BkK5/view?usp=sharing')
        else:
            data = read_vectors_from_plaintext('datasets\\cc.bn.300.vec')
            return data
    else:
        data = read_vectors_from_object_file()
        return data


def read_vectors_from_plaintext(vec_file_path):
    model = KeyedVectors.load_word2vec_format(vec_file_path, binary=False)
    print('dictionary done')

    file_path = 'datasets/pydic.dic'
    with open(file_path, "wb") as file:
        pickle.dump(model, file)
    print('saving done')

    return model


def read_vectors_from_object_file():
    file_path = 'datasets/pydic.dic'
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    print('reading done')
    return data


"""====================================step 3================================================
replaces all the words with corresponding vectors
=========================================================================================="""


def vectorizer(dataset, sentences):
    set_of_vectors = []

    for sentence in sentences:
        vectors_of_words_in_sentence = []
        for word in sentence:
            try:
                vector = dataset[word]
                vectors_of_words_in_sentence.append(vector)
            except KeyError:
                pass
        set_of_vectors.append(vectors_of_words_in_sentence)

    # returns a 3d list
    # [[vect1,vec2...],[vect3,vect4,...],...]
    return set_of_vectors


"""======================================step 4==============================================

=========================================================================================="""


def spectral_clustering(set_of_vectors, sigma):
    # making an empty 2d array for an affinity matrix
    total_sentence = len(set_of_vectors)
    affinity_matrix = []
    for i in range(0, total_sentence):
        row = [0] * total_sentence
        affinity_matrix.append(row)

    # calculating similarity for affinity matrix
    for i in range(0, total_sentence):
        for j in range(i + 1, total_sentence):
            affinity_matrix[i][j] = affinity_matrix[j][i] = (
                similarity(set_of_vectors[i], set_of_vectors[j], sigma))

    # number of clusters which is the size of the summary as the number of sentences
    n_clusters = ceil(total_sentence / 4)

    # clustering
    if len(affinity_matrix) > 1:
        model = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')
        model.fit(affinity_matrix)

        cluster_indices = defaultdict(list)
        for idx, label in enumerate(model.labels_):
            cluster_indices[label].append(idx)

        return cluster_indices

    else:
        return {}


def similarity(sentence_x, sentence_y, sigma):
    most_similar_distances = []

    # finding the distance of the closest word from sentence y for every word in sentence x
    for word_x in sentence_x:
        msd = float('inf')
        for word_y in sentence_y:
            dist = euclidean_distance(word_x, word_y)
            msd = min(dist, msd)
        most_similar_distances.append(msd)

    # finding the distance of the closest word from sentence x for every word in sentence y
    for word_y in sentence_y:
        msd = float('inf')
        for word_x in sentence_x:
            dist = euclidean_distance(word_x, word_y)
            msd = min(dist, msd)
        most_similar_distances.append(msd)

    # to avoid zero divide by chance
    if len(most_similar_distances) == 0:
        return 0

    avg_msd = sum(most_similar_distances) / len(most_similar_distances)

    # gaussian similarity
    return exp(- avg_msd ** 2 / (2 * sigma ** 2))


def euclidean_distance(vect1, vect2):
    return numpy.linalg.norm(vect1 - vect2)


# entry point
def get_summary(text, sigma=2):
    sentences, split_sentences = preprocessor(text)
    vector_space = read_vector()
    set_of_vectors = vectorizer(vector_space, split_sentences)

    set_of_clusters = spectral_clustering(set_of_vectors, sigma)
    indices_in_summary = []

    for cluster in set_of_clusters.items():
        picked_index = cluster[0]
        indices_in_summary.append(picked_index)

    for i in range(len(indices_in_summary)):
        for j in range(i + 1, len(indices_in_summary)):
            if indices_in_summary[i] > indices_in_summary[j]:
                indices_in_summary[i], indices_in_summary[j] = indices_in_summary[j], indices_in_summary[i]

    summary = ''
    for index in indices_in_summary:
        summary += sentences[index] + '। '

    return indices_in_summary, summary
