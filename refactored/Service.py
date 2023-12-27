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


def euclidean_distance(vect1, vect2):
    return numpy.linalg.norm(vect1 - vect2)


def similarity(tuple1, tuple2, sigma):
    distances = []
    pos1, cluster1 = tuple1
    pos2, cluster2 = tuple2

    for vect1 in cluster1:
        min_dist = float('inf')
        for vect2 in cluster2:
            dist = euclidean_distance(vect1, vect2)
            min_dist = min(dist, min_dist)
        distances.append(min_dist)

    for vect1 in cluster2:
        min_dist = float('inf')
        for vect2 in cluster1:
            dist = euclidean_distance(vect1, vect2)
            min_dist = min(dist, min_dist)
        distances.append(min_dist)

    if len(distances) == 0:
        return 0

    average = sum(distances) / len(distances)

    return exp(- average ** 2 / (2 * sigma ** 2))


def spectral_clustering(sent_vectors_position, sigma):
    total_sentence = len(sent_vectors_position)
    affinity_matrix = []
    for i in range(0, total_sentence):
        row = [0] * total_sentence
        affinity_matrix.append(row)

    for i in range(0, total_sentence):
        for j in range(i + 1, total_sentence):
            affinity_matrix[i][j] = affinity_matrix[j][i] = similarity(sent_vectors_position[i],
                                                                       sent_vectors_position[j], sigma)

    cluster_number = ceil(total_sentence / 4)

    if len(affinity_matrix) > 1:
        model = SpectralClustering(n_clusters=cluster_number, affinity='precomputed')
        model.fit(affinity_matrix)

        cluster_indices = defaultdict(list)
        for idx, label in enumerate(model.labels_):
            cluster_indices[label].append(idx)

        return cluster_indices

    else:
        return {}


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


def read_vector():
    if not os.path.exists('datasets\\pydic.dic'):
        if not os.path.exists('datasets\\cc.bn.300.vec'):
            print(
                'dataset doesnot exist. download from https://drive.google.com/file/d/1qSjqzygv8_T7LC_S21nCvv_x_Rt'
                '-BkK5/view?usp=sharing')
        else:
            data = read_vectors_from_plaintext('datasets\\cc.bn.300.vec')
            return data
    else:
        data = read_vectors_from_object_file()
        return data


# caching the dataset reading
@lru_cache(maxsize=1)
def get_resource():
    return read_vector()


def split_text_by_dividers(text, dividers):
    divider_pattern = '|'.join(map(re.escape, dividers))

    tokenizer = RegexpTokenizer(f'[^{divider_pattern}]+|[{divider_pattern}]')
    sentences = tokenizer.tokenize(text)

    sentences = [sentence.strip() for sentence in sentences if sentence.strip() and sentence not in dividers]

    return sentences


def stopword_removal(words):
    stop_word_file = open("datasets\\stopwords.txt", "r", encoding="utf8")
    stop_words = stop_word_file.readlines()
    stop_words = [stop_word.split('\n')[0] for stop_word in stop_words]

    preprocessed_word_list = []
    for sentence in words:
        preprocessed_word_list.append([word for word in sentence if word not in stop_words])

    return preprocessed_word_list


def word_divider(text):
    sentence_dividers = ['।', '|', '!', '\n', '?', ":"]
    sentences = split_text_by_dividers(text=text, dividers=sentence_dividers)

    word_dividers = [' ', ',', '.', ';', '"', "'", '`', '(', ')', '[', ']', '-', '‘', '’‌', '%', '/', '\\']
    words = []
    for sentence in sentences:
        words.append(split_text_by_dividers(sentence, word_dividers))

    preprocessed_word_list = stopword_removal(words)
    return sentences, preprocessed_word_list


def vectorizer(dataset, sentences):
    vectors = []
    sentence_index = 0
    total_sentence = len(sentences)

    for sentence in sentences:
        vectors_of_words_in_sentence = []
        for word in sentence:
            try:
                vector = dataset[word]
                vectors_of_words_in_sentence.append(vector)
            except KeyError:
                pass
        sentence_index += 1
        vectors.append((sentence_index / total_sentence, vectors_of_words_in_sentence))

    return vectors


def get_summary(text, sigma=2):
    sentences, split_sentences = word_divider(text)
    vector_space = get_resource()

    vectors_with_position = vectorizer(vector_space, split_sentences)

    clustered_indices = spectral_clustering(vectors_with_position, sigma)
    summary_indices = []

    for cluster_idx, indices in clustered_indices.items():
        picked_index = indices[0]
        summary_indices.append(picked_index)

    for i in range(len(summary_indices)):
        for j in range(i + 1, len(summary_indices)):
            if summary_indices[i] > summary_indices[j]:
                summary_indices[i], summary_indices[j] = summary_indices[j], summary_indices[i]

    summary = ''
    for index in summary_indices:
        summary += sentences[index] + '। '

    return summary_indices, summary
